import command
from backend import configInit
from get import dataInit

from colorama import Fore, Back, Style


def main():
    configInit()
    # dataInit()
    print(
        f"""{Fore.YELLOW}"Welcome to "{Fore.MAGENTA}"JBPhiSystem"{Fore.RESET}.
This is the 0.1 verson.
"""
    )
    while 1:
        RawCommand = input(Fore.YELLOW + "JBPhiSystem>> " + Fore.RESET)
        Status = command.Command(RawCommand)
        if Status == "EX":
            break
        elif Status == "NF":
            print(Fore.RED + "Command not found" + Fore.RESET)
    print(Fore.YELLOW + "Thanks for using." + Fore.RESET)


main()
