from menu import menu, Inventory
from entity import load_char

inv = Inventory(20)
enm_inv = Inventory(5)

run = True

try:
    plr = load_char(inv)
except OSError:
    print("Character could not be loaded")
    run = False

while run:
    print("----MAIN MENU----")
    print("1. Inventory + Character Menu")
    print("2. Play (no existing)")

    user_choice = input("Enter your choice (1-2): ")
    if user_choice == "1":
        menu(plr)