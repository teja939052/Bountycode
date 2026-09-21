import io
import ast

with io.open('app/data/worlds_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Parse the file as AST to find all _debug calls
tree = ast.parse(content)

# Find all _debug function calls
class DebugFinder(ast.NodeVisitor):
    def __init__(self):
        self.debug_calls = []
    
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == '_debug':
            self.debug_calls.append(node)
        self.generic_visit(node)

finder = DebugFinder()
finder.visit(tree)

print(f'Found {len(finder.debug_calls)} _debug calls')

# Check which ones have 4 positional args without fix_steps keyword
for call in finder.debug_calls:
    args = call.args
    keywords = call.keywords
    
    # Check if fix_steps is already a keyword
    has_fix_steps = any(kw.arg == 'fix_steps' for kw in keywords)
    
    if not has_fix_steps and len(args) == 4:
        # Get line number
        lineno = call.lineno
        print(f'Line {lineno}: 4 positional args, needs fix_steps=[...]')
