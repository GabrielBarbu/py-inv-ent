import os

class Inventory:
    def __init__(self, max_slots: int):
        """Creates an inventory class

        Args:
            max_slots (integer): The maximum number of inventory slots
        """
        self.inventory = {}
        self.max_slots = max_slots
        self.used_slots = 0
        
    def find_item(self, item_name: str):
        """Uses the item name to find the item in inventory and
           returns the item object if it is found

        Args:
            item_name (string): Name of item

        Returns:
            Item: Item class object
            int: -1 If failed
        """
        for i in self.inventory.values():
            if i.name.strip().lower() == item_name.strip().lower():
                return i

        return -1

    def add_to_inv(self, item: object):
        """Adds an item to the inventory

        Args:
            item (object): Takes item class object

        Returns:
            int: 1 if successful, -1 if failed
        """
        if not self.used_slots >= self.max_slots:
            if item.location in self.inventory.keys() and item.location <= self.max_slots:
                item.location += 1
                self.inventory.update({item.location: item})
                self.used_slots += 1
                return 1
            elif item.location in self.inventory.keys() and item.location >= 0:
                item.location -= 1
                self.inventory.update({item.location: item})
                self.used_slots += 1
                return 1
            else:
                self.inventory.update({item.location: item})
                self.used_slots += 1
                return 1
        else:
            return -1

    def remove_from_inv(self, item: object, plr: object):
        """Removes an item from inventory

        Args:
            item (object): Item class
            plr (object): Player class

        Returns:
            int: 1 if successful, -1 if failed
        """
        if item.location in self.inventory.keys():
            if item.name.strip().lower() == plr.equipped_item.strip().lower():
                plr.unequip_item(item)
            self.inventory.pop(item.location)
            return 1
        else:
            return -1

    def save_to_file(self):
        """Saves inventory to a text file
        """
        with open("inv.txt", "w") as file:
            for i in self.inventory.values():
                file.write(f"{i.location},{i.name},{i.stackable},{i.max_stack},{i.current_amt},{i.damage},{i.healing},{i.healing_amt},{i.max_healing},{i.max_heal_amt}\n")

    def load_from_file(self):
        """Loads inventory from a text file
        """
        with open("inv.txt", "r") as file:
            for line in file:
                item_data = line.strip().split(',')
                item_location = int(item_data[0])
                item_name = item_data[1]
                stackable = bool(item_data[2])
                max_stack = int(item_data[3])
                current_amt = int(item_data[4])
                damage = int(item_data[5])
                healing = bool(item_data[6])
                healing_amt = int(item_data[7])
                max_healing = bool(item_data[8])
                max_heal_amt = int(item_data[9])
                item = Item(item_name, item_location, stackable, max_stack, current_amt, damage, healing, healing_amt, max_healing, max_heal_amt)
                self.add_to_inv(item)

    def move_item(self, item: object, new_location:int, plr: object):
        """Adds to item stack

        Args:
            item (object): Item class
            new_location (int): New location of item
            plr (object): Player class

        Returns:
            int: 1 if successful, -1 or -2 if failed
        """
        result1 = self.remove_from_inv(item, plr)
        item.location = new_location
        result2 = self.add_to_inv(item)
        return (result1 + result2) - 1

    def delete_saves(self):
        if os.path.exists("inv.txt") and os.path.exists("char.txt"):
            os.remove("inv.txt")
            os.remove("char.txt")
            return 1
        else:
            return -1

class Item:
    def __init__(self, item_name: str, location: int, stackable: bool, max_stack: int, current_amt: int, damage: int, healing: bool, healing_amt: int, max_healing: bool, max_heal_amt: int):
        """Creates an Item class

        Args:
            item_name (str): Name of item
            location (int): Location in inventory
            stackable (bool): Can it be stacked
            max_stack (int): Amount of times item can stack
            current_amt (int): Current amount in stack
            damage (int): Item damage
            healing (bool): Can it heal
            healing_amt (int): Amount item heals for
            max_healing (bool): Can it increase max health
            max_heal_amt (int): Amount item increases max health by
        """
        self.name = item_name
        self.location = location
        self.stackable = stackable
        self.max_stack = max_stack
        self.current_amt = current_amt
        self.damage = damage
        self.healing = healing
        self.healing_amt = healing_amt
        self.max_healing = max_healing
        self.max_heal_amt = max_heal_amt

    def add_to_stack(self, amt_add: int):
        """Adds to item stack

        Args:
            amt_add (int): Amount to add to stack

        Returns:
            int: 1 if successful, -1 if failed
        """
        if self.stackable and self.current_amt < self.max_stack:
            self.current_amt += amt_add
            return 1
        else:
            return -1

    def remove_from_stack(self, amt_rmv: int):
        """Removes from item stack

        Args:
            amt_rmv (int): Amount to remove from stack

        Returns:
            int: 1 if successful, -1 if failed
        """
        if self.stackable and self.current_amt > 1:
            self.current_amt -= amt_rmv
            return 1
        else:
            return -1