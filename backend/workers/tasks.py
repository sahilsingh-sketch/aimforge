import logging
import traceback
import sys
import os
import json
import time
from datetime import datetime, timezone
import contextlib
import httpx
from bs4 import BeautifulSoup
from dateutil import parser as date_parser

# CRITICAL FIX for Windows WinError 127: Load torch before cv2 to avoid DLL conflicts
import torch

try:
    import psutil
except ImportError:
    psutil = None

from backend.workers.celery_app import celery_app
from backend.core.database import SessionLocal, engine
# pyrefly: ignore [missing-import]
from sqlalchemy.exc import OperationalError
from backend.models.video_job import VideoJob
from backend.video_processing.extractor import extract_frames
from backend.video_processing.ocr_engine import run_ocr_pipeline
from backend.video_processing.yolo_engine import run_yolo_pipeline
from backend.video_processing.crosshair import process_crosshair
from backend.video_processing.movement_tracker import process_movement
from backend.video_processing.debug_annotator import generate_debug_images
from backend.core.config import settings
from backend.models.update import Update

logger = logging.getLogger(__name__)

@contextlib.contextmanager
def telemetry(stage_name):
    log_name = stage_name
    if stage_name == "AI_ANALYSIS":
        log_name = "AI"
    elif stage_name == "COMPLETED":
        log_name = "JOB"
        
    logger.info(f"[{log_name}] Started")
    start_time = time.time()
    yield
    elapsed = time.time() - start_time
    ram_str = ""
    if psutil:
        memory = psutil.Process().memory_info().rss / 1024 / 1024
        ram_str = f" | RAM: {memory:.2f}MB"
    logger.info(f"[{log_name}] Completed")
    logger.info(f"[CELERY] {stage_name} completed in {elapsed:.2f}s{ram_str}")

def update_job_state(job_id, stage, progress, status=None):
    for attempt in range(2):
        db = SessionLocal()
        try:
            logger.info(f"[CELERY] Updating DB... Stage changed to {stage}... Progress changed to {progress}...")
            job = db.query(VideoJob).filter(VideoJob.job_id == job_id).first()
            if job:
                job.current_stage = stage
                if status:
                    job.status = status
                else:
                    if stage not in ["COMPLETED", "FAILED", "UPLOADING", "QUEUED"]:
                        job.status = "PROCESSING"
                    else:
                        job.status = stage
                job.progress_percentage = progress
                db.commit()
                db.refresh(job)
                logger.info(f"[CELERY] DB commit successful... Stage: {stage}, Status: {job.status}, Progress: {progress}")
            return
        except OperationalError as e:
            db.rollback()
            logger.warning(f"OperationalError in update_job_state: {e}. Retrying...")
            engine.dispose()
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to update job state: {e}")
            raise
        finally:
            db.close()
    raise RuntimeError(f"Failed to update job state after 2 attempts for stage {stage}")

def handle_failure(job_id, stage_name, exc):
    full_traceback = traceback.format_exc()
    logger.error(f"[CELERY] {stage_name} failed:\n{full_traceback}")
    for attempt in range(2):
        db = SessionLocal()
        try:
            logger.info(f"[CELERY] Updating DB... Status changed... Progress changed...")
            job = db.query(VideoJob).filter(VideoJob.job_id == job_id).first()
            if job:
                job.status = "FAILED"
                job.error_message = full_traceback
                job.current_stage = stage_name
                job.progress_percentage = 0
                job.completed_at = datetime.now(timezone.utc)
                db.commit()
                db.refresh(job)
                logger.info(f"[CELERY] DB commit successful... Job status updated to FAILED for job {job_id}")
            return
        except OperationalError:
            db.rollback()
            engine.dispose()
        except Exception:
            db.rollback()
            return
        finally:
            db.close()

