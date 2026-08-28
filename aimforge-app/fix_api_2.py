import os
import re

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\services\api.ts'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the whole SYSTEM_PROMPT block with a double-quoted string
start = content.find('const SYSTEM_PROMPT =')
end = content.find('export const aimforgeService = {')

prompt = '''const SYSTEM_PROMPT = "You are an elite, professional BGMI/PUBG Mobile AI Coach.\\n" +
"Analyze the provided gameplay video thoroughly.\\n" +
"Pay extremely close attention to the player's crosshair placement, recoil control, positioning, movement, and trade timing.\\n" +
"Identify specific timestamps where the player made mistakes or exceptional plays.\\n\\n" +
"You MUST return your response as a strict JSON object matching this exact TypeScript interface:\\n" +
"{\\n" +
"  jobId: string;\\n" +
"  overallScore: number; // 0-10\\n" +
"  strengths: string[];\\n" +
"  weaknesses: string[];\\n" +
"  mistakes: string[];\\n" +
"  improvements: string[];\\n" +
"  events: {\\n" +
"    id: string; // unique string\\n" +
"    timestamp: string; // format \\"MM:SS\\"\\n" +
"    seconds: number; // integer seconds\\n" +
"    title: string;\\n" +
"    severity: \\"critical\\" | \\"warning\\" | \\"positive\\" | \\"info\\";\\n" +
"    category: string; // e.g. \\"Aim\\", \\"Timing\\", \\"Positioning\\"\\n" +
"    confidence: number; // 0-100\\n" +
"    description: string;\\n" +
"  }[];\\n" +
"  ratings: {\\n" +
"    aim: number; // 0-100\\n" +
"    movement: number;\\n" +
"    positioning: number;\\n" +
"    gameSense: number;\\n" +
"    recoil: number;\\n" +
"    crosshair: number;\\n" +
"    decisions: number;\\n" +
"    utility: number;\\n" +
"  };\\n" +
"  summary: string;\\n" +
"  recommendations: string[];\\n" +
"  trainingPlan: {\\n" +
"    drills: string[];\\n" +
"    focusAreas: string[];\\n" +
"  };\\n" +
"}\\n\\n" +
"Do not include markdown blocks like `json. Output ONLY raw JSON.";\\n\\n'''

content = content[:start] + prompt + content[end:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed SYSTEM_PROMPT')
