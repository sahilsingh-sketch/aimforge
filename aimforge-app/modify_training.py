import os
import re

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\pages\TrainingPlanPage.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

imports = '''
import { aimforgeService } from "../services/api";
import { useAppStore } from "../store/useAppStore";
'''
content = content.replace('import { useEffect } from "react";', f'import {{ useEffect, useState, useRef }} from "react";\n{imports}')

hook_logic = '''
  const navigate = useNavigate();
  const { analysis } = useAppStore();
'''
content = content.replace('export default function App() {\n  const navigate = useNavigate();\n', f'export default function App() {{\n{hook_logic}')

# Replace some static texts with dynamic if analysis is available
content = content.replace('184ms', '{analysis?.ratings.reactionTime || "184ms"}')
content = content.replace('92%', '{analysis?.ratings.accuracy || "92"}%')
content = content.replace('8.7', '{analysis?.ratings.aim || "8.7"}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('TrainingPlan modified')
