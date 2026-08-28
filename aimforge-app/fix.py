import os
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the main return block
    match = re.search(r'return\s*\(\s*(<div.*)', content, re.DOTALL)
    if not match:
        return False
        
    start_pos = match.start(1)
    
    # Simple tag balancer
    open_divs = 0
    lines = content.split('\n')
    
    in_return = False
    new_lines = []
    
    for i, line in enumerate(lines):
        if 'return (' in line:
            in_return = True
            new_lines.append(line)
            continue
            
        if not in_return:
            new_lines.append(line)
            continue
            
        # Count open divs
        # This is a heuristic, assuming <div and </div> are well formed and on separate lines
        open_count = len(re.findall(r'<div\b[^>]*>', line))
        close_count = len(re.findall(r'</div>', line))
        
        # If we have a single </div> and we are at 0 open divs, it's extra!
        if close_count > 0 and open_divs + open_count - close_count < 0:
            # We found an extra </div>!
            # Let's remove one </div> from this line
            print(f"Removing extra </div> from {filepath} at line {i+1}")
            line = re.sub(r'^\s*</div>\s*$', '', line)
            if not line.strip():
                # Line is now empty, we can skip it
                pass
            else:
                new_lines.append(line)
            # We don't change open_divs since we ignored the extra close
            # But wait, what if there are multiple? Let's just do it manually.
            pass
            
    # Actually, a better approach is to just run a quick script that removes one </div> near the end of the file
    pass

