from menu import menu
from inventory import Inventory
from entity import load_char
from inventory import Item
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog

inv = Inventory(20)
enm_inv = Inventory(5)

run = True

try:
    plr = load_char(inv)
except OSError:
    print("Character could not be loaded")
    run = False


def play_game():
    game_window = Toplevel()
    game_window.title("Game Window")

    ttk.Label(game_window, text="You are in a forest. There is a conveniently placed wooden sword on the ground").grid(
        column=0, row=0)
    user_input = Entry(game_window, width=40)
    user_input.grid(column=0, row=1)

    def process_input():
        user_choice = user_input.get().lower()
        output_label.config(text="")

        if user_choice == "pickup sword":
            item_location = simpledialog.askinteger("Item Location",
                                                    "Enter where you would like to place the wooden sword (0-{}):".format(
                                                        plr.inv.max_slots), parent=game_window)
            if not item_location > plr.inv.max_slots and not item_location < 0 and not item_location in plr.inv.inventory.keys():
                item = Item("Wooden Sword", item_location, False, 1, 1, 10, False, 0)
                result = plr.inv.add_to_inv(item)
                if result == -1:
                    output_label.config(text="Inventory full")
                else:
                    output_label.config(text="You have picked up {}".format(item.name))
                    plr.save()
            else:
                output_label.config(text="Invalid location")

        elif user_choice == "menu":
            menu(plr)

    ttk.Button(game_window, text="Submit", command=process_input).grid(column=0, row=2)
    output_label = ttk.Label(game_window, text="", wraplength=300)
    output_label.grid(column=0, row=3)
    ttk.Button(game_window, text="Close", command=game_window.destroy).grid(column=0, row=4)


def main_menu():
    root = Tk()
    root.title("Main Menu")

    frm = ttk.Frame(root, padding=10)
    frm.grid()

    ttk.Label(frm, text="----MAIN MENU----").grid(column=0, row=0)
    ttk.Button(frm, text="Inventory + Character Menu", command=lambda: menu(plr)).grid(column=0, row=1)
    ttk.Button(frm, text="Play", command=lambda: [root.withdraw(), play_game()]).grid(column=0, row=2)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=3)

    root.mainloop()


if __name__ == "__main__":
    main_menu()
