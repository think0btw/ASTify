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
def generate_identifier(min_len=4, max_len=12):
    return "_" + "".join(
        random.choice(string.ascii_letters)
        for _ in range(random.randint(min_len, max_len))
    )


class NameObfuscator(ast.NodeTransformer):
    def __init__(self, obfuscate_strings=True, obfuscate_numbers=True):
        self.name_map = {}
        self.builtins = set(dir(__builtins__))
        self.obfuscate_strings = obfuscate_strings
        self.obfuscate_numbers = obfuscate_numbers

    def map_name(self, name: str) -> str:
        if name in self.builtins:
            return name
        if name not in self.name_map:
            self.name_map[name] = generate_identifier()
        return self.name_map[name]

    def visit_Name(self, node):
        return ast.copy_location(
            ast.Name(id=self.map_name(node.id), ctx=node.ctx),
            node
        )

    def visit_FunctionDef(self, node):
        node.name = self.map_name(node.name)
        node.args = self.visit(node.args)
        node.body = [self.visit(n) for n in node.body]
        return node

    def visit_arg(self, node):
        node.arg = self.map_name(node.arg)
        return node

    def visit_Constant(self, node):
        
        # ---- STRING ----
        if (
            self.obfuscate_strings
            and isinstance(node.value, str)
            and len(node.value) > 1
        ):
            i = random.randint(1, len(node.value) - 1)
            return ast.BinOp(
                left=ast.Constant(node.value[:i]),
                right=ast.Constant(node.value[i:]),
                op=ast.Add()
            )

        # ---- NUMBER ----
        if (
            self.obfuscate_numbers
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


def obfuscate_source(source_code: str, strings=True, numbers=True) -> str:
    tree = ast.parse(source_code)
    transformer = NameObfuscator(
        obfuscate_strings=strings,
        obfuscate_numbers=numbers
    )
    tree = transformer.visit(tree)
    ast.fix_missing_locations(tree)
    return ast.unparse(tree)
