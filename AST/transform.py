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
    
    def __init__(self, min_len=8, max_len=12):
        self.min_len = min_len
        self.max_len = max_len
        self._cache = set()
        self._counter = 0
    
    def generate(self):
        self._counter += 1
        
        if self._counter < 100:
            name = f"_{self._counter:02x}"
        else:
            length = random.randint(self.min_len, self.max_len)
            suffix = ''.join(random.choices(string.ascii_letters, k=length-4))
            name = f"_{self._counter:03x}{suffix}"
        
        while name in self._cache:
            name += random.choice(string.ascii_letters)
        
        self._cache.add(name)
        return name


class MultiPassObfuscator(ast.NodeTransformer):
    
    def __init__(self, strings=True, numbers=True, passes=1):
        self.names = {}
        self.strings = strings
        self.numbers = numbers
        self.generator = IdentifierGenerator()
        self.builtins = set(dir(builtins))
        self.imports = set()
        self.in_class = False
        self.passes = max(1, min(passes, 2))  

        self._transformed_strings = {}
        self._transformed_numbers = {}
        
        self._string_split_limit = 3  
        self._total_nodes = 0
        self._max_nodes = 1000000  # seceurity limit
    
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
            or name.startswith("_") 
        ):
            return name
        
        if name not in self.names:
            self.names[name] = self.generator.generate()
        
        return self.names[name]
    
    def visit_Module(self, node):
        self.generic_visit(node)
        
        if self.passes > 1 and self._total_nodes < 50000:
            self.generic_visit(node)
        
        return node
    
    def visit_ClassDef(self, node):
        node.name = self.rename(node.name)
        old_in_class = self.in_class
        self.in_class = True
        self.generic_visit(node)
        self.in_class = old_in_class
        return node
    
    def visit_FunctionDef(self, node):
        if not self.in_class or not node.name.startswith("__"):
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
        self._total_nodes += 1
        
        if self._total_nodes > self._max_nodes:
            return node
        
        if self.strings and isinstance(node.value, str):
            if len(node.value) <= 2:
                return node
            
            str_id = id(node.value)
            if str_id in self._transformed_strings:
                return self._transformed_strings[str_id]

            result = self._split_string_optimized(node.value)
            self._transformed_strings[str_id] = result
            return result
        
        if self.numbers and isinstance(node.value, int) and not isinstance(node.value, bool):
            if -10 <= node.value <= 10:
                return node
            
            num_id = node.value
            if num_id in self._transformed_numbers:
                return self._transformed_numbers[num_id]

            r = random.randint(5, 20)
            result = ast.BinOp(
                left=ast.Constant(node.value + r),
                op=ast.Sub(),
                right=ast.Constant(r)
            )
            self._transformed_numbers[num_id] = result
            return result
        
        return node
    
    def _split_string_optimized(self, s: str):

        max_splits = min(self._string_split_limit, len(s) // 10)
        
        if max_splits <= 1 or len(s) < 5:
            return ast.Constant(s)
        

        parts = []
        chunk_size = len(s) // max_splits
        
        for i in range(0, len(s), chunk_size):
            parts.append(s[i:i + chunk_size])
        
        if not parts:
            return ast.Constant(s)
        
        result = ast.Constant(parts[0])
        for part in parts[1:]:
            result = ast.BinOp(
                left=result,
                op=ast.Add(),
                right=ast.Constant(part)
            )
        
        return result


class ObfuscationEngine:
    
    def __init__(self, strings=True, numbers=True, passes=1):
        self.strings = strings
        self.numbers = numbers
        self.passes = passes
    
    def obfuscate(self, source: str) -> str:
   
        try:
            tree = ast.parse(source)
            
            node_count = sum(1 for _ in ast.walk(tree))
            
            if node_count > 10000:
                print(f"[INFO] Large file detected ({node_count} nodes), optimizing...")
                passes = 1
                strings = False if node_count > 50000 else self.strings
            else:
                passes = self.passes
                strings = self.strings
            
  
            obfuscator = MultiPassObfuscator(
                strings=strings,
                numbers=self.numbers,
                passes=passes
            )
            
            obfuscated_tree = obfuscator.visit(tree)
    
            ast.fix_missing_locations(obfuscated_tree)

            result = ast.unparse(obfuscated_tree)

            print(f"[INFO] Obfuscation complete:")
            print(f"  - {len(obfuscator.names)} identifiers renamed")
            print(f"  - {obfuscator._total_nodes} nodes processed")
            
            return result
            
        except RecursionError:
            print("[ERROR] File too complex, using minimal obfuscation...")
            return self._minimal_obfuscate(source)
        
        except Exception as e:
            print(f"[ERROR] Obfuscation failed: {e}")
            raise
    
    def _minimal_obfuscate(self, source: str) -> str:
        tree = ast.parse(source)

        obfuscator = MultiPassObfuscator(
            strings=False,
            numbers=False,
            passes=1
        )
        
        obfuscated_tree = obfuscator.visit(tree)
        ast.fix_missing_locations(obfuscated_tree)
        
        return ast.unparse(obfuscated_tree)
