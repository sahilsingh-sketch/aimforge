import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\services\api.ts'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the direct gemini upload with our backend
new_upload = '''
      // Use our backend for video processing
      const formData = new FormData();
      formData.append("file", file);
      
      const response = await axios.post("http://localhost:8000/api/v1/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            if (onProgress) {
              onProgress(Math.min(99, percentCompleted));
            }
          }
        }
      });

      return { jobId: response.data.job_id };
'''

# Find the start and end of the try block in uploadVideo
start_idx = content.find('try {\n      // Use axios for upload progress')
if start_idx != -1:
    end_idx = content.find('return { jobId: response.data.file.name };', start_idx)
    if end_idx != -1:
        end_idx += len('return { jobId: response.data.file.name };\n')
        content = content[:start_idx] + 'try {\n' + new_upload + content[end_idx:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
