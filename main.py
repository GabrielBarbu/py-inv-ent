from menu import menu, Inventory
from entity import load_char
from inventory import Item

inv = Inventory(20)
enm_inv = Inventory(5)

run = True

try:
    plr = load_char(inv)
except OSError:
    print("Character could not be loaded")
    run = False

if __name__ == "__main__":
    while run:
        game_run = True
        print("----MAIN MENU----")
        print("1. Inventory + Character Menu")
        print("2. Play")

        user_choice = input("Enter your choice (1-2): ")
        if user_choice == "1":
            menu(plr)
        elif user_choice == "2":
            #Basic concept of a game, lots of room for improvement
            while game_run:
                print("You are in a forest. There is a conveniently placed wooden sword on the ground")
                print("")

                user_choice = input(": ")

                if user_choice.lower() == "pickup sword":
                    item_location = input("Enter where you would like to place the wooden sword ({}-{}): ".format(0,plr.inv.max_slots))
                    if item_location.isdigit():
                        item_location = int(item_location)
                        if not item_location > plr.inv.max_slots and not item_location < 0 and not item_location in plr.inv.inventory.keys():
                            item = Item("Wooden Sword", item_location, False, 1, 1, 10, False, 0)
                            result = plr.inv.add_to_inv(item)
                            if result == -1:
                                print("Inventory full")
                            else:
                                print("You have picked up {}".format(item.name))
                                plr.save()
                        else:
                            print("The item location is out of range or there is something already there")
                    else:
                        print("Your location must be an integer")

                elif user_choice.lower() == "menu":
                    menu(plr)