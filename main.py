import Character
import Weapon
import sqlite3
import random


db_name = "diceydb.db"


def battle_menu(players, weapons, enemies):
    print("Which player will you choose?")
    for count, player in enumerate(players, start=1):
        output_string = "[{0}]: {1}"
        print(output_string.format(count, player.name))
    selection = int(input("Selection: ")) - 1
    print()
    print(players[selection])
    print()


def connect_db():
    db_conn = sqlite3.connect(db_name)
    db_cur = db_conn.cursor()
    return db_conn, db_cur


def create_enemy(db_cur):
    name = input("Enemy name: ")
    level = int(input("Enemy level: "))
    hp = random.randint(14, 17) + Character.hp_per_level(level)
    num_dice = 2
    return_enemy = Character.Enemy(name, level, hp, num_dice)
    status = 0

    sql_create_enemy = "INSERT INTO enemy (enemy_name, enemy_lvl, enemy_max_hp, enemy_invsize, status_id) VALUES (?, ?, ?, ?, ?)"
    create_enemy_tuple = (name, level, hp, num_dice, status)
    db_cur.execute(sql_create_enemy, create_enemy_tuple)
    print("Enemy added to database.")
    print(return_enemy)


def create_player(db_cur):
    name = input("Player name: ")
    level = int(input("Player level: "))
    hp = random.randint(14, 17) + Character.hp_per_level(level)
    num_dice = 2
    return_player = Character.Player(name, level, hp, num_dice)

    sql_create_player = "INSERT INTO player (player_name, player_lvl, player_current_hp, player_max_hp, player_xp_current, player_xp_to_level, player_gold, player_numdice, player_invsize, status_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    create_player_tuple = (return_player.name, return_player.level, return_player.current_hp, return_player.max_hp,
                           return_player.xp_current, return_player.xp_to_level, return_player.gold,
                           return_player.num_dice, return_player.inventory_size, return_player.status)
    db_cur.execute(sql_create_player, create_player_tuple)
    print("Player added to database.")
    print(return_player)
    print()


def create_status(db_cur):
    name = input("Status name: ")

    sql_create_status = "INSERT INTO status (status_name) VALUES (?);"
    create_status_tuple = (name,)
    db_cur.execute(sql_create_status, create_status_tuple)
    print("Status added to database.")
    print()


def create_weapon(db_cur):
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

    sql_create_weapon = "INSERT INTO weapon (weapon_name, weapon_min_roll, weapon_max_roll, weapon_modifier, status_id) VALUES (?, ?, ?, ?, ?)"
    create_weapon_tuple = (name, min_roll, max_roll, modifier, status_fx)
    db_cur.execute(sql_create_weapon, create_weapon_tuple)
    print("Weapon added to database.")
    print(weapon_return)


def drop_db(db_cur):
    sql_drop_p = "DROP TABLE IF EXISTS player"
    sql_drop_e = "DROP TABLE IF EXISTS enemy"
    sql_drop_w = "DROP TABLE IF EXISTS weapon"
    db_cur.execute(sql_drop_p)
    db_cur.execute(sql_drop_e)
    db_cur.execute(sql_drop_w)


