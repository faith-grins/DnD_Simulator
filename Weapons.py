from random import choice
from Dice_Rolling import d4, d6, d8, d10, d12

melee = 0
ranged = 1

slashing = 0
piercing = 1
bludgeoning = 2

finesse = 0
heavy = 1
light = 2
loading = 3
reach = 4
thrown = 5
two_handed = 6
versatile = 7


class Weapon:
    def __init__(self, die, num_dice, d_type, m_range, properties):
        self.damage = d_type
        self.range = m_range
        self.properties = properties
        self.die = die
        self.num_dice = num_dice

    def attack(self, abilities: list, reroll=False, versatile=False):
        mod = self.primary_mod(abilities)
        damage = mod
        damage_die = self.die
        if versatile:
            if damage_die == d4:
                damage_die = d6
            elif damage_die == d6:
                damage_die = d8
            elif damage_die == d8:
                damage_die = d10
            elif damage_die == d10:
                damage_die = d12
        for _ in range(self.num_dice):
            roll = choice(damage_die)
            if not reroll:
                damage += roll
            elif roll > 2:
                damage += roll
            else:
                damage += choice(damage_die)
        return damage

    def primary_mod(self, abilities: list):
        mod = abilities[0]
        if self.range == melee and (finesse in self.properties and abilities[1] > abilities[0]):
            mod = abilities[1]
        return (mod - 10) // 2


warhammer = Weapon(d8, 1, bludgeoning, melee, [versatile])
longsword = Weapon(d8, 1, slashing, melee, [versatile])
battleaxe = Weapon(d8, 1, slashing, melee, [versatile])
maul = Weapon(d6, 2, bludgeoning, melee, [two_handed, heavy])
greatsword = Weapon(d6, 2, slashing, melee, [two_handed, heavy])
greataxe = Weapon(d12, 1, slashing, melee, [two_handed, heavy])
flail = Weapon(d8, 1, bludgeoning, melee, [])
shortsword = Weapon(d6, 1, piercing, melee, [finesse, light])
spear = Weapon(d6, 1, piercing, melee, [thrown, versatile])
