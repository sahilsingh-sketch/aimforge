import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\pages\AiCoachPage.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('const { chatHistory, addChatMessage } = useAppStore();', 'const { chatHistory, addChatMessage, analysis } = useAppStore();')
content = content.replace('await aimforgeService.sendChatMessage(msg, chatHistory);', 'await aimforgeService.sendChatMessage(msg, chatHistory, analysis || undefined);')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated AiCoachPage to pass analysis context')
