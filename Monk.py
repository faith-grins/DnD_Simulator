from enum import IntEnum
from Races import Race, ability_adjustment
from PC_Classes import PCClass
from Spells import half_caster_slots
from random import choice
import Dice_Rolling
import Weapons
__author__ = 'faith_grins'


class Options(IntEnum):
    OPEN_FIST = 0
    FOUR_ELEMENTS = 1
    SHADOW = 2
    KENSEI = 3


class Monk(PCClass):

    def __init__(self, level: int, race: Race, *options, starting_array=None):
        if not starting_array:
            starting_array = [10, 15, 13, 12, 14, 8]
        PCClass.__init__(self, race, level, [1, 4, 2, 0, 3, 5], starting_array)
        #   Set Tradition.  Defaults to Open Fist if not provided.
        self.tradition = None
        if level >= 3:
            for o in Options:
                if o in options and o >= Options.OPEN_FIST:
                    self.tradition = o
            if not self.tradition:
                self.tradition = Options.OPEN_FIST
        #   Set martial arts die
        self.martial_die = Dice_Rolling.d4
        if level > 16:
            self.martial_die = Dice_Rolling.d10
        elif level > 10:
            self.martial_die = Dice_Rolling.d8
        elif level > 4:
            self.martial_die = Dice_Rolling.d6
        #   Set ki pool size
        self.max_ki = 0 if level < 2 else level
        self.ki = self.max_ki
        self.unarmed_attack = Weapons.Weapon(self.martial_die, 1, Weapons.bludgeoning, Weapons.melee, [Weapons.finesse])
        self.weapons = [Weapons.spear, Weapons.shortsword, self.unarmed_attack]
        for w in self.weapons:
            if Weapons.finesse not in w.properties:
                w.properties.append(Weapons.finesse)
        self.AC = 10 + self.dex_mod() + self.wis_mod()

    def __str__(self):
        return str({'level': self.level, 'tradition': self.tradition,
                    'abilities': self.abilities, 'race': self.race})

    def set_weapons(self, weapons: list):
        self.weapons = weapons
        if self.unarmed_attack not in self.weapons:
            self.weapons.append(self.unarmed_attack)

    def attack(self, weapon=0, ac=13, flurry=False, dodge=False):
        weapon = self.weapons[weapon]
        num_attacks = 1 if self.level < 5 else 2
        versatile = Weapons.versatile in weapon.properties
        damage = 0
        unarmed_attacks = 0
        if flurry and self.ki > 0:
            unarmed_attacks += 2
        elif not dodge:
            unarmed_attacks += 1
        bonus = self.proficiency_bonus + weapon.primary_mod(self.abilities)
        for i in range(num_attacks):
            attack_roll = choice(Dice_Rolling.d20) + bonus
            if attack_roll >= ac:
                hit = weapon.attack(self.abilities, versatile=versatile)
                damage += hit
        for i in range(unarmed_attacks):
            attack_roll = choice(Dice_Rolling.d20) + bonus
            if attack_roll >= ac:
                hit = self.unarmed_attack.attack(self.abilities)
                damage += hit
        return damage


# Hank_Defender_of_Peanut_Butter = Paladin(12, Race.HALF_ELF, Options.OATH_OF_VENGEANCE, Options.DEFENSE)
# print(Hank_Defender_of_Peanut_Butter)
