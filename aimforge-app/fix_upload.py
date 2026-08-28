import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\pages\UploadPage.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports for store and API
if 'useAppStore' not in content:
    content = content.replace('import { useState } from "react";', 'import { useState } from "react";\nimport { useAppStore } from "../store/useAppStore";\nimport { aimforgeService } from "../services/api";')

# Inject hooks
content = content.replace('const navigate = useNavigate();', 'const navigate = useNavigate();\n  const { setJobId, setVideoUrl } = useAppStore();')

# Replace startUpload
new_upload = '''const startUpload = async () => {
    if (!file) return;
    
    setIsUploading(true);
    setUploadProgress(10);
    
    try {
      // Save local video URL for preview
      setVideoUrl(URL.createObjectURL(file));
      
      const { jobId } = await aimforgeService.uploadVideo(file, (p) => setUploadProgress(p));
      setUploadProgress(100);
      setJobId(jobId);
      
      setTimeout(() => navigate("/processing"), 500);
    } catch (e) {
      console.error(e);
      setError("Failed to upload video");
      setIsUploading(false);
    }
  };'''

start = content.find('const startUpload = () => {')
end = content.find('const cancelUpload = () => {')

content = content[:start] + new_upload + '\n\n  ' + content[end:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated UploadPage')
