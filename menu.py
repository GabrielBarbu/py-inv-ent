import tkinter.simpledialog
from cheat_menu import cheat_menu
from entity import Entity
from tkinter import *
from tkinter import ttk


def open_character_menu(plr: Entity):
    """Runs the character menu

    Args:
        plr (Entity): Player class
    """
    char_window = Toplevel()
    char_window.title("Character Menu")

    ttk.Label(char_window, text="----CHARACTER MENU----").grid(column=0, row=0)

    def view_stats():
        stats_text = (f"Name: {plr.name}\n"
                      f"Health: {plr.health}\n"
                      f"Current Damage: {plr.real_dmg}\n"
                      f"Currently Equipped: {plr.equipped_item}")
        stats_label.config(text=stats_text)

    def use_item():
        item_name = tkinter.simpledialog.askstring("Use Item", "Enter the name of the item to use:", parent=char_window)
        if item_name:
            try:
                item = plr.inv.find_item(item_name)
                result = plr.use_item(item)

                if result == 1 and item != -1:
                    healing = item.healing_amt
                    stats_label.config(text=f"Used {item.name}, healed {healing} HP.")
                    plr.save()
                else:
                    stats_label.config(text="Item does not exist or cannot be used.")
            except Exception as e:
                stats_label.config(text=f"Error using item: {e}")

    stats_label = Label(char_window, text="", wraplength=300, justify="left")
    stats_label.grid(column=0, row=3)

    ttk.Button(char_window, text="View Character Stats", command=view_stats).grid(column=0, row=1)
    ttk.Button(char_window, text="Use Item", command=use_item).grid(column=0, row=2)
    ttk.Button(char_window, text="Close", command=char_window.destroy).grid(column=0, row=4)


def menu(plr: Entity):
    """Runs the menu

    Args:
        plr (Entity): Player class
    """

    def update_inventory_display():
        inventory_text = "\n".join([
            f"Name: {i.name} | Slot: {i.location} | Amount: {i.current_amt} | Damage: {i.damage} | Healing: {i.healing_amt}"
            for i in plr.inv.inventory.values()
        ])
        use_label.config(text=inventory_text)

    def on_selection(event):
        """Handles user selection from the combobox"""
        user_choice = cmbx.get()
        use_label.config(text=f"Selected: {user_choice}")

        if user_choice.startswith("1"):
            update_inventory_display()

        elif user_choice.startswith("2"):
            item_name = tkinter.simpledialog.askstring("Remove Item", "Enter Item Name:")
            item = plr.inv.find_item(item_name)
            if item != -1:
                confirmation = tkinter.simpledialog.askstring("Confirm", f"Delete {item.name}? (Y/N)")
                if confirmation and confirmation.upper() == "Y":
                    plr.inv.remove_from_inv(item, plr)
                    plr.save()
                    use_label.config(text=f"{item.name} removed from inventory.")
                else:
                    use_label.config(text="Deletion canceled.")
            else:
                use_label.config(text="Item not found.")

        elif user_choice.startswith("3"):
            action = tkinter.simpledialog.askstring("Equip or Unequip", "Equip (E) or Unequip (U)?")
            item_name = tkinter.simpledialog.askstring("Enter Item Name", "Enter Item Name:")

            if action and item_name:
                item = plr.inv.find_item(item_name)
                if action.upper() == "E":
                    result = plr.equip_item(item)
                    use_label.config(text=f"{item.name} equipped." if result else "Item not found or already equipped.")
                    plr.save()
                elif action.upper() == "U":
                    result = plr.unequip_item(item)
                    use_label.config(
                        text=f"{item.name} unequipped." if result else "Item not equipped or does not exist.")
                    plr.save()
                else:
                    use_label.config(text="Invalid choice.")

        elif user_choice.startswith("4"):
            item_name = tkinter.simpledialog.askstring("Move Item", "Enter the name of the item:")
            new_location = tkinter.simpledialog.askstring("New Location", "Enter the new location for the item:")

            if new_location and new_location.isdigit():
                new_location = int(new_location)
                if 0 <= new_location <= plr.inv.max_slots and new_location not in plr.inv.inventory.keys():
                    item = plr.inv.find_item(item_name)
                    result = plr.inv.move_item(item, new_location)
                    if result == 1:
                        use_label.config(text=f"{item.name} moved to slot {new_location}.")
                        plr.save()
                    else:
                        use_label.config(text="Item could not be moved.")
                else:
                    use_label.config(text="Invalid slot: Out of range or occupied.")
            else:
                use_label.config(text="Invalid input: Location must be a number.")

        elif user_choice.startswith("5"):
            open_character_menu(plr)

        elif user_choice.startswith("6"):
            root.destroy()

    def check_cheat_code(cheat_code_entry):
        if cheat_code_entry.get() == "iamacheater":
            cheat_menu(plr)
            use_label.config(text="Cheat menu activated.")

    root = Tk()
    root.title("Inventory Menu")

    frm = ttk.Frame(root, padding=10)
    frm.grid()

    ttk.Label(frm, text="----INVENTORY MENU----").grid(column=0, row=0)
    use_label = Label(frm, text="", wraplength=300, justify="left")
    use_label.grid(column=0, row=2)

    cmbx = ttk.Combobox(frm, width=40, state="readonly")
    cmbx['values'] = [
        "1. View stats of items in inventory",
        "2. Remove an item from inventory",
        "3. Equip or Unequip an item",
        "4. Move an item to another slot",
        "5. View character menu",
        "6. Exit Menu",
    ]
    cmbx.grid(column=0, row=1)
    cmbx.bind("<<ComboboxSelected>>", on_selection)

    ttk.Label(frm, text="Enter Cheat Code:").grid(column=0, row=5)
    cheat_code_entry = Entry(frm, width=20)
    cheat_code_entry.grid(column=0, row=6)
    ttk.Button(frm, text="Submit", command=lambda: check_cheat_code(cheat_code_entry)).grid(column=0, row=7)

    ttk.Button(frm, text="Clear", command=lambda: cmbx.set('')).grid(column=0, row=3)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=4)

    root.mainloop()