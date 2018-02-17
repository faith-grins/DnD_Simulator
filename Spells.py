from math import ceil
__author__ = 'faith_grins'


# TODO:  properly implement this
def full_caster_slots(level: int):
    return {1: min(4, ceil(level / 2) + 1) if level >= 2 else 0,
            2: min(3, ceil(level / 2) - 1) if level >= 5 else 0,
            3: min(3, ceil(level / 2) - 3) if level >= 9 else 0,
            4: min(3, ceil(level / 2) - 6) if level >= 13 else 0,
            5: min(2, ceil(level / 2) - 8) if level >= 17 else 0}


def half_caster_slots(level: int):
    return {1: min(4, ceil(level / 2) + 1) if level >= 2 else 0,
            2: min(3, ceil(level / 2) - 1) if level >= 5 else 0,
            3: min(3, ceil(level / 2) - 3) if level >= 9 else 0,
            4: min(3, ceil(level / 2) - 6) if level >= 13 else 0,
            5: min(2, ceil(level / 2) - 8) if level >= 17 else 0}


# TODO:  properly implement this
def one_third_caster_slots(level: int):
    return {1: min(4, ceil(level / 2) + 1) if level >= 2 else 0,
            2: min(3, ceil(level / 2) - 1) if level >= 5 else 0,
            3: min(3, ceil(level / 2) - 3) if level >= 9 else 0,
            4: min(3, ceil(level / 2) - 6) if level >= 13 else 0}


def psi_points(level: int):
    return [0, 4, 6, 14, 17, 27, 32, 38, 44, 57, 64,
            64, 64, 64, 64, 64, 64, 64, 71, 71, 71][level]
