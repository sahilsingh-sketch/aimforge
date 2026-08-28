import os
import cv2

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend\services\upload_service.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
# Find where save_upload is called
save_call = r'(file_path, file_size = await StorageManager\.save_upload\(file, job_id\))'
def_match = re.search(save_call, content)
if def_match:
    original = def_match.group(1)
    new_code = original + '''
            # STEP 4: VIDEO VALIDATION
            import cv2
            import numpy as np
            cap = cv2.VideoCapture(file_path)
            if not cap.isOpened():
                print(f"[DEBUG VALIDATION] ERROR: OpenCV could not open {file_path}")
            else:
                fps = cap.get(cv2.CAP_PROP_FPS)
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                duration = frame_count / fps if fps > 0 else 0
                print(f"[DEBUG VALIDATION] fps: {fps}, width: {width}, height: {height}, duration: {duration}s")
                
                ret, frame = cap.read()
                if not ret or frame is None:
                    print(f"[DEBUG VALIDATION] ERROR: Could not read first frame!")
                else:
                    avg_color_per_row = np.average(frame, axis=0)
                    avg_color = np.average(avg_color_per_row, axis=0)
                    print(f"[DEBUG VALIDATION] First frame read successfully. Avg Color (BGR): {avg_color}")
                    if sum(avg_color) < 10:
                        print(f"[DEBUG VALIDATION] ERROR: FIRST FRAME IS COMPLETELY BLACK!")
                    else:
                        print(f"[DEBUG VALIDATION] SUCCESS: First frame has content.")
                    
                    # STEP 5: EXTRACT 5 FRAMES
                    debug_dir = StorageManager.get_debug_dir(job_id)
                    cv2.imwrite(os.path.join(debug_dir, "frame_test_1.jpg"), frame)
                    for i in range(2, 6):
                        ret, frame = cap.read()
                        if ret and frame is not None:
                            cv2.imwrite(os.path.join(debug_dir, f"frame_test_{i}.jpg"), frame)
                    print(f"[DEBUG VALIDATION] Extracted 5 frames to {debug_dir}")
                cap.release()
'''
    content = content.replace(original, new_code)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
