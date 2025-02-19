from entity import Entity
from inventory import Item

def secret_menu(plr: Entity):
    print("----CHEATER MENU----")
    print("1. Add an item to inventory")
    print("2. Add or remove quantity from an item")
    print("")

    user_choice = input("Enter your choice (1-2): ")

    if user_choice == "1":
        item_name = input("Enter the name of the item: ")
        item_location = input("Enter the spot you would like your item to be in (0-{}): ".format(plr.inv.max_slots))
        stacking = input("Would you like this item to be stackable? (Y/N): ")
        damage = input("Enter the damage of the item: ")
        healing = input("Can this item heal? (Y/N): ")

        if item_location.isdigit() and damage.isdigit():
            item_location = int(item_location)
            if stacking.upper() == "Y":
                max_stack = input("Enter the max number of times this item can be stacked: ")
                stacking = True
            else:
                max_stack = "0"
                stacking = False
            if healing.upper() == "Y":
                healing_amt = input("Enter the amount you want this item to heal for: ")
                healing = True
            else:
                healing_amt = "0"
                healing = False
            if not item_location > plr.inv.max_slots and not item_location < 0 and not item_location in plr.inv.inventory.keys() and max_stack.isdigit() and healing_amt.isdigit():
                max_stack = int(max_stack)
                healing_amt = int(healing_amt)
                damage = int(damage)
                item = Item(item_name, item_location, stacking, max_stack, 1, damage, healing, healing_amt)
                result = plr.inv.add_to_inv(item)
                if result == -1:
                    print("Inventory full")
                plr.save()
            else:
                print("The item_location is out of range or max range and healing amount are not integers")
        else:
            print("Your location and damage must be integers")

    elif user_choice == "2":
        item_name = input("Enter the name of the item: ")
        user_choice = input("Add or Remove quantity (A/R): ")

        if user_choice.upper() == "A":
            item = plr.inv.find_item(item_name)
            if item != -1:
                add_amt = input("How much would you like to add to {}? (Max: {}): ".format(item.name, (
                            item.max_stack - item.current_amt)))
                if add_amt.isdigit():
                    add_amt = int(add_amt)
                    res = item.add_to_stack(add_amt)
                    if res == 1:
                        plr.save()
                    else:
                        print("Unable to add to quantity")
                else:
                    print("The amount must be an integer")
            else:
                print("The item was not found")

        if user_choice.upper() == "R":
            item = plr.inv.find_item(item_name)
            if item != -1:
                rmv_amt = input(
                    "How much would you like to remove from {}? (Max: {}): ".format(item.name, (item.current_amt - 1)))
                if rmv_amt.isdigit():
                    rmv_amt = int(rmv_amt)
                    res = item.remove_from_stack(rmv_amt)
                    if res == 1:
                        plr.save()
                    else:
                        print("Unable to remove from quantity")
                else:
                    print("The amount must be an integer")
            else:
                print("The item was not found")