import ast
import random
import string
import builtins

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
    def __init__(self, min_len=10, max_len=18):
        self.min_len = min_len
        self.max_len = max_len

    def generate(self):
        return "_" + "".join(
            random.choice(string.ascii_letters)
            for _ in range(random.randint(self.min_len, self.max_len))
        )
class MultiPassObfuscator(ast.NodeTransformer):
    def __init__(self, strings=True, numbers=True, passes=3):
        self.names = {}
        self.strings = strings
        self.numbers = numbers
        self.generators = IdentifierGenerator()
        self.builtins = set(dir(builtins))
        self.imports = set()
        self.in_class = False
        self.passes = passes

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.asname or alias.name)
        return node

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.imports.add(alias.asname or alias.name)
        return node

    def rename(self, name: str) -> str:
        if (
            name in self.builtins
            or name in self.imports
            or name.startswith("__")
        ):
            return name

        if name not in self.names:
            self.names[name] = self.generators.generate()

        return self.names[name]

    def visit_Module(self, node):
        for _ in range(self.passes):
            self.generic_visit(node)
        return node

    def visit_ClassDef(self, node):
        node.name = self.rename(node.name)
        self.in_class = True
        self.generic_visit(node)
        self.in_class = False
        return node

    def visit_FunctionDef(self, node):
     
        if not self.in_class:
            node.name = self.rename(node.name)
        self.generic_visit(node)
        return node

    def visit_arg(self, node):
        node.arg = self.rename(node.arg)
        return node

    def visit_Name(self, node):
        node.id = self.rename(node.id)
        return node

    def visit_Attribute(self, node):
        self.generic_visit(node)
        return node

    def visit_Constant(self, node):

        if self.strings and isinstance(node.value, str) and len(node.value) > 1:
            i = random.randint(1, len(node.value) - 1)
            return ast.BinOp(
                left=ast.Constant(node.value[:i]),
                op=ast.Add(),
                right=ast.Constant(node.value[i:])
            )

        if self.numbers and isinstance(node.value, int) and not isinstance(node.value, bool):
            r = random.randint(10, 50)
            return ast.BinOp(
                left=ast.Constant(node.value + r),
                op=ast.Sub(),
                right=ast.Constant(r)
            )

        return node

class ObfuscationEngine:
    def __init__(self, strings=True, numbers=True, passes=2):
        self.strings = strings
        self.numbers = numbers
        self.passes = passes

    def obfuscate(self, source: str) -> str:
        tree = ast.parse(source)
        obf = MultiPassObfuscator(
            self.strings,
            self.numbers,
            self.passes
        ).visit(tree)
        ast.fix_missing_locations(obf)
        return ast.unparse(obf)
