import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\services\api.ts'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add axios import
if 'import axios from "axios";' not in content:
    content = 'import axios from "axios";\n' + content

# Replace uploadVideo to use axios
start = content.find('uploadVideo: async (file: File, _onProgress?: (percent: number) => void): Promise<{ jobId: string }> => {')
end = content.find('  getJobStatus: async')

new_upload = '''uploadVideo: async (file: File, onProgress?: (percent: number) => void): Promise<{ jobId: string }> => {
    const key = getGeminiKey();
    if (!key) {
      console.warn("No Gemini API key found. Using mock upload.");
      return new Promise((resolve) => {
        let p = 0;
        const interval = setInterval(() => {
          p += 10;
          if (onProgress) onProgress(p);
          if (p >= 100) {
            clearInterval(interval);
            resolve({ jobId: "mock-job" });
          }
        }, 300);
      });
    }

    try {
      // Use axios for upload progress
      const response = await axios.post(https://generativelanguage.googleapis.com/upload/v1beta/files?uploadType=media&key=, file, {
        headers: {
          "Content-Type": file.type,
        },
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            if (onProgress) {
              onProgress(Math.min(99, percentCompleted)); // Keep at 99 until backend fully responds
            }
          }
        }
      });

      return { jobId: response.data.file.name };
    } catch (error: any) {
      console.error("Upload error:", error);
      throw new Error(error.response?.data?.error?.message || "Failed to upload video");
    }
  },

'''

content = content[:start] + new_upload + content[end:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
