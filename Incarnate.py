from enum import IntEnum
from Races import Race, ability_adjustment
from PC_Classes import PCClass
from Spells import half_caster_slots
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
        #   Set Hit Dice
        self.max_hit_dice = level
        self.current_hit_dice = self.max_hit_dice
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
        return str({'level': self.level, 'legacy': self.legacy, 'style': self.style,
                    'abilities': self.abilities, 'race': self.race, 'spells': self.spell_slots})

    def set_weapons(self, weapons: list):
        self.weapons = weapons

    def attack(self, weapon=0, ac=13):
        weapon = self.weapons[weapon]
        num_attacks = 1 if self.level < 5 or self.legacy == Options.AVATAR else 2
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
                if self.level >= 7 and self.current_essentia > 0:
                    max_bonus = 2
                    while self.current_essentia > 0 and max_bonus > 0:
                        max_bonus -= 1
                        self.current_essentia -= 1
                        hit += choice(Dice_Rolling.d8)
                if i == num_attacks - 1 and dual_wield:
                    hit -= (bonus - self.proficiency_bonus)
                damage += hit
        return damage


# Hank_Defender_of_Peanut_Butter = Paladin(12, Race.HALF_ELF, Options.OATH_OF_VENGEANCE, Options.DEFENSE)
# print(Hank_Defender_of_Peanut_Butter)
