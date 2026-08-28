import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend\core\config.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('def DATABASE_URI(self) -> str:', 'def DATABASE_URI(self) -> str:\n        return "sqlite:///./test.db"\n        #')
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
