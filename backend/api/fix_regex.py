
import re
try:
    with open('main.py', 'rb') as f:
        content = f.read().decode('utf-8', 'ignore')
    
    # Replace triple quoted strings with a comment
    # We use a non-greedy match .*? and DOTALL flag to match across newlines
    fixed_content = re.sub(r'""".*?"""', '# docstring removed', content, flags=re.DOTALL)
    
    with open('main_final.py', 'w', encoding='utf-8') as f:
        f.write(fixed_content)
        
    print("Successfully created main_final.py")
except Exception as e:
    print(f"Error: {e}")
