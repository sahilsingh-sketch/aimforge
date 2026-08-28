import os
import re

files = [
    'LandingPage.tsx',
    'Dashboard.tsx',
    'HistoryPage.tsx',
    'TrainingPlanPage.tsx',
    'AiCoachPage.tsx',
    'ProfilePage.tsx'
]

for page in files:
    path = os.path.join('src', 'pages', page)
    if not os.path.exists(path): continue
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # ensure useNavigate is present
    if 'useNavigate' not in content:
        content = content.replace('import { useEffect', 'import { useNavigate } from "react-router-dom";\nimport { useEffect')
        if 'import { useNavigate' not in content:
            # If no useEffect
            content = 'import { useNavigate } from "react-router-dom";\n' + content

    if 'const navigate = useNavigate();' not in content:
        content = content.replace('export default function App() {\n', 'export default function App() {\n  const navigate = useNavigate();\n')

    # Replace navigation texts with clickable spans
    if page == 'LandingPage.tsx':
        content = content.replace('>\n              Dashboard\n            </button>', ' onClick={() => navigate("/dashboard")} style={{cursor: "pointer"}}>\n              Dashboard\n            </button>')
        content = content.replace('>\n              Analysis\n            </button>', ' onClick={() => navigate("/dashboard")} style={{cursor: "pointer"}}>\n              Analysis\n            </button>')
        content = content.replace('>\n              History\n            </button>', ' onClick={() => navigate("/history")} style={{cursor: "pointer"}}>\n              History\n            </button>')
        content = content.replace('>\n              Training\n            </button>', ' onClick={() => navigate("/training")} style={{cursor: "pointer"}}>\n              Training\n            </button>')
        content = content.replace('>\n              AI Coach\n            </button>', ' onClick={() => navigate("/coach")} style={{cursor: "pointer"}}>\n              AI Coach\n            </button>')
        content = content.replace('>\n              Profile\n            </button>', ' onClick={() => navigate("/profile")} style={{cursor: "pointer"}}>\n              Profile\n            </button>')
        
        # Action buttons
        content = content.replace('<Button className="rounded-lg bg-[#f54900] text-orange-50">', '<Button className="rounded-lg bg-[#f54900] text-orange-50" onClick={() => navigate("/dashboard")}>')
        content = content.replace('<Button\n                className="shadow-[0_0_30px_oklch(0.646_0.222_41.116/0.4)] rounded-xl bg-[#f54900] text-orange-50 gap-2"\n                size="lg"\n              >', '<Button\n                className="shadow-[0_0_30px_oklch(0.646_0.222_41.116/0.4)] rounded-xl bg-[#f54900] text-orange-50 gap-2"\n                size="lg"\n                onClick={() => navigate("/upload")}\n              >')
    else:
        # Screens 2-6
        content = content.replace('<span>Dashboard</span>', '<span onClick={() => navigate("/dashboard")} className="cursor-pointer hover:text-white w-full h-full">Dashboard</span>')
        content = content.replace('<span>Analysis</span>', '<span onClick={() => navigate("/dashboard")} className="cursor-pointer hover:text-white w-full h-full">Analysis</span>')
        content = content.replace('<span>History</span>', '<span onClick={() => navigate("/history")} className="cursor-pointer hover:text-white w-full h-full">History</span>')
        content = content.replace('<span>Training</span>', '<span onClick={() => navigate("/training")} className="cursor-pointer hover:text-white w-full h-full">Training</span>')
        content = content.replace('<span>AI Coach</span>', '<span onClick={() => navigate("/coach")} className="cursor-pointer hover:text-white w-full h-full">AI Coach</span>')
        content = content.replace('<span>Profile</span>', '<span onClick={() => navigate("/profile")} className="cursor-pointer hover:text-white w-full h-full">Profile</span>')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Nav links fixed')
