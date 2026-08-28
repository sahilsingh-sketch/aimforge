import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend\requirements.txt'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'paddleocr' not in content:
    content += '\npaddlepaddle==2.6.1\npaddleocr==2.7.3\n'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
