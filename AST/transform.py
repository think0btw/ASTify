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
class IdentifierGenerator:
    def __init__(self, min_len=4, max_len=12):
        self.min_len = min_len
        self.max_len = max_len

    def generate(self):
        return "_" + "".join(
            random.choice(string.ascii_letters)
            for _ in range(random.randint(self.min_len, self.max_len))
        )

class Obfuscator(ast.NodeTransformer):
    def __init__(self, strings=True, numbers=True):
        self.names = {}
        self.builtins = set(dir(__builtins__))
        self.strings = strings
        self.numbers = numbers
        self.gen = IdentifierGenerator()

    # ---- Names ----
    def rename(self, name: str) -> str:
        if name in self.builtins:
            return name
        if name not in self.names:
            self.names[name] = self.gen.generate()
        return self.names[name]

    def visit_Name(self, node):
        return ast.copy_location(
            ast.Name(id=self.rename(node.id), ctx=node.ctx),
            node
        )

    def visit_arg(self, node):
        node.arg = self.rename(node.arg)
        return node

    def visit_FunctionDef(self, node):
        node.name = self.rename(node.name)
        self.generic_visit(node)
        return node

    def visit_Constant(self, node):

        # strings
        if (
            self.strings
            and isinstance(node.value, str)
            and len(node.value) > 1
        ):
            cut = random.randint(1, len(node.value) - 1)
            return ast.BinOp(
                left=ast.Constant(node.value[:cut]),
                right=ast.Constant(node.value[cut:]),
                op=ast.Add()
            )

        # numbers
        if (
            self.numbers
            and isinstance(node.value, (int, float))
            and not isinstance(node.value, bool)
        ):
            offset = random.randint(1, 10)
            return ast.BinOp(
                left=ast.Constant(node.value + offset),
                right=ast.Constant(offset),
                op=ast.Sub()
            )

        return node

class ObfuscationEngine:
    def __init__(self, strings=True, numbers=True):
        self.strings = strings
        self.numbers = numbers

    def obfuscate(self, source: str) -> str:
        tree = ast.parse(source)
        tree = Obfuscator(
            strings=self.strings,
            numbers=self.numbers
        ).visit(tree)
        ast.fix_missing_locations(tree)
        return ast.unparse(tree)
