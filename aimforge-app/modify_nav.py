import os
import re

pages = [
    'LandingPage.tsx',
    'Dashboard.tsx',
    'HistoryPage.tsx',
    'TrainingPlanPage.tsx',
    'AiCoachPage.tsx',
    'ProfilePage.tsx'
]

routes = {
    'Dashboard': '/dashboard',
    'Analysis': '/dashboard',
    'History': '/history',
    'Training': '/training',
    'AI Coach': '/coach',
    'Profile': '/profile'
}

for page in pages:
    path = os.path.join('src', 'pages', page)
    if not os.path.exists(path): continue
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add pointer cursor to buttons and nav divs
    for name, route in routes.items():
        # Match pattern where the element contains the text
        # e.g. <div className="... flex px-3 py-2 items-center gap-2"> \n <Icon className="size-4" /> \n <span>Dashboard</span>
        # We'll use regex to find the nearest opening tag <div  or <button  before the text.
        
        # Simple string replacement for specific elements (since it's mostly standardized)
        if name == 'Dashboard':
            content = re.sub(r'(<button[^>]*?)(\s*>[\s\S]*?Dashboard\s*</button>)', r'\1 onClick={() => navigate("/dashboard")} style={{cursor: "pointer"}}\2', content)
            content = re.sub(r'(<div[^>]*?)(\s*>[\s\S]*?<span>Dashboard</span>\s*</div>)', r'\1 onClick={() => navigate("/dashboard")} style={{cursor: "pointer"}}\2', content)
        elif name == 'Analysis':
            content = re.sub(r'(<button[^>]*?)(\s*>[\s\S]*?Analysis\s*</button>)', r'\1 onClick={() => navigate("/dashboard")} style={{cursor: "pointer"}}\2', content)
            content = re.sub(r'(<div[^>]*?)(\s*>[\s\S]*?<span>Analysis</span>\s*</div>)', r'\1 onClick={() => navigate("/dashboard")} style={{cursor: "pointer"}}\2', content)
        elif name == 'History':
            content = re.sub(r'(<button[^>]*?)(\s*>[\s\S]*?History\s*</button>)', r'\1 onClick={() => navigate("/history")} style={{cursor: "pointer"}}\2', content)
            content = re.sub(r'(<div[^>]*?)(\s*>[\s\S]*?<span>History</span>\s*</div>)', r'\1 onClick={() => navigate("/history")} style={{cursor: "pointer"}}\2', content)
        elif name == 'Training':
            content = re.sub(r'(<button[^>]*?)(\s*>[\s\S]*?Training\s*</button>)', r'\1 onClick={() => navigate("/training")} style={{cursor: "pointer"}}\2', content)
            content = re.sub(r'(<div[^>]*?)(\s*>[\s\S]*?<span>Training</span>\s*</div>)', r'\1 onClick={() => navigate("/training")} style={{cursor: "pointer"}}\2', content)
        elif name == 'AI Coach':
            content = re.sub(r'(<button[^>]*?)(\s*>[\s\S]*?AI Coach\s*</button>)', r'\1 onClick={() => navigate("/coach")} style={{cursor: "pointer"}}\2', content)
            content = re.sub(r'(<div[^>]*?)(\s*>[\s\S]*?<span>AI Coach</span>\s*</div>)', r'\1 onClick={() => navigate("/coach")} style={{cursor: "pointer"}}\2', content)
        elif name == 'Profile':
            content = re.sub(r'(<button[^>]*?)(\s*>[\s\S]*?Profile\s*</button>)', r'\1 onClick={() => navigate("/profile")} style={{cursor: "pointer"}}\2', content)
            content = re.sub(r'(<div[^>]*?)(\s*>[\s\S]*?<span>Profile</span>\s*</div>)', r'\1 onClick={() => navigate("/profile")} style={{cursor: "pointer"}}\2', content)

    # For LandingPage link to Dashboard on "Get Started" and "Upload Gameplay"
    content = content.replace('Get Started\n            </Button>', 'Get Started\n            </Button>').replace('<Button className="rounded-lg bg-[#f54900] text-orange-50">', '<Button className="rounded-lg bg-[#f54900] text-orange-50" onClick={() => navigate("/dashboard")}>')
    content = content.replace('<Button\n                className="shadow-[0_0_30px_oklch(0.646_0.222_41.116/0.4)] rounded-xl bg-[#f54900] text-orange-50 gap-2"\n                size="lg"\n              >\n                <Upload className="size-5" />\n                Upload Gameplay\n              </Button>', '<Button\n                className="shadow-[0_0_30px_oklch(0.646_0.222_41.116/0.4)] rounded-xl bg-[#f54900] text-orange-50 gap-2"\n                size="lg"\n                onClick={() => navigate("/upload")}\n              >\n                <Upload className="size-5" />\n                Upload Gameplay\n              </Button>')
    
    # Check if we didn't double-inject
    content = re.sub(r'(onClick=\{.*?\})\s*onClick=\{.*?\}', r'\1', content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Navigation updated.")
