from enum import IntEnum
from Races import Race
from PC_Classes import PCClass
from Spells import half_caster_slots
__author__ = 'faith_grins'


class Options(IntEnum):
    DUELING = 0
    ARCHERY = 1
    DEFENSE = 2
    TWO_WEAPON_FIGHTING = 3
    BEASTMASTER = 4
    HUNTER = 5
    COLOSSUS_SLAYER = 6
    HORDEBREAKER = 7


class Ranger(PCClass):

    def __init__(self, level: int, race: Race, *options, starting_array=None):
        if not starting_array:
            starting_array = [12, 15, 14, 10, 13, 8]
        PCClass.__init__(self, race, level, [1, 2, 4, 3, 0, 5], starting_array)
        #   Set Hit Points
        self.max_hp = 10 + 6 * (level - 1) + self.con_mod()*level
        self.current_hp = self.max_hp
        #   Set Hit Dice
        self.max_hit_dice = level
        self.current_hit_dice = self.max_hit_dice
        self.hit_die = Dice_Rolling.d10
        #   Set fighting style.  Defaults to Dueling if not provided.
        self.style = None
        if level >= 2:
            for o in Options:
                if o in options and o < Options.BEASTMASTER:
                    self.style = o
                    break
            if not self.style:
                self.style = Options.DUELING
        #   Set Oath.  Defaults to Ancients if not provided.
        self.archetype = None
        if level >= 3:
            for o in Options:
                if o in options and (o == Options.BEASTMASTER or o == Options.HUNTER):
                    self.archetype = o
                    break
            if not self.archetype:
                self.oath = Options.BEASTMASTER
        #   Handle Spells/spell slots.
        self.spell_slots = half_caster_slots(level)

    def __str__(self):
        return str({'level': self.level, 'archetype': self.archetype, 'style': self.style,
                    'abilities': self.abilities, 'race': self.race, 'spells': self.spell_slots})