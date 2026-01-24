
try:
    with open('main.py', 'rb') as f:
        content = f.read().decode('utf-8', 'ignore')
    
    lines = content.splitlines()
    new_lines = []
    skip = False
    
    for line in lines:
        stripped = line.strip()
        # Single line docstring
        if '"""' in stripped and stripped.count('"""') >= 2:
            # Replace with comment if it looks like a docstring line
            if stripped.startswith('"""') and stripped.endswith('"""'):
                new_lines.append(line.replace('"""', '# '))
            else:
                new_lines.append(line)
            continue
            
        # Multi-line docstring start/end
        if '"""' in stripped:
            if not skip:
                skip = True
                new_lines.append('# ' + line.replace('"""', ''))
            else:
                skip = False
                new_lines.append('# ' + line.replace('"""', ''))
            continue
            
        if not skip:
            new_lines.append(line)
        else:
            new_lines.append('# ' + line)
            
    with open('main_nuclear.py', 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
        
    print("Successfully created main_nuclear.py")
except Exception as e:
    print(f"Error: {e}")
