import asyncio
import httpx
import os
import time

API_URL = "http://localhost:8000/api/v1"
TEST_VIDEO_PATH = "c:\\Users\\aprsa.SAHIL\\OneDrive\\Desktop\\Project1\\test_video.mp4"

async def test_flow():
    if not os.path.exists(TEST_VIDEO_PATH):
        print("Test video not found!")
        return
            
    print("Testing Upload...")
    async with httpx.AsyncClient(timeout=60.0) as client:
        headers = {"x-user-id": "test_user"}
        with open(TEST_VIDEO_PATH, "rb") as f:
            files = {"file": ("test_video.mp4", f, "video/mp4")}
            response = await client.post(f"{API_URL}/upload", files=files, headers=headers)
            
        print(f"Upload Response: {response.status_code}")
        if response.status_code != 200:
            print(f"Error: {response.text}")
            return
            
        data = response.json()
        job_id = data.get("job_id")
        print(f"Job ID: {job_id}")
        
        # 2. Poll status
        print("Polling status...")
        while True:
            status_resp = await client.get(f"{API_URL}/jobs/{job_id}", headers=headers)
            if status_resp.status_code != 200:
                print(f"Error getting status: {status_resp.text}")
                break
                
            status_data = status_resp.json()
            status = status_data.get("status")
            progress = status_data.get("progress_percentage", 0)
            stage = status_data.get("current_stage", "unknown")
            print(f"Status: {status} | Stage: {stage} | Progress: {progress}%")
            
            if status == "COMPLETED":
                print("Job Completed!")
                break
            elif status == "FAILED":
                print("Job Failed!")
                break
                
            time.sleep(2)
            
        # 3. Check analysis report
        print("Fetching Analysis Report...")
        analysis_resp = await client.get(f"{API_URL}/analysis/{job_id}", headers=headers)
        print(f"Analysis Response Code: {analysis_resp.status_code}")
        if analysis_resp.status_code == 200:
            print("Successfully fetched analysis report!")
            print(analysis_resp.json())
        else:
            print(f"Error: {analysis_resp.text}")

        # 4. Check history API
        print("Fetching Gameplays...")
        history_resp = await client.get(f"{API_URL}/gameplays", headers=headers)
        print(f"History Response Code: {history_resp.status_code}")
        if history_resp.status_code == 200:
            print(f"Total gameplays: {len(history_resp.json())}")

if __name__ == "__main__":
    asyncio.run(test_flow())
