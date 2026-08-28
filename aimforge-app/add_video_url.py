import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\store\useAppStore.ts'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('  jobId: string | null;', '  jobId: string | null;\n  videoUrl: string | null;\n  setVideoUrl: (url: string | null) => void;')
content = content.replace('  jobId: null,', '  jobId: null,\n  videoUrl: null,\n  setVideoUrl: (url) => set({ videoUrl: url }),')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
