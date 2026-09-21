import io
import ast
import re

with io.open('app/data/worlds_data.py', 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

# Parse the file as AST
tree = ast.parse(content)

# Find all _debug calls with 4 positional args
class DebugFixer(ast.NodeVisitor):
    def __init__(self):
        self.replacements = []
    
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == '_debug':
            args = node.args
            keywords = node.keywords
            
            has_fix_steps = any(kw.arg == 'fix_steps' for kw in keywords)
            
            if not has_fix_steps and len(args) == 4:
                # Get the line content
                lineno = node.lineno - 1  # 0-indexed
                line = lines[lineno]
                
                # Extract the 4 arguments
                prompt_arg = ast.unparse(args[0])
                buggy_arg = ast.unparse(args[1])
                fix_steps_arg = ast.unparse(args[2])
                answer_arg = ast.unparse(args[3])
                
                # Build new call
                new_call = f'_debug({prompt_arg}, {buggy_arg}, fix_steps=[{fix_steps_arg}], answer={answer_arg})'
                
                self.replacements.append((lineno, line, new_call))
        
        self.generic_visit(node)

fixer = DebugFixer()
fixer.visit(tree)

print(f'Found {len(fixer.replacements)} calls to fix')

# Apply replacements in reverse order to preserve line numbers
for lineno, old_line, new_call in reversed(fixer.replacements):
    # Find the exact line and replace it
    # The _debug call might span multiple lines, so we need to find the full call
    # For simplicity, replace the entire line if it starts with _debug
    if lines[lineno].strip().startswith('_debug('):
        lines[lineno] = lines[lineno].replace(lines[lineno].strip(), new_call)
        print(f'Fixed line {lineno+1}')

new_content = '\n'.join(lines)

with io.open('app/data/worlds_data.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Done')
