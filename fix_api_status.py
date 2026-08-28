import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\services\api.ts'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace getJobStatus
status_start = content.find('getJobStatus: async (jobId: string)')
status_end = content.find('getAnalysis: async (jobId: string)')
if status_start != -1 and status_end != -1:
    new_status = '''getJobStatus: async (jobId: string): Promise<{ status: "pending" | "processing" | "completed" | "error" }> => {
    if (jobId === "mock-job") return { status: "completed" };
    try {
      const response = await axios.get(http://localhost:8000/api/v1/jobs/);
      const data = response.data;
      if (data.status === "COMPLETED") return { status: "completed" };
      if (data.status === "FAILED") return { status: "error" };
      if (data.status === "PROCESSING" || data.status === "UPLOADED") return { status: "processing" };
      return { status: "pending" };
    } catch (e) {
      console.error("Status error:", e);
      return { status: "error" };
    }
  },

  '''
    content = content[:status_start] + new_status + content[status_end:]

# Write back
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
