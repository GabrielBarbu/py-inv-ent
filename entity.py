from inventory import Inventory, Item

class Entity:
    def __init__(self, inventory: Inventory, char_name: str, char_health: int, char_base_dmg: int, equipped_item: str, max_health: int):
        """Creates an entity class

        Args:
            inventory (Inventory): Inventory class
            char_name (str): Name of character
            char_health (int): Character health
            char_base_dmg (int): Character base damage
            equipped_item (str): Currently equipped item (has to be an item class)
            max_health (int): The max health of the character
        """
        self.inv = inventory
        self.name = char_name
        self.health = char_health
        self.base_dmg = char_base_dmg
        self.real_dmg = self.base_dmg
        self.equipped_item = equipped_item
        self.max_health = max_health

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
        if self.equipped_item == "None":
            self.equipped_item = item.name
            self.real_dmg = item.damage
            return 1
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
        else:
            return -1

    def save(self):
        """Saves the character to a text file and calls inventory save
        """
        self.inv.save_to_file()
        with open("char.txt", "w") as file:
            file.write(
                self.name + "," + str(self.health) + "," + str(self.base_dmg) + "," + str(self.equipped_item) + "," + str(self.max_health) + "\n")

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
            enemy.health -= self.real_dmg
            return enemy.check_health()
        else:
            return enemy.check_health()

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
                plr = Entity(inv, name, health, base_dmg, equipped_item, max_health)
            plr.inv.load_from_file()
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
            plr = Entity(inv, char_name, 100, 1, "None", 100)
            print("Character {} created".format(char_name))
            plr.save()
            temp_run = False
            return plr