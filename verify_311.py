import sys
try:
    import torch
    print("PyTorch loaded")
except Exception as e:
    print("PyTorch failed:", e)

try:
    import paddleocr
    print("PaddleOCR loaded")
except Exception as e:
    print("PaddleOCR failed:", e)

