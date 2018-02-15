monster = {1: [2, 13, 85, 3, 11, False],
           2: [2, 13, 100, 3, [8, 11], False],
           3: [2, 13, 59, 7, [10, 14], False],
           4: [2, 12, 85, 7, [14, 14], False],
           5: [3, 13, 105, 8, [18, 21], False],
           6: [3, 14, 114, 7, [11, 10, 11], [5,  15, 31]],
           7: [3, 17, 126, 9, [19, 19], False],
           8: [3, 15, 138, 9, [25, 25], False],
           9: [4, 18, 162, 11, [28, 28], False],
           10: [4, 17, 220, 7, [32, 32], False],
           11: [4, 17, 235, 8, [23, 23, 24], False],
           12: [4, 17, 250, 8, [25, 25, 25], False],
           13: [5, 18, 265, 8, [26, 27, 27], False],
           14: [5, 18, 280, 8, [30, 30, 30], False],
           15: [5, 18, 295, 8, 95, False],
           16: [5, 18, 310, 9, 102, False],
           17: [6, 19, 325, 10, 108, False],
           18: [6, 19, 340, 10, 113, False],
           19: [6, 19, 355, 10, 119, False],
           20: [6, 19, 400, 10, 140, False]}

import pickle

with open('monster_block', 'wb') as file_out:
    pickle.dump(monster, file_out)