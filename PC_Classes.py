from Races import Race, ability_adjustment
from enum import IntEnum
__author__ = 'faith_grins'


class Actions(IntEnum):
    ATTACK = 0
    DODGE = 1
    DASH = 2
    DISENGAGE = 3
    HIDE = 4
    CAST_SPELL = 5


class Conditions(IntEnum):
    DODGE = 0
    PRONE = 1
    GRAPPLED = 2
    RESTRAINED = 3
    STUNNED = 4
    PETRIFIED = 5
    CHARMED = 6


class ClassList(IntEnum):
    BARBARIAN = 0
    BARD = 1
    CLERIC = 2
    DRUID = 3
    FIGHTER = 4
    MONK = 5
    PALADIN = 6
    RANGER = 7
    ROGUE = 8
    SORCERER = 9
    WARLOCK = 10
    WIZARD = 11


class PCClass:
    def __init__(self, race: Race, level: int, priorities: list, starting_array: list, class_marker=ClassList.FIGHTER):
        self.race = race
        self.level = level
        # Do race adjustments before ASIs
        self.abilities = ability_adjustment(race, starting_array)
        #   Handle ability score increases.
        asi = 0
        if level >= 4:
            asi += 2
        if level >= 6 and class_marker == ClassList.FIGHTER:
            asi += 2
        if level >= 8:
            asi += 2
        if level >= 10 and class_marker == ClassList.ROGUE:
            asi += 2
        if level >= 12:
            asi += 2
        if level >= 14 and class_marker == ClassList.FIGHTER:
            asi += 2
        if level >= 16:
            asi += 2
        if level >= 19:
            asi += 2
        while asi > 0:
            asi -= 1
            for p in priorities:
                # TODO: make this a little less naive. (E.g.:  make better use of odd values.)
                if self.abilities[p] < 20:
                    self.abilities[p] += 1
                    break
        self.actions = {}
        self.proficiency_bonus = 2 if self.level < 5 else 3 if self.level < 9 else 4 if self.level < 13 else 5 if self.level < 17 else 6
        self.temp_hit_points = 0
        self.max_hit_dice = level
        self.current_hit_dice = self.max_hit_dice
        self.conditions = []

    def __str__(self):
        return str({'level': self.level, 'abilities': self.abilities, 'race': self.race})

    def str_mod(self):
        return -5 + (self.abilities[0] // 2)

    def dex_mod(self):
        return -5 + (self.abilities[1] // 2)

    def con_mod(self):
        return -5 + (self.abilities[2] // 2)

    def int_mod(self):
        return -5 + (self.abilities[3] // 2)

    def wis_mod(self):
        return -5 + (self.abilities[4] // 2)

    def cha_mod(self):
        return -5 + (self.abilities[5] // 2)

    def initiative(self):
        if Conditions.DODGE in self.conditions:
            self.conditions.remove(Conditions.DODGE)
