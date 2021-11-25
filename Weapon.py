class Weapon:
    status_list = ["None", "Poison", "Sleep", "Freeze"]

    def __init__(self, name, min_roll, max_roll, modifier, status_fx):
        self.name = name
        self.min_roll = min_roll
        self.max_roll = max_roll
        self.modifier = modifier
        self.status_fx = status_fx

    def __str__(self):
        outputstring = "Weapon name: {0}\n" \
                       "Minimum roll: {1}\n" \
                       "Maximum roll: {2}\n" \
                       "Modifier: {3}\n" \
                       "Status effect: {4}\n"

        return outputstring.format(self.name,
                                   self.min_roll,
                                   self.max_roll,
                                   self.modifier,
                                   self.status_list[self.status_fx])


def print_status_effects():
    print("STATUS EFFECTS")
    print("[0]: None\n[1]: Poison\n[2]: Sleep\n[3]: Freeze")
