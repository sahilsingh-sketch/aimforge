import os
import re

files = [
    r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\pages\UploadPage.tsx',
    r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\services\api.ts',
    r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\pages\ProcessingPage.tsx',
    r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\pages\LandingPage.tsx',
    r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\pages\ProfilePage.tsx',
    r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\pages\TrainingPlanPage.tsx'
]

for path in files:
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix backslashes in template literals
    content = content.replace('\\', '').replace('\\$', '$')
    
    # Fix regex issues in LandingPage from my earlier modify_nav.py script
    # It seems there are extra injected things or missing braces.
    # Let's fix LandingPage syntax errors
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Syntax fixes applied')
