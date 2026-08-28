import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\pages\Dashboard.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix hooks
content = content.replace('const { analysis, setAnalysis, currentVideoTime, setCurrentVideoTime } = useAppStore();', 'const { analysis, setAnalysis, currentVideoTime, setCurrentVideoTime, jobId, videoUrl } = useAppStore();')

content = content.replace('const data = await aimforgeService.getAnalysis("demo-job-id");', 'const data = await aimforgeService.getAnalysis(jobId || "mock-job");')

# Replace video URL
old_video = 'src="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"'
content = content.replace(old_video, 'src={videoUrl || "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"}')

# Bind dynamic analysis data to Dashboard stats
# Overall score
content = content.replace('8.7</span>', '{analysis?.overallScore || 8.7}</span>')
# Strengths
content = content.replace('<span>Recoil Control</span>', '<span>{analysis?.strengths?.[0] || "Recoil Control"}</span>')
content = content.replace('<span>Trade Timing</span>', '<span>{analysis?.strengths?.[1] || "Trade Timing"}</span>')
# Weaknesses
content = content.replace('<span>Pre-aim Height</span>', '<span>{analysis?.weaknesses?.[0] || "Pre-aim Height"}</span>')
content = content.replace('<span>Reaction Time</span>', '<span>{analysis?.weaknesses?.[1] || "Reaction Time"}</span>')

# Map ratings dynamically
content = content.replace('Aim</span>\\n                              <span className="font-semibold text-neutral-50 text-sm leading-5">\\n                                88', 'Aim</span>\\n                              <span className="font-semibold text-neutral-50 text-sm leading-5">\\n                                {analysis?.ratings?.aim || 88}')
content = content.replace('Movement</span>\\n                              <span className="font-semibold text-neutral-50 text-sm leading-5">\\n                                76', 'Movement</span>\\n                              <span className="font-semibold text-neutral-50 text-sm leading-5">\\n                                {analysis?.ratings?.movement || 76}')
content = content.replace('Positioning</span>\\n                              <span className="font-semibold text-neutral-50 text-sm leading-5">\\n                                62', 'Positioning</span>\\n                              <span className="font-semibold text-neutral-50 text-sm leading-5">\\n                                {analysis?.ratings?.positioning || 62}')
content = content.replace('Game Sense</span>\\n                              <span className="font-semibold text-neutral-50 text-sm leading-5">\\n                                71', 'Game Sense</span>\\n                              <span className="font-semibold text-neutral-50 text-sm leading-5">\\n                                {analysis?.ratings?.gameSense || 71}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated Dashboard')
