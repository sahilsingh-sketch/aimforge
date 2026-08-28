import sys

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\pages\AiCoachPage.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

open_divs = content.count('<div')
close_divs = content.count('</div')

print(f'open: {open_divs}, close: {close_divs}')
if open_divs > close_divs:
    print('Adding closing divs')
    content = content.replace('  );\n}', '  </div>\n' * (open_divs - close_divs) + '  );\n}')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
