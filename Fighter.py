from enum import IntEnum
from Races import Race, ability_adjustment
from PC_Classes import PCClass
from Spells import one_third_caster_slots
from random import choice
import Dice_Rolling
import Weapons
__author__ = 'faith_grins'


class Options(IntEnum):
    DUELING = 0
    PROTECTION = 1
    DEFENSE = 2
    GREAT_WEAPON_FIGHTING = 3
    ARCHERY = 4
    TWO_WEAPON_FIGHTING = 5
    CHAMPION = 6
    BATTLEMASTER = 7
    ELDRITCH_KNIGHT = 8


class Fighter(PCClass):

    def __init__(self, level: int, race: Race, *options, starting_array=None):
        if not starting_array:
            starting_array = [15, 13, 14, 8, 12, 10]
        PCClass.__init__(self, race, level, [0, 2, 1, 5, 3, 4], starting_array)
        #   Set fighting style.  Defaults to Dueling if not provided.
        self.style = None
        for o in options:
            if o in Options and o < Options.CHAMPION:
                self.style = o
        if not self.style:
            self.style = Options.DUELING
        #   Set Archetype.  Defaults to Champion if not provided.
        self.archetype = None
        if level >= 3:
            for o in Options:
                if o in options and o >= Options.CHAMPION:
                    self.archetype = o
            if not self.archetype:
                self.archetype = Options.CHAMPION
        #   Handle Spells/spell slots.
        if self.archetype == Options.ELDRITCH_KNIGHT:
            self.spell_slots = one_third_caster_slots(level)
        else:
            self.spell_slots = None
        self.weapons = []
        default_weapons = {Options.DUELING: Weapons.battleaxe, Options.PROTECTION: Weapons.battleaxe,
                           Options.DEFENSE: Weapons.greatsword, Options.GREAT_WEAPON_FIGHTING: Weapons.greatsword,
                           Options.TWO_WEAPON_FIGHTING: Weapons.shortsword}
        self.weapons.append(default_weapons[self.style])
        self.AC = 18
        if self.weapons[0] == Weapons.battleaxe:
            self.AC += 2

    def __str__(self):
        return str({'level': self.level, 'archetype': self.archetype, 'style': self.style,
                    'abilities': self.abilities, 'race': self.race, 'spells': self.spell_slots})

    def set_weapons(self, weapons: list):
        self.weapons = weapons

    def attack(self, weapon=0, ac=13):
        weapon = self.weapons[weapon]
        num_attacks = 1 if self.level < 5 else 2 if self.level < 11 else 3 if self.level < 20 else 4
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
                damage += weapon.attack(self.abilities, re_roll)
                if self.style == Options.DUELING and weapon.properties != Weapons.two_handed:
                    damage += 2
                if i == num_attacks - 1 and dual_wield and self.style != Options.TWO_WEAPON_FIGHTING:
                    damage -= (bonus - self.proficiency_bonus)
        return damage

# Ragnar_McRyan = Fighter(12, Race.HALF_ELF, Options.BATTLEMASTER, Options.DEFENSE)
# print(Ragnar_McRyan)
