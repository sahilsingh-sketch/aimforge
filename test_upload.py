import requests

try:
    with open('test_video.mp4', 'rb') as f:
        # Use python-requests to upload
        response = requests.post('http://127.0.0.1:8000/api/v1/upload', files={'file': ('test_video.mp4', f, 'video/mp4')})
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
