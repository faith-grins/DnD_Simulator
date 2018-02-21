from enum import IntEnum
from Races import Race, ability_adjustment
from PC_Classes import PCClass, Conditions
from Spells import psi_points
from random import choice
import Dice_Rolling
import Weapons
__author__ = 'faith_grins'


class Options(IntEnum):
    IMMORTAL = 0
    AVATAR = 1
    SOULKNIFE = 2
    NOMAD = 3
    WUJEN = 4


class Incarnate(PCClass):

    def __init__(self, level: int, race: Race, *options, starting_array=None):
        if not starting_array:
            starting_array = [15, 12, 13, 8, 10, 14]
        PCClass.__init__(self, race, level, [0, 2, 5, 1, 4, 3], starting_array)
        #   Set Hit Points
        self.max_hp = 8 + 5 * (level - 1) + self.con_mod()*level
        self.current_hp = self.max_hp
        #   Set Hit Die
        self.hit_die = Dice_Rolling.d8
        #   Set max Psi points
        self.max_psi = psi_points(level)
        self.current_psi = self.max_psi
        #   Set Tradition.  Defaults to Immortal
        self.tradition = None
        for o in Options:
            if o in options and o >= Options.IMMORTAL:
                self.tradition = o
        if not self.tradition:
            self.tradition = Options.IMMORTAL
        #   Gear.  Defaults to a spear, leather armor, and a shield
        self.weapons = []
        self.weapons.append(Weapons.spear)
        self.AC = 11 + self.dex_mod()
        if self.tradition == Options.IMMORTAL:
            self.AC = 10 + self.dex_mod() + self.con_mod()
        #   Talents TODO:  Implement this properly
        self.talents = []
        #   Disciplines TODO:  Implement this properly
        self.disciplines = []

    def __str__(self):
        return str({'level': self.level, 'legacy': self.tradition, 'talents': self.talents, 'psi points': self.max_psi,
                    'abilities': self.abilities, 'race': self.race, 'disciplines': self.disciplines})

    def set_weapons(self, weapons: list):
        self.weapons = weapons

    def action(self, command=None):
        if not command:
            command ==
        if command == 'dodge':
            self.conditions.append(Conditions.DODGE)

    def attack(self, weapon=0, ac=13, num_attacks=1):
        weapon = self.weapons[weapon]
        dual_wield = False
        if weapon == Weapons.shortsword:
            num_attacks += 1
            dual_wield = True
        damage = 0
        bonus = self.proficiency_bonus + weapon.primary_mod(self.abilities)
        for i in range(num_attacks):
            attack_roll = choice(Dice_Rolling.d20) + bonus
            if attack_roll >= ac:
                hit = weapon.attack(self.abilities)
                if i == num_attacks - 1 and dual_wield:
                    hit -= (bonus - self.proficiency_bonus)
                damage += hit
        return damage

    def long_rest(self):
        self.current_hp = self.max_hp
        self.current_psi = self.max_psi
        self.current_hit_dice = max(self.max_hit_dice, self.current_hit_dice + self.max_hit_dice//2)

    def short_rest(self):
        average_recovery = sum(self.hit_die) / len(self.hit_die) + self.con_mod()
        while self.current_hp < self.max_hp - average_recovery and self.current_hit_dice > 0:
            self.current_hit_dice -= 1
            self.current_hp += choice(self.hit_die) + self.con_mod()
