from enum import IntEnum
from Races import Race, ability_adjustment
from PC_Classes import PCClass
from Spells import half_caster_slots
from random import choice
import Dice_Rolling
import Weapons
__author__ = 'faith_grins'


class Options(IntEnum):
    DUELING = 0
    PROTECTION = 1
    DEFENSE = 2
    GREAT_WEAPON_FIGHTING = 3
    OATH_OF_ANCIENTS = 4
    OATH_OF_DEVOTION = 5
    OATH_OF_VENGEANCE = 6


class Paladin(PCClass):

    def __init__(self, level: int, race: Race, *options, starting_array=None):
        if not starting_array:
            starting_array = [15, 12, 13, 8, 10, 14]
        PCClass.__init__(self, race, level, [0, 2, 5, 1, 4, 3], starting_array)
        #   Set fighting style.  Defaults to Dueling if not provided.
        self.style = None
        if level >= 2:
            for o in Options:
                if o in options and o < Options.OATH_OF_ANCIENTS:
                    self.style = o
            if not self.style:
                self.style = Options.DUELING
        #   Set Oath.  Defaults to Ancients if not provided.
        self.oath = None
        if level >= 3:
            for o in Options:
                if o in options and o >= Options.OATH_OF_ANCIENTS:
                    self.oath = o
            if not self.oath:
                self.oath = Options.OATH_OF_ANCIENTS
        #   Handle Spells/spell slots.
        self.spell_slots = half_caster_slots(level)
        self.weapons = []
        default_weapons = {Options.DUELING: Weapons.battleaxe, Options.PROTECTION: Weapons.battleaxe,
                           Options.DEFENSE: Weapons.greatsword, Options.GREAT_WEAPON_FIGHTING: Weapons.greatsword}
        self.weapons.append(default_weapons[self.style])
        self.AC = 18
        if self.weapons[0] == Weapons.battleaxe:
            self.AC += 2

    def __str__(self):
        return str({'level': self.level, 'oath': self.oath, 'style': self.style,
                    'abilities': self.abilities, 'race': self.race, 'spells': self.spell_slots})

    def set_weapons(self, weapons: list):
        self.weapons = weapons

    def attack(self, weapon=0, ac=13):
        weapon = self.weapons[weapon]
        num_attacks = 1 if self.level < 5 else 2
        dual_wield = False
        if weapon == Weapons.shortsword:
            num_attacks += 1
            dual_wield = True
        re_roll = Options.GREAT_WEAPON_FIGHTING and Weapons.two_handed in weapon.properties
        damage = 0
        bonus = self.proficiency_bonus + weapon.primary_mod(self.abilities)
        for i in range(num_attacks):
            attack_roll = choice(Dice_Rolling.d20) + bonus
            if attack_roll >= ac:
                hit = weapon.attack(self.abilities, re_roll)
                if self.style == Options.DUELING and weapon.properties != Weapons.two_handed:
                    hit += 2
                if self.level >= 11:
                    hit += choice(Dice_Rolling.d8)
                if i == num_attacks - 1 and dual_wield:
                    hit -= (bonus - self.proficiency_bonus)
                damage += hit
        return damage


# Hank_Defender_of_Peanut_Butter = Paladin(12, Race.HALF_ELF, Options.OATH_OF_VENGEANCE, Options.DEFENSE)
# print(Hank_Defender_of_Peanut_Butter)
