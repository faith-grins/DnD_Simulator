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
        #   Set Hit Points
        self.max_hp = 10 + 6 * (level - 1) + self.con_mod()*level
        self.current_hp = self.max_hp
        #   Set Hit Dice
        self.max_hit_dice = level
        self.current_hit_dice = self.max_hit_dice
        self.hit_die = Dice_Rolling.d10
        #   Set fighting style.  Defaults to Dueling if not provided.
        self.style = None
        for o in options:
            if o in Options and o < Options.CHAMPION:
                self.style = o
        if not self.style:
            self.style = Options.DUELING
        #   Set Archetype.  Defaults to Champion if not provided.
        self.max_superiority_dice = 0
        self.archetype = None
        if level >= 3:
            for o in Options:
                if o in options and o >= Options.CHAMPION:
                    self.archetype = o
            if not self.archetype:
                self.archetype = Options.CHAMPION
        if self.archetype == Options.BATTLEMASTER:
            self.max_superiority_dice = 4 if level < 10 else 5
            self.superiority_die = Dice_Rolling.d8 if level < 10 else Dice_Rolling.d10
        self.current_superiority_dice = self.max_superiority_dice
        #   Handle Spells/spell slots.
        if self.archetype == Options.ELDRITCH_KNIGHT:
            self.max_spell_slots = one_third_caster_slots(level)
        else:
            self.max_spell_slots = None
        self.current_spell_slots = self.max_spell_slots
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

    def long_rest(self):
        self.current_hp = self.max_hp
        self.current_hit_dice = max(self.max_hit_dice, self.current_hit_dice + self.max_hit_dice//2)


    def short_rest(self):
        average_recovery = sum(self.hit_die) / len(self.hit_die) + self.con_mod()
        while self.current_hp < self.max_hp - average_recovery and self.current_hit_dice > 0:
            self.current_hit_dice -= 1
            self.current_hp += choice(self.hit_die) + self.con_mod()

# Ragnar_McRyan = Fighter(12, Race.HALF_ELF, Options.BATTLEMASTER, Options.DEFENSE)
# print(Ragnar_McRyan)
