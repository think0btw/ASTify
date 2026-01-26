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
        self.strings = strings
        self.numbers = numbers
        self.gen = IdentifierGenerator()

        self.builtins = set(dir(builtins))
        self.imports = set()

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.asname or alias.name)
        return node

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.imports.add(alias.asname or alias.name)
        return node

def rename(self, name):
    if name.startswith("__") and name.endswith("__"):
        return name
    if name in self.builtins:
        return name
    if name in self.imports:
        return name
    if name not in self.names:
        self.names[name] = self.gen.generate()
    return self.names[name]


    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            if node.id in self.builtins or node.id in self.imports:
                return node

        node.id = self.rename(node.id)
        return node

    def visit_arg(self, node):
        node.arg = self.rename(node.arg)
        return node

    def visit_FunctionDef(self, node):
        node.name = self.rename(node.name)
        self.generic_visit(node)
        return node
    
    def visit_ClassDef(self, node):
      node.name = self.rename(node.name)
      self.generic_visit(node)
      return node

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in self.builtins or node.func.id in self.imports:
                return self.generic_visit(node)

        self.generic_visit(node)
        return node

    def visit_Constant(self, node):
        if self.strings and isinstance(node.value, str) and len(node.value) > 1:
            cut = random.randint(1, len(node.value) - 1)
            new_node = ast.BinOp(
                left=ast.Constant(node.value[:cut]),
                right=ast.Constant(node.value[cut:]),
                op=ast.Add()
            )
            return ast.copy_location(new_node, node)

        if self.numbers and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            offset = random.randint(1, 10)
            new_node = ast.BinOp(
                left=ast.Constant(node.value + offset),
                right=ast.Constant(offset),
                op=ast.Sub()
            )
            return ast.copy_location(new_node, node)

        return node


class ObfuscationEngine:
    def __init__(self, strings=True, numbers=True):
        self.strings = strings
        self.numbers = numbers

    def obfuscate(self, source: str) -> str:
        tree = ast.parse(source)
        tree = Obfuscator(self.strings, self.numbers).visit(tree)
        ast.fix_missing_locations(tree)
        return ast.unparse(tree)
