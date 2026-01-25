import ast
import random
import string
"""
╔═╗╔═╗╔╦╗                  
╠═╣╚═╗ ║                   
╩ ╩╚═╝ ╩                   
┌┬┐┬─┐┌─┐┌┐┌┌─┐┌─┐┌─┐┬─┐┌┬┐
 │ ├┬┘├─┤│││└─┐├┤ │ │├┬┘│││
 ┴ ┴└─┴ ┴┘└┘└─┘└  └─┘┴└─┴ ┴

-- By think0btw --

"""
# Random name gen
def rand_name(min_len=0, max_len=10):
    return "_" + "".join(
        random.choice(string.ascii_letters)
        for _ in range(random.randint(min_len, max_len))
    )

class SimpleObfuscator(ast.NodeTransformer):
    def __init__(self):
        self.names = {}
        self.builtins = set(dir(__builtins__))

    def obf_name(self, name):
        if name in self.builtins:
            return name
        if name not in self.names:
            self.names[name] = rand_name()
        return self.names[name]
    
    def visit_Name(self, node):
        return ast.copy_location(
            ast.Name(
                id=self.obf_name(node.id),
                ctx=node.ctx
            ),
            node
        )
    def visit_FunctionDef(self, node):
        node.name = self.obf_name(node.name)
        node.args = self.visit(node.args)
        node.body = [self.visit(n) for n in node.body]
        return node

    def visit_arg(self, node):
        node.arg = self.obf_name(node.arg)
        return node

    # Strings → "abc" became "a" + "bc" --> you can change it to other obfuscation methods
    def visit_Constant(self, node):
        if isinstance(node.value, str) and len(node.value) > 1:
            i = random.randint(1, len(node.value) - 1)
            return ast.BinOp(
                left=ast.Constant(node.value[:i]),
                right=ast.Constant(node.value[i:]),
                op=ast.Add()
            )
        return node


def obfuscate(source_code: str) -> str:
    tree = ast.parse(source_code)
    tree = SimpleObfuscator().visit(tree)
    ast.fix_missing_locations(tree)
    return ast.unparse(tree)
