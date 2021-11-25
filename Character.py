import random
import Weapon
import sqlite3


class Player:
    status_list = ["None", "Poison", "Sleep", "Freeze"]

    def __init__(self, name, level, hp, num_dice):
        self.name = name
        self.level = level
        self.current_hp = hp
        self.max_hp = hp
        self.xp_current = 0
        self.xp_to_level = 6 + level
        self.gold = 0
        self.num_dice = num_dice
        self.weapons = []
        self.inventory_size = 8
        self.status = 0

    def __str__(self):
        outputstring = "Player name: {0}\n" \
                       "Level: {1}\n" \
                       "HP: {2}/{3}\n" \
                       "XP: {4}/{5}\n" \
                       "Gold: {6}\n" \
                       "Number of Dice: {7}\n" \
                       "Status: {8}"
        return outputstring.format(self.name,
                                   self.level,
                                   self.current_hp,
                                   self.max_hp,
                                   self.xp_current,
                                   self.xp_to_level,
                                   self.gold,
                                   self.num_dice,
                                   self.status_list[self.status])

    def add_weapon(self, weapon):
        if len(self.weapons) < self.inventory_size:
            self.weapons.append(weapon)
        else:
            print("Inventory full.")

    def attack(self, weaponindex, enemy):
        pass

    def get_gold(self, amount):
        self.gold += amount

    def heal(self, amount):
        self.current_hp += amount

    def level_up(self):
        # Increase all relevant stats
        # Heal to full health
        self.max_hp_up(random.randint(2, 4))
        self.heal(self.max_hp - self.current_hp)
        self.level += 1
        self.xp_current = 0

    def max_hp_up(self, amount):
        self.max_hp = self.max_hp + amount

    def print_weapons(self):
        for x in self.weapons:
            print(x)

    def set_status(self, status_fx):
        self.status = status_fx

    def use_gold(self, amount):
        self.gold -= amount

    def xp_up(self, amount):
        self.xp_current += amount


class Enemy:
    status_list = ["None", "Poison", "Sleep", "Freeze"]

    def __init__(self, name, level, hp, num_dice):
        self.name = name
        self.level = level
        self.current_hp = hp
        self.max_hp = hp
        self.num_dice = num_dice
        self.inventory_size = 4
        self.status = 0

    def __str__(self):
        outputstring = "Player name: {0}\nLevel: {1}\nHP: {2}/{3}\nNumber of Dice: {4}"
        return outputstring.format(self.name, self.level, self.current_hp, self.max_hp, self.num_dice)


def hp_per_level(level):
    hp_added = 0
    for x in range(level):
        hp_added += random.randint(2,4)
    return hp_added
