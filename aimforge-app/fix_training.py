import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\pages\TrainingPlanPage.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Make sure useAppStore is imported and used
if 'useAppStore' not in content:
    content = content.replace('import { useNavigate } from "react-router-dom";', 'import { useNavigate } from "react-router-dom";\nimport { useAppStore } from "../store/useAppStore";')
    content = content.replace('const navigate = useNavigate();', 'const navigate = useNavigate();\n  const { analysis } = useAppStore();')

# Replace static values if they haven't been replaced yet
if '184ms' in content:
    content = content.replace('184ms', '{analysis?.ratings?.reactionTime || "184"}ms')
if '92%' in content:
    content = content.replace('92%', '{analysis?.ratings?.accuracy || "92"}%')
if '8.7<' in content:
    content = content.replace('8.7<', '{analysis?.overallScore || "8.7"}<')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
