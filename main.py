import os
from colorama import Fore, Style, init
from AST.transform import ObfuscationEngine
init()

def clear():    
    os.system('cls' if os.name == 'nt' else 'clear')


def color(text):
    result = ""
    r, g, b = 170, 0, 255
    up = True

    for line in text.splitlines():
        for char in line:
            if up:
                g += 3
                if g >= 180:
                    up = False
            else:
                g -= 2
                if g <= 40:
                    up = True

            result += f"\033[38;2;{r};{g};{b}m{char}\033[0m"
        result += "\n" 

    return result


banner = color(r"""
⠀⠀⠀⠀⠀⠀⢀⣤⣶⣶⣖⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣾⡟⣉⣽⣿⢿⡿⣿⣿⣆⠀⠀⠀  _____ _____ _____ _ ___     
⠀⠀⠀⢠⣿⣿⣿⡗⠋⠙⡿⣷⢌⣿⣿⠀⠀⠀ |  _  |   __|_   _|_|  _|_ _ 
⣷⣄⣀⣿⣿⣿⣿⣷⣦⣤⣾⣿⣿⣿⡿⠀⠀⠀ |     |__   | | | | |  _| | |
⠈⠙⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⢀ |__|__|_____| |_| |_|_| |_  |
⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠻⠿⠿⠋                        |___|
⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀  ~ By think0btw 
⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⡄  ~ v1.0
⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⢀⡾⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣷⣶⣴⣾⠏⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠛⠛⠋⠁⠀⠀⠀""")


def enter():
    engine = ObfuscationEngine()

    while True:
        prompt = (
            Fore.LIGHTMAGENTA_EX + "┌─[" +
            Fore.WHITE + "ASTify" +
            Fore.LIGHTMAGENTA_EX + "]─" +
            Fore.LIGHTMAGENTA_EX + "(" +
            Fore.WHITE + "~/Main" +
            Fore.LIGHTMAGENTA_EX + ")" + "\n" +
            Fore.LIGHTMAGENTA_EX + "└─" +
            Fore.WHITE + "$ " +
            Fore.LIGHTMAGENTA_EX + "File ➜ "
        )

        path = input(prompt).strip().strip('"').strip("'")
        if not (path.lower().endswith(".py") and os.path.isfile(path)):
            print(Fore.RED + "Invalid Python file")
            continue
        print(Fore.GREEN + "File accepted")
        
        with open(path, "r", encoding="utf-8") as f:
            source = f.read()

        obfuscated = engine.obfuscate(source)

        out_name = input(
            Fore.LIGHTMAGENTA_EX + "Output file name ➜ " + Fore.WHITE
        ).strip()
        
        if not out_name:
            out_name = path.replace(".py", "_obf.py")
        if not out_name.lower().endswith(".py"):
            out_name += ".py"

        with open(out_name, "w", encoding="utf-8") as f:
            f.write(obfuscated)

        print(Fore.GREEN + f"Saved → {out_name}")

if __name__ == "__main__":
    clear()
    print(banner)
    enter()
    
