import Character
import Weapon
import random


def battle_menu(players, weapons, enemies):
    print("Which player will you choose?")
    for count, player in enumerate(players, start=1):
        output_string = "[{0}]: {1}"
        print(output_string.format(count, player.name))
    selection = int(input("Selection: ")) - 1
    print()
    print(players[selection])
    print()


def create_enemy():
    name = input("Enemy name: ")
    level = 1
    hp = random.randint(14, 17)
    num_dice = 2
    return Character.Enemy(name, level, hp, num_dice)


def create_player():
    name = input("Player name: ")
    level = int(input("Player level: "))
    hp = random.randint(14, 17) + Character.hp_per_level(level)
    num_dice = 2
    return_player = Character.Player(name, level, hp, num_dice)
    print(return_player)
    print()
    return return_player


def create_weapon():
    name = input("Weapon name: ")

    min_roll = 0
    while not 1 <= min_roll <= 6:
        min_roll = int(input("Enter minimum roll (1 to 6): "))
        if not 1 <= min_roll <= 6:
            print("Must enter between 1 and 6.")

    max_roll = 0
    while not min_roll <= max_roll <= 6:
        max_roll = int(input("Enter maximum roll (1 to 6): "))
        if not min_roll <= max_roll <= 6:
            print("Must enter between", min_roll, " and 6.")

    modifier = int(input("Enter attack modifier to add to a successful roll: "))

    Weapon.print_status_effects()
    status_fx = int(input("Enter weapon status effect: "))

    weapon_return = Weapon.Weapon(name, min_roll, max_roll, modifier, status_fx)
    return weapon_return


def main_menu():
    players = []
    weapons = []
    enemies = []
    while True:
        print("DICE BATTLE GAME MENU")
        print("*********************")
        print("[1] Create a player")
        print("[2] Create an enemy")
        print("[3] Create a weapon")
        print("[4] Assign a weapon")
        print("[5] Attack!")
        print("[6] Quit")
        selection = int(input("Selection: "))
        print()

        if selection == 1:
            players.append(create_player())
        elif selection == 2:
            enemies.append(create_enemy())
        elif selection == 3:
            weapons.append(create_weapon())
        elif selection == 4:
            pass
        elif selection == 5:
            battle_menu(players, weapons, enemies)
        elif selection == 6:
            exit(0)


def main():
    main_menu()
    

main()
