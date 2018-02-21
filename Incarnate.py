from enum import IntEnum
from Races import Race, ability_adjustment
from PC_Classes import PCClass
from random import choice
import Dice_Rolling
import Weapons
__author__ = 'faith_grins'


class Options(IntEnum):
    SOULBORN = 0
    AVATAR = 1
    TOTEMIST = 2


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
        #   Set max Essentia
        if level >= 2:
            self.max_essentia = level
        else:
            self.max_essentia = 0
        self.current_essentia = self.max_essentia
        #   Set Legacy.  Defaults to Soulborn
        self.legacy = None
        if level >= 3:
            for o in Options:
                if o in options and o >= Options.SOULBORN:
                    self.legacy = o
            if not self.legacy:
                self.legacy = Options.SOULBORN
        # Gear.  Defaults to a spear, scale mail, and a shield
        self.weapons = []
        if level >= 3 and self.legacy == Options.SOULBORN:
            self.weapons.append(Weapons.battleaxe)
        else:
            self.weapons.append(Weapons.spear)
        self.AC = max(12 + self.dex_mod(), 14 + max(2, self.dex_mod())) + 2
        if self.legacy == Options.SOULBORN:
            if self.level >= 5:
                self.AC = 20
            else:
                self.AC = 19

    def __str__(self):
        return str({'level': self.level, 'legacy': self.legacy, 'abilities': self.abilities, 'race': self.race,
                    'essentia': self.max_essentia})

    def set_weapons(self, weapons: list):
        self.weapons = weapons

    def attack(self, weapon=0, offhand=None, ac=13):
        weapon = self.weapons[weapon]
        num_attacks = 1 if self.level < 5 or self.legacy == Options.AVATAR else 2
        if offhand:
            offhand = self.weapons[offhand]
            dual_wield = True
            num_attacks += 1
        else:
            dual_wield = False
        damage = 0
        for i in range(num_attacks):
            attack_roll = choice(Dice_Rolling.d20) + self.proficiency_bonus + weapon.primary_mod(self.abilities)
            this_weapon = weapon if i < (num_attacks - 1) else offhand
            bonus = this_weapon.primary_mod(self.abilities)
            if attack_roll >= ac:
                hit = this_weapon.attack(self.abilities)
                if self.level >= 7 and self.current_essentia > 0:
                    max_bonus = 2
                    while self.current_essentia > 0 and max_bonus > 0:
                        max_bonus -= 1
                        self.current_essentia -= 1
                        hit += choice(Dice_Rolling.d8)
                if i == num_attacks - 1 and dual_wield:
                    hit -= bonus
                damage += hit
        return damage

    def long_rest(self):
        self.current_hp = self.max_hp
        self.current_essentia = self.max_essentia
        self.current_hit_dice = max(self.max_hit_dice, self.current_hit_dice + self.max_hit_dice//2)

    def short_rest(self):
        self.current_essentia = self.max_essentia
        average_recovery = sum(self.hit_die) / len(self.hit_die) + self.con_mod()
        while self.current_hp < self.max_hp - average_recovery and self.current_hit_dice > 0:
            self.current_hit_dice -= 1
            self.current_hp += choice(self.hit_die) + self.con_mod()
