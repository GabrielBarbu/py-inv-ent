from menu import menu, create_character, Inventory, Entity

inv = Inventory(20)
enm_inv = Inventory(5)

try:
    with open("char.txt", "r") as file:
        char = [line.strip().split(',') for line in file]
        for char_data in char:
            name = char_data[0]
            health = int(char_data[1])
            base_dmg = int(char_data[2])
            equipped_item = char_data[3]
            plr = Entity(inv, name, health, base_dmg, equipped_item)
        inv.load_from_file()
except OSError:
    temp_run = True

    while temp_run:
        char_name = input("Enter the name of your character: ")
        char_health = input("Enter the health of your character: ")
        char_base_dmg = input("Enter the base damage of your character: ")
        plr = create_character(inv, char_name, char_health, char_base_dmg)
        if plr == -1:
            print("The health and damage must be integers")
        else:
            print("Character {} created".format(char_name))
            plr.save()
            temp_run = False

run = True

while run:
    print("----MAIN MENU----")
    print("1. Inventory + Character Menu")
    print("2. Play (no existing)")

    user_choice = input("Enter your choice (1-2): ")
    if user_choice == "1":
        menu(plr)