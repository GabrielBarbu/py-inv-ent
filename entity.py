from inventory import Inventory

class Entity:
    def __init__(self, inventory: Inventory, char_name: str, char_health: int, char_base_dmg: int, equipped_item: str):
        """Creates an entity class

        Args:
            inventory (Inventory): Inventory class
            char_name (str): Name of character
            char_health (int): Character health
            char_base_dmg (int): Character base damage
            equipped_item (str): Currently equipped item (has to be an item)
        """
        self.inv = inventory
        self.name = char_name
        self.health = char_health
        self.base_dmg = char_base_dmg
        self.real_dmg = self.base_dmg
        self.equipped_item = equipped_item

    def equip_item(self, item_name: str):
        """Equips an item, the damage becomes item damage

        Args:
            item_name (str): Name of item

        Returns:
            int: 1 if successful, -1 if failed
        """
        if self.equipped_item == "None":
            for i in self.inv.inventory.values():
                if i.name.strip() == item_name.strip():
                    self.equipped_item = i.name
                    self.real_dmg = i.damage
                    return 1
                else:
                    return -1
        else:
            return -1

    def unequip_item(self, item_name: str):
        """Unequips an item, damage is returned to base

        Args:
            item_name (str): Name of item

        Returns:
            int: 1 if successful, -1 if failed
        """
        for i in self.inv.inventory.values():
            if i.name.strip() == item_name.strip():
                if self.equipped_item.strip() == i.name.strip():
                    self.equipped_item = "None"
                    self.real_dmg = self.base_dmg
                    return 1
                else:
                    return -1
            else:
                return -1

    def save(self):
        """Saves the character to a text file and calls inventory save
        """
        self.inv.save_to_file()
        with open("char.txt", "w") as file:
            file.write(self.name + "," + str(self.health) + "," + str(self.base_dmg) + "," + str(self.equipped_item) + "\n")
            
    def use_item(self, item_name: str):
        """Uses an item to heal

        Args:
            item_name (str): Item name

        Returns:
            int: 1 if successful, -1 if failed
        """
        for i in self.inv.inventory.values():
            if i.name.strip() == item_name.strip():
                if i.healing:
                    self.health += i.healing_amt
                    if self.equipped_item == i.name.strip():
                        self.unequip_item(item_name)
                    if i.stackable and i.current_amt > 1:
                        i.remove_from_stack(1)
                    else:
                        self.inv.remove_from_inv(i.location)
                    return 1
                else:
                    return -1
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