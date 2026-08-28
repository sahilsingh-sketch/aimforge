import os
import time
import json
from ultralytics import YOLO
import torch

def benchmark():
    workspaces = "storage/videos/workspaces"
    test_job = None
    frames_json_path = None
    
    # Find a valid job with frames
    for job in os.listdir(workspaces):
        frames_path = os.path.join(workspaces, job, "frames", "frames.json")
        if os.path.exists(frames_path):
            with open(frames_path, 'r') as f:
                data = json.load(f)
                if len(data) > 0:
                    test_job = job
                    frames_json_path = frames_path
                    frames_dir = os.path.join(workspaces, job, "frames")
                    frames_metadata = data
                    break
                    
    if not test_job:
        print("No valid job found for benchmarking.")
        return
        
    print(f"Benchmarking using job: {test_job}")
    print(f"CUDA Available: {torch.cuda.is_available()}")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}")
    
    model = YOLO("yolov8n.pt")
    
    # Select first 50 frames to benchmark original logic
    test_frames_meta = frames_metadata[:50]
    total_frames = len(test_frames_meta)
    
    print(f"Benchmarking Original Logic ({total_frames} frames)...")
    start_time = time.time()
    
    for meta in test_frames_meta:
        frame_path = os.path.join(frames_dir, meta["path"])
        if os.path.exists(frame_path):
            results = model.predict(source=frame_path, verbose=False)
            
    total_time = time.time() - start_time
    print(f"Original Logic Time: {total_time:.2f}s")
    print(f"Average time per frame: {(total_time / total_frames) * 1000:.2f}ms")
    
    # Benchmarking optimized logic (Batching)
    print("\nBenchmarking Optimized Logic (Batch Size=8, imgsz=640)...")
    valid_paths = [os.path.join(frames_dir, meta["path"]) for meta in test_frames_meta if os.path.exists(os.path.join(frames_dir, meta["path"]))]
    
    start_time = time.time()
    batch_size = 8
    
    for i in range(0, len(valid_paths), batch_size):
        batch = valid_paths[i:i + batch_size]
        results = model.predict(source=batch, verbose=False, device=device, imgsz=640, conf=0.35, classes=[0, 2, 3, 7, 24])
        
    total_time_opt = time.time() - start_time
    print(f"Optimized Logic Time: {total_time_opt:.2f}s")
    print(f"Optimized Average time per frame: {(total_time_opt / len(valid_paths)) * 1000:.2f}ms")
    print(f"Speedup: {total_time / total_time_opt:.2f}x")

if __name__ == "__main__":
    import torch
    original_load = torch.load
    def patched_load(*args, **kwargs):
        kwargs['weights_only'] = False
        return original_load(*args, **kwargs)
    torch.load = patched_load
    benchmark()
