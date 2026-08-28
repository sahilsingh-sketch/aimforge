import requests

try:
    with open('test_video.mp4', 'rb') as f:
        response = requests.post('http://localhost:8000/api/v1/upload', files={'file': f})
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
