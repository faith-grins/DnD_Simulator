from random import choice

d4 = range(1, 5)
d6 = range(1, 7)
d8 = range(1, 9)
d10 = range(1, 11)
d12 = range(1, 13)
d20 = range(1, 21)


def __test():
    six = range(1, 7)
    one_die = []
    two_dice = []
    for _ in range(10000):
        rolls = [choice(six), choice(six), choice(six)]
        three_d6 = sum(rolls) % 6
        # twod6 = (sum(rolls) % 3 + 3*sum(rolls) % 5) % 6
        one_die.append(three_d6)
        # twodice.append(twod6)
    # print(sum(twodice)/len(twodice))
    print(sum(one_die)/len(one_die))
