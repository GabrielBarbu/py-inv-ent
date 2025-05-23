import tkinter.simpledialog
from tkinter import *
from tkinter import ttk
from entity import Entity
from inventory import Item


def cheat_menu(plr: Entity):
    """Opens the cheat menu in a new window"""
    cheat_window = Toplevel()
    cheat_window.title("Cheater Menu")

    ttk.Label(cheat_window, text="----CHEATER MENU----").grid(column=0, row=0)

    def open_char_cheat_menu():
        """Runs the character cheat menu """
        char_window = Toplevel()
        char_window.title("Character Menu")

        ttk.Label(char_window, text="----CHARACTER MENU----").grid(column=0, row=0)

        def view_stats():
            stats_text = (f"Name: {plr.name}\n"
                          f"Health: {plr.health}\n"
                          f"Max Health: {plr.max_health}\n"
                          f"Armour: {plr.armour}\n"
                          f"Current Damage: {plr.real_dmg}\n"
                          f"Currently Equipped: {plr.equipped_item}\n"
                          f"Torso Armour: {plr.torso}\n"
                          f"Legs Armour: {plr.legs}\n"
                          f"Head Armour: {plr.head}\n"
                          f"Feet Armour: {plr.feet}"
                          )
            stats_label.config(text=stats_text)

        def modify_health():
            health = tkinter.simpledialog.askinteger("Health Modification", "Enter new health:", parent=char_window)
            if health < 1:
                stats_label.config(text="Incorrect health")
            else:
                plr.health = health

        stats_label = Label(char_window, text="", wraplength=300, justify="left")
        stats_label.grid(column=0, row=3)

        ttk.Button(char_window, text="View Character Stats", command=view_stats).grid(column=0, row=1)
        ttk.Button(char_window, text="Modify Health", command=modify_health).grid(column=0, row=2)
        ttk.Button(char_window, text="Close", command=char_window.destroy).grid(column=0, row=4)

    def add_item():
        item_name = tkinter.simpledialog.askstring("Add Item", "Enter the name of the item:", parent=cheat_window)
        item_location = tkinter.simpledialog.askinteger("Item Location", f"Enter the spot (0-{plr.inv.max_slots}):",
                                                        parent=cheat_window)
        stacking = tkinter.simpledialog.askstring("Stackable?", "Should this item be stackable? (Y/N):",
                                                  parent=cheat_window)
        damage = tkinter.simpledialog.askinteger("Item Damage", "Enter the damage of the item:", parent=cheat_window)

        if stacking and stacking.upper() == "Y":
            max_stack = tkinter.simpledialog.askinteger("Max Stack", "Enter the max stack count:", parent=cheat_window)
            stacking = True
        else:
            max_stack = 0
            stacking = False

        healing = tkinter.simpledialog.askstring("Healing Item?", "Can this item heal? (Y/N):", parent=cheat_window)
        if healing and healing.upper() == "Y":
            healing_amt = tkinter.simpledialog.askinteger("Healing Amount", "Enter healing amount:",
                                                          parent=cheat_window)
            healing = True
        else:
            healing_amt = 0
            healing = False

        max_healing = tkinter.simpledialog.askstring("Max Healing", "Does this item increase the max health (Y/N):", parent=cheat_window)
        if max_healing and max_healing.upper() == "Y":
            max_heal_amt = tkinter.simpledialog.askinteger("Max Heal", "Enter the max heal amount:", parent=cheat_window)
            max_healing = True
        else:
            max_heal_amt = 0
            max_healing = False

        armour_inc = tkinter.simpledialog.askstring("Armour Increase", "Does this item increase the armour (Y/N):", parent=cheat_window)
        if armour_inc and armour_inc.upper() == "Y":
            armour_inc_amt = tkinter.simpledialog.askfloat("Armour Increase Amount", "Enter the armour increase amount:", parent=cheat_window)
            armour_inc = True
            armour_types = ["Legs", "Torso", "Head", "Feet"]
            armour_type = tkinter.simpledialog.askstring("Type of Armour", "Type of Armour (Legs, Torso, Head, Feet):")
            for i in armour_types:
                if i not in armour_type:
                    result_label.config(text="Invalid Armour Type")
                else:
                    armour_type = armour_type.lower()
        else:
            armour_inc_amt = 0
            armour_inc = False
            armour_type = "None"

        if 0 <= item_location <= plr.inv.max_slots and item_location not in plr.inv.inventory:
            item = Item(item_name, item_location, stacking, max_stack, 1, damage, healing, healing_amt, max_healing, max_heal_amt, armour_inc, armour_inc_amt, armour_type)
            result = plr.inv.add_to_inv(item)
            if result == -1:
                result_label.config(text="Inventory full!")
            else:
                plr.save()
                result_label.config(text=f"{item_name} added to inventory.")
        else:
            result_label.config(text="Invalid slot or item parameters.")

    def modify_quantity():
        item_name = tkinter.simpledialog.askstring("Modify Quantity", "Enter the name of the item:",
                                                   parent=cheat_window)
        action = tkinter.simpledialog.askstring("Modify", "Add or Remove quantity? (A/R):", parent=cheat_window)

        item = plr.inv.find_item(item_name)
        if item == -1:
            result_label.config(text="Item not found.")
            return

        if action and action.upper() == "A":
            add_amt = tkinter.simpledialog.askinteger("Add Quantity",
                                                      f"How much to add? (Max {item.max_stack - item.current_amt}):",
                                                      parent=cheat_window)
            if add_amt < item.max_stack:
                if item.add_to_stack(add_amt) == 1:
                    plr.save()
                    result_label.config(text=f"Added {add_amt} to {item_name}.")
                else:
                    result_label.config(text="Unable to add quantity.")

        elif action and action.upper() == "R":
            rmv_amt = tkinter.simpledialog.askinteger("Remove Quantity",
                                                      f"How much to remove? (Max {item.current_amt - 1}):",
                                                      parent=cheat_window)
            if rmv_amt:
                if item.remove_from_stack(rmv_amt) == 1:
                    plr.save()
                    result_label.config(text=f"Removed {rmv_amt} from {item_name}.")
                else:
                    result_label.config(text="Unable to remove quantity.")
    
    def add_base_item():
        """Runs the base item cheat menu """
        base_window = Toplevel()
        base_window.title("Base Item Menu")

        ttk.Label(base_window, text="----BASE ITEM MENU----").grid(column=0, row=0)

        def view_items():
            stats_text = "\n".join([
            f"Name: {i.name} | Slot: {i.location} | Amount: {i.current_amt} | Damage: {i.damage} | Healing: {i.healing_amt} | Max Health Increase: {i.max_heal_amt} | Armour Increase: {i.armour_inc_amt}"
            for i in plr.inv.hidden_inv.values()
            ])
            stats_label.config(text=stats_text)

        def add_item():
            item_name = tkinter.simpledialog.askstring("Item Name", "Enter item name to add:", parent=base_window)
            for i in plr.inv.hidden_inv.values():
                if i.name.strip().lower() == item_name.strip().lower():
                    plr.inv.add_to_inv(i)
                    plr.save()

        stats_label = Label(base_window, text="", wraplength=300, justify="left")
        stats_label.grid(column=0, row=3)

        ttk.Button(base_window, text="View Base Items", command=view_items).grid(column=0, row=1)
        ttk.Button(base_window, text="Add Item", command=add_item).grid(column=0, row=2)
        ttk.Button(base_window, text="Close", command=base_window.destroy).grid(column=0, row=4)

    result_label = Label(cheat_window, text="", wraplength=300, justify="left")
    result_label.grid(column=0, row=5)

    ttk.Button(cheat_window, text="Add Item", command=add_item).grid(column=0, row=1)
    ttk.Button(cheat_window, text="Modify Item Quantity", command=modify_quantity).grid(column=0, row=2)
    ttk.Button(cheat_window, text="Character Cheat Menu", command=open_char_cheat_menu).grid(column=0, row=3)
    ttk.Button(cheat_window, text="Add Base Item", command=add_base_item).grid(column=0, row=4)
    ttk.Button(cheat_window, text="Close", command=cheat_window.destroy).grid(column=0, row=6)