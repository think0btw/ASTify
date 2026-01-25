import os
from colorama import Fore, Style, init

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

        if path.lower().endswith(".py") and os.path.isfile(path):
            print(Fore.GREEN + "File accepted")
        else:
            print(Fore.RED + "Invalid Python file")
    
def main():
    clear()
    print(banner)
    enter()

if __name__ == "__main__":
    main()
    
