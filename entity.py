import inventory
from inventory import Inventory, Item

class Entity:
    def __init__(self, inventory: Inventory, char_name: str, char_health: int, char_base_dmg: int, equipped_item: str, max_health: int, armour: float, max_armour: float):
        """Creates an entity class

        Args:
            inventory (Inventory): Inventory class
            char_name (str): Name of character
            char_health (int): Character health
            char_base_dmg (int): Character base damage
            equipped_item (str): Currently equipped item (has to be an item class)
            max_health (int): The max health of the character
            armour (float): The armour of the character
            max_armour (float): The max armour of the character
        """
        self.inv = inventory
        self.name = char_name
        self.health = char_health
        self.base_dmg = char_base_dmg
        self.real_dmg = self.base_dmg
        self.equipped_item = equipped_item
        self.max_health = max_health
        self.armour = armour
        self.max_armour = max_armour
        self.torso = "None"
        self.head = "None"
        self.legs = "None"
        self.feet = "None"

    def check_item(self, item_name: str):
        """Equips an item, the damage becomes item damage

        Args:
            item_name (str): Name of item

        Returns:
            int: 1 if successful, "None" if failed
        """
        item = self.inv.find_item(item_name)
        if type(item) == Item:
            return 1
        else:
            return "None"

    def equip_item(self, item: Item):
        """Equips an item, the damage becomes item damage

        Args:
            item (Item): Item class

        Returns:
            int: 1 if successful, -1 if failed
        """
        if self.equipped_item == "None" and item.armour_inc == False:
            self.equipped_item = item.name
            self.real_dmg = item.damage
            return 1
        elif self.torso == "None":
            if item.armour_type == "torso":
                self.torso = item.name
                self.armour += item.armour_inc_amt
                return 1
            else:
                return -1
        elif self.head == "None":
            if item.armour_type == "head":
                self.head = item.name
                self.armour += item.armour_inc_amt
                return 1
            else:
                return -1
        elif self.legs == "None":
            if item.armour_type == "legs":
                self.legs = item.name
                self.armour += item.armour_inc_amt
                return 1
            else:
                return -1
        elif self.feet == "None":
            if item.armour_type == "feet":
                self.feet = item.name
                self.armour += item.armour_inc_amt
                return 1
            else:
                return -1
        else:
            return -1

    def unequip_item(self, item: Item):
        """Unequips an item, damage is returned to base

        Args:
            item (Item): Item class

        Returns:
            int: 1 if successful, -1 if failed
        """
        if self.equipped_item.strip().lower() == item.name.strip().lower():
            self.equipped_item = "None"
            self.real_dmg = self.base_dmg
            return 1
        elif self.torso.strip().lower() == item.name.strip().lower():
            self.torso = "None"
            self.armour -= item.armour_inc_amt
            return 1
        elif self.legs.strip().lower() == item.name.strip().lower():
            self.legs = "None"
            self.armour -= item.armour_inc_amt
            return 1
        elif self.head.strip().lower() == item.name.strip().lower():
            self.head = "None"
            self.armour -= item.armour_inc_amt
            return 1
        elif self.feet.strip().lower() == item.name.strip().lower():
            self.feet = "None"
            self.armour -= item.armour_inc_amt
            return 1
        else:
            return -1

    def save(self):
        """Saves the character to a text file and calls inventory save
        """
        self.inv.save_to_file()
        print(self.torso, self.head, self.legs, self.feet)
        with open("char.txt", "w") as file:
            file.write(
                self.name + "," + str(self.health) + "," + str(self.base_dmg) + "," + str(self.equipped_item) + "," + str(self.max_health) + "," + str(self.max_armour) +
                "," + self.torso + "," + self.head + "," + self.legs + "," + self.feet + "\n")

    def use_item(self, item: Item):
        """Uses an item to heal

        Args:
            item (Item): Item class

        Returns:
            int: 1 if successful, -1 if failed
        """
        i = item
        if i.healing:
            self.health += i.healing_amt
            if self.equipped_item.strip() == i.name.strip():
                self.unequip_item(i)
            if i.stackable and i.current_amt > 1:
                i.remove_from_stack(1)
            else:
                self.inv.remove_from_inv(i, self)
            return 1
        else:
            return -1

    def check_health(self):
        """Checks the health of the character, to see if they are dead

        Returns:
            int: 1 if alive, -1 if dead
        """
        if self.health <= 0:
            return -1
        else:
            return 1

    def attack(self, enemy: object):
        """Attacks the enemy

        Args:
            enemy (Entity): Enemy entity class

        Returns:
            int: Calls check_health() and returns value from there
        """
        if enemy.health > 0:
            if enemy.armour > 0:
                enemy.health -= (self.real_dmg - (self.real_dmg * enemy.armour))
            else:
                enemy.health -= self.real_dmg
            return enemy.check_health()
        else:
            return enemy.check_health()

    def load_armour(self):
        """Loads the armour of the character

        Returns:
            int: 1 if successful, -1 if failed
        """
        with open("char.txt", "r") as file:
            char = [line.strip().split(',') for line in file]
            for char_data in char:
                torso = char_data[6]
                head = char_data[7]
                legs = char_data[8]
                feet = char_data[9]
                print(torso,head,legs,feet)
                if torso != "None":
                    self.equip_item(self.inv.find_item(torso))
                else:
                    self.torso = "None"
                if head != "None":
                    self.equip_item(self.inv.find_item(head))
                else:
                    self.head = "None"
                if legs != "None":
                    self.equip_item(self.inv.find_item(legs))
                else:
                    self.legs = "None"
                if feet != "None":
                    self.equip_item(self.inv.find_item(feet))
                else:
                    self.feet = "None"

def load_char(inv: Inventory):
    """Loads the character

    Args:
        inv (Inventory): Inventory class

    Returns:
        Entity: Entity class
    """
    try:
        with open("char.txt", "r") as file:
            char = [line.strip().split(',') for line in file]
            for char_data in char:
                name = char_data[0]
                health = int(char_data[1])
                base_dmg = int(char_data[2])
                equipped_item = char_data[3]
                max_health = int(char_data[4])
                max_armour = float(char_data[5])
                plr = Entity(inv, name, health, base_dmg, equipped_item, max_health, 0, max_armour)
            plr.inv.load_from_file()
            plr.inv.load_base_items()
            plr.load_armour()
            result = plr.check_item(equipped_item)
            if result == 1:
                return plr
            else:
                plr.equipped_item = result
                plr.save()
                return plr
    except OSError:
        temp_run = True

        while temp_run:
            char_name = input("Enter the name of your character: ")
            plr = Entity(inv, char_name, 100, 1, "None", 100, 0, 0.9)
            print("Character {} created".format(char_name))
            plr.save()
            temp_run = False
            return plr