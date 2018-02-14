from Fighter import Fighter
from Fighter import Options as FighterOptions
from Paladin import Paladin
from Paladin import Options as PaladinOptions
from Monk import Monk
from Ranger import Ranger
import Races

bram = Fighter(8, Races.Race.HUMAN, FighterOptions.GREAT_WEAPON_FIGHTING, starting_array=[15, 13, 15, 9, 10, 9])
kane = Paladin(8, Races.Race.HUMAN, FighterOptions.GREAT_WEAPON_FIGHTING, starting_array=[15, 13, 15, 9, 10, 9])
ragnar = Fighter(12, Races.Race.HUMAN, FighterOptions.GREAT_WEAPON_FIGHTING, starting_array=[15, 13, 15, 9, 10, 9])
butterbeer = Paladin(12, Races.Race.HUMAN, PaladinOptions.GREAT_WEAPON_FIGHTING, starting_array=[15, 9, 15, 9, 10, 13])
dinglendingle = Monk(12, Races.Race.STOUT_HALFLING, starting_array=[8, 14, 13, 12, 14, 12])
tak = Monk(8, Races.Race.STOUT_HALFLING, starting_array=[8, 14, 13, 12, 14, 12])
n = 18000
comparisons = {bram: [], kane: [], tak: [], ragnar: [], butterbeer: [], dinglendingle: []}
for character in comparisons:
    for _ in range(n):
        comparisons[character].append(character.attack())
    comparisons[character].sort()
    print(character)
    print('Min result: {0}\nMax result: {1}\nMedian result: {2}\nMean: {3}'.format(min(comparisons[character]),
            max(comparisons[character]), comparisons[character][n//2], sum(comparisons[character])/n))
    print()
    print()