def run_pipeline(job_id: str, target_fps: int = 5):
    from backend.services.performance.profiler import Profiler
    profiler = Profiler()
    logger.info(f"[PIPELINE] CELERY_STARTED for job {job_id}")

    for attempt in range(2):
        db = SessionLocal()
        try:
            logger.info('[CELERY] Entering stage PIPELINE_INIT...')
            job = db.query(VideoJob).filter(VideoJob.job_id == job_id).first()
            if not job:
                logger.error(f"[CELERY] ERROR: Job {job_id} not found")
                db.close()
                return {"error": "Job not found"}
            
            # Guard against stale auto-started tasks
            if job.status != "QUEUED":
                logger.warning(f"[CELERY] Job {job_id} is in status {job.status} (not QUEUED). Aborting task as stale.")
                db.close()
                return {"error": "Job is stale or already processed"}
                
            storage_path = job.storage_path
            logger.info('[CELERY] DB query successful...')
            break
        except OperationalError:
            db.rollback()
            engine.dispose()
        except Exception as e:
            db.rollback()
            handle_failure(job_id, "PIPELINE_INIT", e)
            db.close()
            return
        finally:
            logger.info('[CELERY] Leaving stage PIPELINE_INIT...')
            db.close()

    # Initial status update now that we know the job is valid and not stale
    update_job_state(job_id, "UPLOADING", 100)
    update_job_state(job_id, "PROCESSING", 5)
            
    if not storage_path:
        handle_failure(job_id, "PIPELINE_INIT", ValueError("No storage_path"))
        return

    def create_callback(stage_name):
        def callback(progress_percent: int):
            update_job_state(job_id, stage_name, progress_percent)
            if progress_percent % 10 == 0 or progress_percent == 100:
                logger.info(f"[CELERY] {stage_name} progress: {progress_percent}%")
        return callback

    from backend.storage.manager import StorageManager
    job_dir = StorageManager.get_job_dir(job_id)
    frames_dir = StorageManager.get_frames_dir(job_id)
    analysis_dir = StorageManager.get_analysis_dir(job_id)
    debug_dir = StorageManager.get_debug_dir(job_id)
    local_video_path = os.path.join(job_dir, "temp_video.mp4")
    
    logger.info(f"[CELERY] Initialized local directories for job {job_id}:")
    logger.info(f"[CELERY] - job_dir: {job_dir}")
    logger.info(f"[CELERY] - frames_dir: {frames_dir}")
    logger.info(f"[CELERY] - analysis_dir: {analysis_dir}")
    logger.info(f"[CELERY] - debug_dir: {debug_dir}")
    
    try:
        # 0. DOWNLOAD S3 VIDEO
        try:
            logger.info('[CELERY] Entering stage DOWNLOAD_VIDEO...')
            logger.info(f"[CELERY] Downloading video from AWS S3")
            with telemetry("DOWNLOAD_VIDEO"):
                StorageManager.download_file(storage_path, local_video_path)
            
            if not os.path.exists(local_video_path):
                raise FileNotFoundError(f"DOWNLOAD_VIDEO failed: Local file not created at {local_video_path}")
            file_size_mb = os.path.getsize(local_video_path) / (1024 * 1024)
            if file_size_mb == 0:
                raise ValueError(f"DOWNLOAD_VIDEO failed: Local file {local_video_path} is 0 bytes.")
            logger.info(f"[CELERY] Temporary file successfully downloaded. Size: {file_size_mb:.2f} MB, Path: {local_video_path}")
        except Exception as e:
            handle_failure(job_id, "DOWNLOAD_VIDEO", e)
            return
        finally:
            logger.info('[CELERY] Leaving stage DOWNLOAD_VIDEO...')


        # 0.5 METADATA EXTRACTION
        try:
            logger.info('[CELERY] Entering stage METADATA_EXTRACTION...')
            logger.info("[CELERY] Metadata extraction started")
            with telemetry("METADATA_EXTRACTION"):
                from backend.video_processing.metadata import extract_video_metadata
                metadata = extract_video_metadata(local_video_path)
                metadata_path = os.path.join(job_dir, "metadata.json")
                with open(metadata_path, "w", encoding="utf-8") as meta_f:
                    json.dump(metadata, meta_f, indent=2)
                
                if not os.path.exists(metadata_path):
                    raise FileNotFoundError(f"METADATA_EXTRACTION failed: {metadata_path} not created.")
                meta_size_kb = os.path.getsize(metadata_path) / 1024
                logger.info(f"[CELERY] Generated metadata.json. Size: {meta_size_kb:.2f} KB, Path: {metadata_path}")
                
                # Update DB with metadata
                for attempt in range(2):
                    db = SessionLocal()
                    try:
                        job = db.query(VideoJob).filter(VideoJob.job_id == job_id).first()
                        if job:
                            job.fps = metadata.get("fps")
                            job.duration = metadata.get("duration")
                            job.width = metadata.get("width")
                            job.height = metadata.get("height")
                            db.commit()
                            logger.info(f'[CELERY] DB commit successful...')
                        break
                    except OperationalError:
                        db.rollback()
                        engine.dispose()
                    finally:
                        db.close()
        except Exception as e:
            handle_failure(job_id, "METADATA_EXTRACTION", e)
            return
        finally:
            logger.info('[CELERY] Leaving stage METADATA_EXTRACTION...')


        # 1. FRAME EXTRACTION (Sequential)
        try:
            logger.info('[PIPELINE] FRAME_EXTRACTION_STARTED')
            update_job_state(job_id, "FRAME_EXTRACTION", 0)
            profiler.start("FRAME_EXTRACTION")
            
            from backend.services.video.extractor import VideoExtractor
            extractor = VideoExtractor(job_id, local_video_path, frames_dir)
            frames_meta = extractor.extract_frames(target_fps=5, progress_callback=create_callback("FRAME_EXTRACTION"))
            
            frames_json_path = os.path.join(frames_dir, "frames.json")
            if not os.path.exists(frames_json_path):
                raise FileNotFoundError(f"FRAME_EXTRACTION failed: {frames_json_path} not created.")
            frames_size_kb = os.path.getsize(frames_json_path) / 1024
            logger.info(f"[CELERY] Generated frames.json. Size: {frames_size_kb:.2f} KB")
            
            if frames_meta:
                for attempt in range(2):
                    db = SessionLocal()
                    try:
                        job = db.query(VideoJob).filter(VideoJob.job_id == job_id).first()
                        if job:
                            job.frame_count = len(frames_meta)
                            db.commit()
                        break
                    except OperationalError:
                        db.rollback()
                        engine.dispose()
                    finally:
                        db.close()
            profiler.end("FRAME_EXTRACTION")
            logger.info('[PIPELINE] FRAME_EXTRACTION_COMPLETED')
        except Exception as e:
            handle_failure(job_id, "FRAME_EXTRACTION", e)
            return

        # 1.5 BGMI VALIDATION (Fallback)
        try:
            logger.info('[CELERY] Entering stage BGMI_VALIDATION...')
            update_job_state(job_id, "BGMI_VALIDATION", 0, status="PROCESSING")
            from backend.services.validation.bgmi_validator import BGMIValidator
            import cv2
            
            # Sample up to 5 frames from the extracted metadata
            sample_metadata = []
            if len(frames_meta) > 5:
                step = max(1, len(frames_meta) // 5)
                for i in range(0, len(frames_meta), step):
                    sample_metadata.append(frames_meta[i])
            else:
                sample_metadata = frames_meta
                
            sample_frames = []
            for meta in sample_metadata[:5]:
                frame_path = os.path.join(frames_dir, meta["path"])
                if os.path.exists(frame_path):
                    img = cv2.imread(frame_path)
                    if img is not None:
                        sample_frames.append(img)
                        
            validator = BGMIValidator()
            validation_result = validator.validate_frames(sample_frames)
            
            if not validation_result.get("valid"):
                logger.warning(f"[CELERY] BGMI_VALIDATION failed. Status: INVALID_GAMEPLAY")
                for attempt in range(2):
                    db = SessionLocal()
                    try:
                        job = db.query(VideoJob).filter(VideoJob.job_id == job_id).first()
                        if job:
                            job.status = "INVALID_GAMEPLAY"
                            job.error_message = validation_result.get("reason", "Unknown")
                            job.current_stage = "BGMI_VALIDATION"
                            job.progress_percentage = 0
                            db.commit()
                        break
                    except OperationalError:
                        db.rollback()
                        engine.dispose()
                    finally:
                        db.close()
                return {"status": "error", "message": "Invalid gameplay video"}
            
            logger.info('[CELERY] BGMI_VALIDATION passed.')
        except Exception as e:
            handle_failure(job_id, "BGMI_VALIDATION", e)
            return

        # 2. SEQUENTIAL/PARALLEL PROCESSING
        try:
            logger.info('[CELERY] Entering SEQUENTIAL/PARALLEL STAGES...')
            update_job_state(job_id, "PROCESSING", 0, status="PROCESSING")
            
            # Run ML Models sequentially to avoid VRAM OOM and safely utilize memory cache
            logger.info("[PIPELINE] OCR_STARTED")
            profiler.start("OCR")
            from backend.services.ocr.ocr_service import run_ocr_pipeline
            run_ocr_pipeline(job_id, progress_callback=create_callback("OCR"))
            profiler.end("OCR")
            logger.info("[PIPELINE] OCR_COMPLETED")
            
            logger.info("[PIPELINE] DETECTION_STARTED")
            profiler.start("OBJECT_DETECTION")
            from backend.services.detection.yolo_service import run_yolo_pipeline
            run_yolo_pipeline(job_id, progress_callback=create_callback("OBJECT_DETECTION"))
            profiler.end("OBJECT_DETECTION")
            logger.info("[PIPELINE] DETECTION_COMPLETED")
            
            # Run lightweight processing tasks in parallel
            from concurrent.futures import ThreadPoolExecutor, as_completed
            
            def run_crosshair():
                profiler.start("CROSSHAIR")
                process_crosshair(job_id=job_id)
                profiler.end("CROSSHAIR")
                return "CROSSHAIR"
                
            def run_movement():
                profiler.start("MOVEMENT")
                process_movement(job_id=job_id)
                profiler.end("MOVEMENT")
                return "MOVEMENT"
                
            def run_debug():
                profiler.start("DEBUG_GENERATION")
                generate_debug_images(job_id=job_id)
                profiler.end("DEBUG_GENERATION")
                return "DEBUG_GENERATION"
            
            logger.info("[CELERY] Running lightweight tasks in parallel...")
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = [
                    executor.submit(run_crosshair),
                    executor.submit(run_movement),
                    executor.submit(run_debug)
                ]
                for future in as_completed(futures):
                    stage_name = future.result()
                    logger.info(f"[PARALLEL] {stage_name} completed.")
                    
        except Exception as e:
            handle_failure(job_id, "PARALLEL_PROCESSING", e)
            return

        # 7. AI ANALYSIS
        try:
            logger.info('[CELERY] Entering stage AI_ANALYSIS...')
            logger.info("[CELERY] AI Analysis started")
            update_job_state(job_id, "AI_ANALYSIS", 0)
            with telemetry("AI_ANALYSIS"):
                from backend.services.ai_analysis import generate_ai_report
                generate_ai_report(job_id)
            update_job_state(job_id, "REPORT_GENERATION", 100)
            logger.info(f"[REPORT] Saved")
        except Exception as e:
            handle_failure(job_id, "AI_ANALYSIS", e)
            return
        finally:
            logger.info('[CELERY] Leaving stage AI_ANALYSIS...')


        # 8. COMPLETED
        try:
            logger.info('[CELERY] Entering stage COMPLETED...')
            logger.info(f"[CELERY] Saving report")
            with telemetry("COMPLETED"):
                for attempt in range(2):
                    db = SessionLocal()
                    try:
                        final_job = db.query(VideoJob).filter(VideoJob.job_id == job_id).first()
                        if final_job:
                            final_job.status = "COMPLETED"
                            final_job.progress_percentage = 100
                            final_job.completed_at = datetime.now(timezone.utc)
                            final_job.current_stage = "COMPLETED"
                            db.commit()
                            logger.info(f"[PIPELINE] COMPLETED")
                        break
                    except OperationalError:
                        db.rollback()
                        engine.dispose()
                    finally:
                        db.close()
        except Exception as e:
            handle_failure(job_id, "COMPLETED", e)
            return
        finally:
            logger.info('[CELERY] Leaving stage COMPLETED...')


        profiler.summary()
        return {"status": "success", "job_id": job_id}

    except Exception as e:
        handle_failure(job_id, "PIPELINE", e)
    finally:
        try:
            if 'local_video_path' in locals() and os.path.exists(local_video_path):
                os.remove(local_video_path)
                logger.info(f"[CELERY] Temporary file deleted")
        except Exception as cleanup_error:
            logger.warning(f"Failed to delete temp video file {local_video_path}: {cleanup_error}")

@celery_app.task(bind=True, name="backend.workers.extract_frames_task")
def extract_frames_task(self, job_id: str, target_fps: int = 2):
    return run_pipeline(job_id, target_fps)

def safe_date_parse(date_str):
    if not date_str:
        return None
    try:
        return date_parser.parse(date_str)
    except Exception:
        return None

@celery_app.task(bind=True, name="backend.workers.tasks.fetch_bgmi_updates")
def fetch_bgmi_updates(self):
    logger.info("[BGMI_UPDATES] Starting BGMI updates fetcher")
    updates_to_save = []
    
    # 1. Fetch from GNews API
    if settings.GNEWS_API_KEY:
        try:
            url = "https://gnews.io/api/v4/search"
            params = {
                "q": "BGMI",
                "lang": "en",
                "max": "10",
                "apikey": settings.GNEWS_API_KEY
            }
            res = httpx.get(url, params=params, timeout=10)
            if res.status_code == 200:
                data = res.json()
                for article in data.get("articles", []):
                    updates_to_save.append({
                        "source": "GNEWS",
                        "source_url": article.get("url"),
                        "external_id": None,
                        "title": article.get("title"),
                        "description": article.get("description"),
                        "thumbnail_url": article.get("image"),
                        "category": "GAME_NEWS",
                        "status": "NEWS",
                        "published_at": safe_date_parse(article.get("publishedAt"))
                    })
            else:
                logger.warning(f"[BGMI_UPDATES] GNews API failed with {res.status_code}")
        except Exception as e:
            logger.error(f"[BGMI_UPDATES] Failed to fetch GNews: {e}")

    # 2. Fetch from YouTube API (Tournament/Pro Play)
    if settings.YOUTUBE_API_KEY:
        queries = [
            {"q": "BGMI esports", "category": "TOURNAMENT", "status": "COMPLETED"},
            {"q": "BGMI tournament", "category": "TOURNAMENT", "status": "COMPLETED"},
            {"q": "BGMI pro players", "category": "PRO_PLAY", "status": "COMPLETED"},
            {"q": "BGMI gameplay", "category": "GAME_NEWS", "status": "NEWS"}
        ]
        
        for q_item in queries:
            try:
                url = "https://www.googleapis.com/youtube/v3/search"
                params = {
                    "part": "snippet",
                    "q": q_item["q"],
                    "maxResults": "3",
                    "order": "date",
                    "type": "video",
                    "key": settings.YOUTUBE_API_KEY
                }
                res = httpx.get(url, params=params, timeout=10)
                if res.status_code == 200:
                    data = res.json()
                    for item in data.get("items", []):
                        snippet = item.get("snippet", {})
                        video_id = item.get("id", {}).get("videoId")
                        updates_to_save.append({
                            "source": "YOUTUBE",
                            "source_url": f"https://youtube.com/watch?v={video_id}",
                            "external_id": video_id,
                            "title": snippet.get("title", "").replace("&quot;", '"').replace("&#39;", "'"),
                            "description": snippet.get("description"),
                            "thumbnail_url": snippet.get("thumbnails", {}).get("high", {}).get("url"),
                            "category": q_item["category"],
                            "status": q_item["status"],
                            "published_at": safe_date_parse(snippet.get("publishedAt"))
                        })
                else:
                    logger.warning(f"[BGMI_UPDATES] YouTube API failed for {q_item['q']} with {res.status_code}: {res.text}")
            except Exception as e:
                logger.error(f"[BGMI_UPDATES] Failed to fetch YouTube query {q_item['q']}: {e}")

    # 3. Krafton Scraper (Fallback for official news)
    # They don't have a simple REST API, so we scrape the first page of news.
    try:
        url = "https://battlegroundsmobileindia.com/news"
        # We need headers that look like a browser to avoid simple bot blocks
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        res = httpx.get(url, headers=headers, timeout=15)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            # This relies on current DOM structure
            news_items = soup.select(".news-list .item")
            for item in news_items:
                link_el = item.select_one("a")
                title_el = item.select_one(".title")
                date_el = item.select_one(".date")
                
                if link_el and title_el:
                    link = link_el.get("href")
                    if link and not link.startswith("http"):
                        link = "https://battlegroundsmobileindia.com" + link
                    
                    # They don't typically have thumbnail per list item, but we'll try
                    img_el = item.select_one("img")
                    thumbnail = img_el.get("src") if img_el else None
                    if thumbnail and not thumbnail.startswith("http"):
                        thumbnail = "https://battlegroundsmobileindia.com" + thumbnail
                        
                    updates_to_save.append({
                        "source": "KRAFTON",
                        "source_url": link,
                        "external_id": link,
                        "title": title_el.text.strip(),
                        "description": "",
                        "thumbnail_url": thumbnail,
                        "category": "GAME_NEWS",
                        "status": "NEWS",
                        "published_at": safe_date_parse(date_el.text.strip() if date_el else None)
                    })
    except Exception as e:
        logger.error(f"[BGMI_UPDATES] Failed to scrape Krafton: {e}")

    # Save to database and deduplicate
    db = SessionLocal()
    try:
        new_records_added = 0
        for upd in updates_to_save:
            # Check by external_id if exists
            exists = False
            if upd["external_id"]:
                exists = db.query(Update).filter(Update.external_id == upd["external_id"]).first()
            
            # Fallback check by source_url
            if not exists and upd["source_url"]:
                exists = db.query(Update).filter(Update.source_url == upd["source_url"]).first()
                
            if not exists:
                new_update = Update(**upd)
                db.add(new_update)
                new_records_added += 1
                
        if new_records_added > 0:
            db.commit()
            logger.info(f"[BGMI_UPDATES] Added {new_records_added} new updates to database.")
        else:
            logger.info("[BGMI_UPDATES] No new updates found.")
    except Exception as e:
        db.rollback()
        logger.error(f"[BGMI_UPDATES] Error saving updates to DB: {e}")
    finally:
        db.close()

