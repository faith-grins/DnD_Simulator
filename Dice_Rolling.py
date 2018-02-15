from random import choice

d4 = [1, 2, 3, 4]
d6 = [1, 2, 3, 4, 5, 6]
d8 = [1, 2, 3, 4, 5, 6, 7, 8]
d10 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
d12 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
d20 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]


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
