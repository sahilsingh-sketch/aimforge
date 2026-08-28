import logging
from collections import Counter

logger = logging.getLogger(__name__)

class TelemetryAggregator:
    @staticmethod
    def format_timestamp(ts: float) -> str:
        minutes = int(ts // 60)
        seconds = int(ts % 60)
        return f"{minutes:02d}:{seconds:02d}"

    @classmethod
    def summarize(cls, ocr_data: list, yolo_data: list, crosshair_data: list, movement_data: list, video_duration: float = 0) -> str:
        import json
        import math
        from collections import Counter
        """
        Groups telemetry into fixed 60-second chunks spanning the entire match.
        Outputs a fully structured JSON string to guarantee the LLM sees the complete timeline.
        """
        # Determine duration if not provided
        max_ts = 0
        for d in (ocr_data, yolo_data, crosshair_data, movement_data):
            for item in d:
                if item.get("timestamp") and item["timestamp"] > max_ts:
                    max_ts = item["timestamp"]
        
        duration = max(video_duration, max_ts)
        if duration == 0:
            return json.dumps({"error": "No telemetry data found"}, indent=2)

        # 60s segments
        segment_duration = 60
        num_segments = math.ceil(duration / segment_duration)
        segments = []
        
        # Organize data by segment
        ocr_by_segment = [[] for _ in range(num_segments)]
        yolo_by_segment = [[] for _ in range(num_segments)]
        
        for item in ocr_data:
            ts = item.get("timestamp", 0)
            idx = min(int(ts // segment_duration), num_segments - 1)
            ocr_by_segment[idx].append(item)
            
        for item in yolo_data:
            ts = item.get("timestamp", 0)
            idx = min(int(ts // segment_duration), num_segments - 1)
            yolo_by_segment[idx].append(item)

        global_max_kills = 0
        enemy_encounters = 0
        vehicle_frames = 0
        health_readings = []
        
        for i in range(num_segments):
            start_time = i * segment_duration
            end_time = min((i + 1) * segment_duration, duration)
            
            ocr_items = ocr_by_segment[i]
            yolo_items = yolo_by_segment[i]
            
            # segment stats
            kills = 0
            weapons = Counter()
            healths = []
            enemies_spotted = 0
            vehicles = 0
            
            for item in ocr_items:
                if item.get("kills"):
                    kills = max(kills, item["kills"])
                    global_max_kills = max(global_max_kills, item["kills"])
                if item.get("weapon"):
                    weapons[item["weapon"]] += 1
                if item.get("health") is not None:
                    healths.append(item["health"])
                    health_readings.append(item["health"])
                    
            for item in yolo_items:
                c = item.get("class")
                if c == "Player":
                    enemies_spotted += 1
                    enemy_encounters += 1
                elif c == "Vehicle":
                    vehicles += 1
                    vehicle_frames += 1
                    
            avg_health = sum(healths) / len(healths) if healths else None
            top_weapon = weapons.most_common(1)[0][0] if weapons else None
            
            activity = "LOW_ACTIVITY"
            if enemies_spotted > 0:
                activity = "COMBAT"
            elif vehicles > 0:
                activity = "ROTATION"
            elif top_weapon and len(ocr_items) > 10:
                activity = "LOOTING_OR_HOLDING"
                
            observations = []
            if enemies_spotted > 5:
                observations.append("Heavy enemy presence detected.")
            elif enemies_spotted > 0:
                observations.append("Enemy spotted in line of sight.")
                
            if vehicles > 0:
                observations.append("Player is interacting with or near a vehicle.")
                
            if avg_health is not None and avg_health < 40:
                observations.append(f"Health dropped critical (avg {avg_health:.1f}%).")
                
            if kills > 0:
                observations.append(f"Kills recorded at this segment: {kills}")
                
            if activity == "LOW_ACTIVITY":
                observations.append("No significant events detected.")

            segments.append({
                "start_time": start_time,
                "end_time": end_time,
                "start_time_fmt": cls.format_timestamp(start_time),
                "end_time_fmt": cls.format_timestamp(end_time),
                "activity": activity,
                "avg_health": round(avg_health, 1) if avg_health else None,
                "top_weapon": top_weapon,
                "enemies_spotted_frames": enemies_spotted,
                "observations": observations
            })
            
        full_coverage_data = {
            "video_duration_seconds": duration,
            "total_segments": num_segments,
            "global_stats": {
                "max_kills": global_max_kills,
                "total_enemy_detection_frames": enemy_encounters,
                "total_vehicle_frames": vehicle_frames,
                "avg_health_overall": round(sum(health_readings) / len(health_readings), 1) if health_readings else 100
            },
            "timeline": segments
        }
        
        return json.dumps(full_coverage_data, indent=2)
