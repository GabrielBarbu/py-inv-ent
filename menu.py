from entity import Entity, Inventory
from cheat_menu import cheat_menu


def menu(plr: Entity):
    """Runs the menu

    Args:
        plr (Entity): Player class
    """

    run = True

    while run:
        run2 = True
        print("----INVENTORY MENU----")
        print("1. View stats of items in inventory")
        print("2. Remove an item from inventory")
        print("3. Equip or Unequip an item")
        print("4. Move an item to another slot")
        print("5. View character menu")
        print("6. Exit Menu")
        print("")

        user_choice = input("Enter your choice (1-5): ")

        if user_choice == "1":
            for i in plr.inv.inventory.values():
                print("Name: {} Slot: {} Amount: {} Damage: {} Healing: {}".format(i.name, i.location, i.current_amt,
                                                                                   i.damage, i.healing_amt))

        elif user_choice == "2":
            item_name = input("Enter the name of the item: ")

            item = plr.inv.find_item(item_name)
            if item != -1:
                item_location = int(item.location)
                confirmation = input(
                    "The item you are deleting is {} are you sure you wish to continue? (Y/N): ".format(item.name))
                if confirmation.upper() == "Y":
                    plr.inv.remove_from_inv(item_location)
                    plr.save()
            else:
                print("The item was not found")

        elif user_choice == "3":
            user_choice = input("Equip or Unequip (E/U): ")

            if user_choice.upper() == "E":
                item_name = input("Enter the name of the item: ")
                result = plr.equip_item(item_name)
                if result == 1:
                    print("{} has been equipped".format(item_name))
                    plr.save()
                else:
                    print("The item does not exist or something is already equipped")
            elif user_choice.upper() == "U":
                item_name = input("Enter the name of the item: ")
                result = plr.unequip_item(item_name)
                if result == 1:
                    print("{} has been unequipped".format(item_name))
                    plr.save()
                else:
                    print("The item does not exist or it is not equipped")
            else:
                print("That is not a choice")

        elif user_choice == "4":
            item_name = input("Enter the name of the item: ")
            new_location = input("Enter the new location for the item: ")

            if new_location.isdigit():
                new_location = int(new_location)
                if not new_location > plr.inv.max_slots and not new_location < 0 and not new_location in plr.inv.inventory.keys():
                    result = plr.inv.move_item(item_name, new_location)
                    if result == 1:
                        print("{} has been moved to slot {}".format(item_name, new_location))
                        plr.save()
                    else:
                        print("This item could not be moved")
                else:
                    print("The item location is out of range or there is something already there")
            else:
                print("The new location must be an integer")

        elif user_choice == "5":
            while run2:
                print("----CHARACTER MENU----")
                print("1. View character stats")
                print("2. Use an item")
                print("")

                user_choice = input("Enter your choice: ")

                if user_choice == "1":
                    print("Name:", plr.name)
                    print("Health:", plr.health)
                    print("Current damage:", plr.real_dmg)
                    print("Currently equipped item:", plr.equipped_item)

                elif user_choice == "2":
                    item_name = input("Enter the name of the item you wish to use: ")
                    result = plr.use_item(item_name)
                    if result == 1:
                        print("You have used {} to heal {} hp".format(item_name,
                                                                      plr.inv.find_item(item_name).healing_amt))
                        plr.save()
                    else:
                        print("This item does not exist or could not be used")
                run2 = False

        elif user_choice == "6":
            break

        elif user_choice == "iamacheater":
            cheat_menu(plr)