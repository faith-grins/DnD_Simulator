from enum import IntEnum
__author__ = 'faith_grins'


class Race(IntEnum):
    HUMAN = 0
    HALF_ELF = 1
    HALF_ORC = 2
    DRAGONBORN = 3
    TIEFLING = 4
    HILL_DWARF = 5
    MOUNTAIN_DWARF = 6
    STOUT_HALFLING = 7
    LIGHT_HALFLING = 8
    FOREST_GNOME = 9
    ROCK_GNOME = 10
    WOOD_ELF = 11
    HIGH_ELF = 12


def ability_adjustment(race: Race, abilities: list):
    if race == Race.HUMAN:
        return [i+1 for i in abilities]
    if race == Race.HALF_ELF:
        abilities[5] += 2
        bonus = 2
        while any(i % 2 == 1 for i in abilities) and bonus > 0:
            abilities[abilities.index(max([i for i in abilities if i % 2 == 1]))] += 1
            bonus -= 1
        if bonus > 0:
            for i in range(bonus):
                abilities[bonus] += 1
        return abilities
    race_mods = {0: {Race.HALF_ORC: 2, Race.DRAGONBORN: 2, Race.MOUNTAIN_DWARF: 2},
                 1: {Race.STOUT_HALFLING: 2, Race.LIGHT_HALFLING: 2, Race.FOREST_GNOME: 1,
                     Race.WOOD_ELF: 2, Race.HIGH_ELF: 2},
                 2: {Race.HALF_ORC: 1, Race.MOUNTAIN_DWARF: 2, Race.HILL_DWARF: 2,
                     Race.STOUT_HALFLING: 1, Race.ROCK_GNOME: 1},
                 3: {Race.TIEFLING: 1, Race.ROCK_GNOME: 2, 10: Race.FOREST_GNOME, 12: 1},
                 4: {Race.WOOD_ELF: 1, Race.HILL_DWARF: 1},
                 5: {Race.DRAGONBORN: 1, Race.TIEFLING: 2, Race.LIGHT_HALFLING: 1}}
    for i in race_mods:
        if race in race_mods[i]:
            abilities[i] += race_mods[i][race]
    return abilities
