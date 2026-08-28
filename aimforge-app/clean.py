import os
import re

def clean_unused(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace('import { BrowserRouter as Router, Routes, Route, Link, useLocation } from "react-router-dom";', 'import { BrowserRouter as Router, Routes, Route } from "react-router-dom";')
    content = content.replace('import { aimforgeService } from "../services/api";\nimport { useAppStore } from "../store/useAppStore";', '')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

clean_unused(r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\App.tsx')
clean_unused(r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\pages\TrainingPlanPage.tsx')

# Also fix the import types in api.ts and useAppStore.ts
def fix_types(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('import { AnalysisResponse, ChatMessage } from "../types";', 'import type { AnalysisResponse, ChatMessage } from "../types";')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_types(r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\services\api.ts')
fix_types(r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\store\useAppStore.ts')

print('Cleaned up unused variables and fixed type imports')
