import os
path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\services\api.ts'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('";\\n\\nexport const', '";\n\nexport const')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
