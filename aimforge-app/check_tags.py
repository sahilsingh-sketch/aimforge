import os
import re

def check_balance(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the main return block
    # We will just do a simple tag stack for the return block
    match = re.search(r'return\s*\(\s*(<div.*)', content, re.DOTALL)
    if not match:
        print(f"No return block found in {filepath}")
        return

    jsx = match.group(1)
    
    # We want to match all <div...> and </div> and <ComingSoonModal... /> etc
    # Actually, simpler: we can just count opening <div (without closing />) and closing </div>
    # But wait, self-closing divs don't exist usually, but other tags do.
    # Let's write a simple HTML parser logic to find the first extra closing tag or unclosed tags.
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'return (' in line:
            start_line = i
            break
    else:
        start_line = 0
        
    stack = []
    
    # regex to find tags
    tag_pattern = re.compile(r'</?([a-zA-Z0-9]+)[^>]*>')
    
    for i, line in enumerate(lines[start_line:], start=start_line+1):
        # strip comments
        line_clean = re.sub(r'\{/\*.*?\*/\}', '', line)
        
        for m in tag_pattern.finditer(line_clean):
            tag_text = m.group(0)
            tag_name = m.group(1)
            
            if tag_text.endswith('/>'):
                continue # self closing
            
            if tag_text.startswith('</'):
                if not stack:
                    print(f"{os.path.basename(filepath)}: EXTRA CLOSING TAG at line {i}: {tag_text}")
                    return
                top = stack.pop()
                if top[0] != tag_name:
                    print(f"{os.path.basename(filepath)}: MISMATCH at line {i}. Expected </{top[0]}> but got {tag_text}. Open tag was at line {top[1]}")
            else:
                stack.append((tag_name, i))

    if stack:
        print(f"{os.path.basename(filepath)}: UNCLOSED TAGS: {stack}")
    else:
        print(f"{os.path.basename(filepath)}: OK")

def main():
    pages_dir = r"c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\pages"
    for filename in os.listdir(pages_dir):
        if filename.endswith('.tsx'):
            filepath = os.path.join(pages_dir, filename)
            check_balance(filepath)

if __name__ == "__main__":
    main()
