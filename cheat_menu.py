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
                          f"Current Damage: {plr.real_dmg}\n"
                          f"Currently Equipped: {plr.equipped_item}")
            stats_label.config(text=stats_text)

        def modify_health():
            health = tkinter.simpledialog.askinteger("Health Modification", "Enter new health:", parent=char_window)
            plr.health = health
            plr.save()

        def modify_dmg():
            damage = tkinter.simpledialog.askinteger("Damage Modification", "Enter new damage:", parent=char_window)
            plr.base_dmg = damage
            plr.save()

        stats_label = Label(char_window, text="", wraplength=300, justify="left")
        stats_label.grid(column=0, row=3)

        ttk.Button(char_window, text="View Character Stats", command=view_stats).grid(column=0, row=1)
        ttk.Button(char_window, text="Modify Health", command=modify_health).grid(column=0, row=2)
        ttk.Button(char_window, text="Modify Damage", command=modify_dmg).grid(column=0, row=3)
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

        if 0 <= item_location <= plr.inv.max_slots and item_location not in plr.inv.inventory:
            item = Item(item_name, item_location, stacking, max_stack, 1, damage, healing, healing_amt)
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
            if add_amt:
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

    result_label = Label(cheat_window, text="", wraplength=300, justify="left")
    result_label.grid(column=0, row=3)

    ttk.Button(cheat_window, text="Add Item", command=add_item).grid(column=0, row=1)
    ttk.Button(cheat_window, text="Modify Item Quantity", command=modify_quantity).grid(column=0, row=2)
    ttk.Button(cheat_window, text="Character Cheat Menu", command=open_char_cheat_menu).grid(column=0, row=3)
    ttk.Button(cheat_window, text="Close", command=cheat_window.destroy).grid(column=0, row=5)