def initialize_db(db_cur):
    sql_playertable = "CREATE TABLE IF NOT EXISTS player (" \
                      "player_id               integer         CONSTRAINT player_id_pk PRIMARY KEY AUTOINCREMENT," \
                      "player_name             varchar(20)     CONSTRAINT player_name_nn NOT NULL," \
                      "player_lvl              integer         CONSTRAINT player_lvl_nn NOT NULL," \
                      "player_current_hp       integer         CONSTRAINT player_curhp_chk CHECK (player_current_hp <= player_max_hp AND player_current_hp >= 0) NOT NULL," \
                      "player_max_hp           integer         CONSTRAINT player_max_hp_chk CHECK (player_max_hp >= player_current_hp) NOT NULL," \
                      "player_xp_current       integer         CONSTRAINT player_curxp_chk CHECK (player_xp_current <= player_xp_to_level AND player_xp_current >= 0) NOT NULL," \
                      "player_xp_to_level      integer         CONSTRAINT player_xplev_chk CHECK (player_xp_to_level >= player_xp_current) NOT NULL," \
                      "player_gold             integer         CONSTRAINT player_gold_chk CHECK (player_gold >= 0) NOT NULL," \
                      "player_numdice          integer         CONSTRAINT player_numdice_chk CHECK (player_numdice > 0) NOT NULL," \
                      "player_invsize          integer         CONSTRAINT player_invsize_chk CHECK (player_invsize > 0) NOT NULL," \
                      "status_id               integer         CONSTRAINT player_status_fk REFERENCES status(status_id) NOT NULL" \
                      ");"
    sql_enemytable = "CREATE TABLE IF NOT EXISTS enemy (" \
                     "enemy_id                integer         CONSTRAINT enemy_id_pk PRIMARY KEY AUTOINCREMENT," \
                     "enemy_name              varchar(20)     CONSTRAINT enemy_name_nn NOT NULL," \
                     "enemy_lvl               integer         CONSTRAINT enemy_lvl_nn NOT NULL," \
                     "enemy_max_hp            integer         CONSTRAINT enemy_maxhp_chk CHECK (enemy_max_hp >= 0)," \
                     "enemy_invsize           integer         CONSTRAINT enemy_invsize_chk CHECK (enemy_invsize > 0)," \
                     "enemy_numdice           integer         CONSTRAINT enemy_numdice_chk CHECK (enemy_numdice > 0)," \
                     "status_id               integer         CONSTRAINT enemy_status_fk REFERENCES status(status_id) NOT NULL" \
                     ");"
    sql_weapontable = "CREATE TABLE IF NOT EXISTS weapon (" \
                      "weapon_id               integer         CONSTRAINT weapon_id_pk PRIMARY KEY AUTOINCREMENT," \
                      "weapon_name             varchar(20)     CONSTRAINT weapon_name_nn NOT NULL," \
                      "weapon_min_roll         integer         CONSTRAINT weapon_minroll_chk CHECK (weapon_min_roll >= 1 AND weapon_min_roll <= weapon_max_roll)," \
                      "weapon_max_roll         integer         CONSTRAINT weapon_maxroll_chk CHECK (weapon_max_roll >= weapon_min_roll AND weapon_max_roll <= 6)," \
                      "weapon_modifier         integer         CONSTRAINT weapon_mod_chk CHECK (weapon_modifier >= 0)," \
                      "status_id               integer         CONSTRAINT weapon_status_fx_fk REFERENCES status(status_id) NOT NULL" \
                      ");"
    sql_inventorytable = "CREATE TABLE IF NOT EXISTS inventory (" \
                         "inv_playerid         integer         CONSTRAINT inv_pid_fk REFERENCES player(player_id)," \
                         "inv_weaponid         integer         CONSTRAINT inv_wid_fk REFERENCES weapon(weapon_id)," \
                         "CONSTRAINT inv_pk PRIMARY KEY (inv_playerid, inv_weaponid)" \
                         ");"

    sql_statustable = "CREATE TABLE IF NOT EXISTS status (" \
                      "status_id                 integer         CONSTRAINT status_id_pk PRIMARY KEY AUTOINCREMENT," \
                      "status_name               varchar(20)     CONSTRAINT status_name_nn NOT NULL" \
                      ");"

    db_cur.execute(sql_statustable)
    print("status table complete")
    db_cur.execute(sql_playertable)
    print("player table complete")
    db_cur.execute(sql_enemytable)
    print("enemy table complete")
    db_cur.execute(sql_weapontable)
    print("weapon table complete")
    db_cur.execute(sql_inventorytable)
    print("inventory table complete")


def print_db(db_cur):
    print_p = db_cur.execute("SELECT * FROM player")
    print("Players")
    for row_p in print_p:
        print(row_p)

    print("Enemies")
    print_e = db_cur.execute("SELECT * FROM enemy")
    for row_e in print_e:
        print(row_e)

    print("Weapons")
    print_w = db_cur.execute("SELECT * FROM weapon")
    for row_w in print_w:
        print(row_w)

    print("Inventories")
    print_i = db_cur.execute("SELECT * FROM inventory")
    for row_i in print_i:
        print(row_i)

    print("Statuses")
    print_s = db_cur.execute("SELECT * FROM status")
    for row_s in print_s:
        print(row_s)

    print()


def main_menu(db_conn, db_cur):
    while True:
        print("DICE BATTLE GAME MENU")
        print("*********************")
        print("[1] Create a player")
        print("[2] Create an enemy")
        print("[3] Create a weapon")
        print("[4] Create a status condition")
        print("[5] Assign a weapon")
        print("[9] Attack!")
        print("[11] Initialize DB")
        print("[22] Drop DB")
        print("[33] Print DB")
        print("[99] Quit")
        selection = int(input("Selection: "))
        print()

        if selection == 1:
            create_player(db_cur)
        elif selection == 2:
            create_enemy(db_cur)
        elif selection == 3:
            create_weapon(db_cur)
        elif selection == 4:
            create_status(db_cur)
        elif selection == 5:
            pass
        elif selection == 9:
            pass
        elif selection == 11:
            initialize_db(db_cur)
        elif selection == 22:
            drop_db(db_cur)
        elif selection == 33:
            print_db(db_cur)
        elif selection == 99:
            exit(0)

        db_conn.commit()


def main():
    db_conn, db_cur = connect_db()
    main_menu(db_conn, db_cur)
    

main()
