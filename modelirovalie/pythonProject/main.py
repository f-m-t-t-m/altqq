import copy


if __name__ == '__main__':
    table = [
        [-1, 3, 10],
        [1, 1, 6],
        [1, -1, 3],
        [-1, -4, -4],
        [1, 2, 0]
    ]

    resolving_column = None
    print(table)
    max = table[4][0]
    if table[4][1] > max:
        max = table[4][1]
        if max > 0:
            resolving_column = 1
    elif max > 0:
        resolving_column = 0

    while resolving_column is not None:
        resolving_stroke = None
        min = float('inf')
        for i in range(4):
            if 0 < table[i][2] / table[i][resolving_column] < min:
                min = table[i][2] / table[i][resolving_column]
                resolving_stroke = i
        print(resolving_stroke)
        print(resolving_column)
        print()
        if resolving_stroke is None:
            break

        newTable = copy.deepcopy(table)
        newTable[resolving_stroke][resolving_column] = 1 / table[resolving_stroke][resolving_column]
        for j in range(3):
            if j == resolving_column:
                continue
            newTable[resolving_stroke][j] /= table[resolving_stroke][resolving_column]

        for i in range(5):
            if i == resolving_stroke:
                continue
            newTable[i][resolving_column] = -(table[i][resolving_column] / table[resolving_stroke][resolving_column])

        for i in range(5):
            for j in range(3):
                if i == resolving_stroke or j == resolving_column:
                    continue
                newTable[i][j] -= table[resolving_stroke][j] * table[i][resolving_column] / table[resolving_stroke][resolving_column]
        resolving_column = None
        table = newTable
        max = table[4][0]
        if table[4][1] >= max:
            max = table[4][1]
            if max > 0:
                resolving_column = 1
        elif max > 0:
            resolving_column = 0

        for i in table:
            print(i)
        print()

