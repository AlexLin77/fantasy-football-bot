
def qbvalueAdded(df, nextPick, rd):
    # drop titles row
    df = df.iloc[1:]

    # when less available players
    if nextPick+1 > len(df):
        comps = len(df)
    else:
        comps = nextPick+1

    for i in range(comps):
        if i == 0:
            firstPPG = df.iat[i, 4]
            secondPPG = df.iat[i, 4]
        # before round 5, ~1 QB per rotation
        if rd < 5:
            target = int(max(round(1/20 * nextPick), 1))
            if i == target:
                secondPPG = df.iat[target, 4]
        # after round 5, ~3 QB per rotation
        else:
            target = int(max(round(3/20 * nextPick), 1))
            if i == target:
                secondPPG = df.iat[target, 4]

    diff = float(firstPPG) - float(secondPPG)

    return (df.iat[0, 1], diff, 'QB')


def rbvalueAdded(df, nextPick, rd):
    # drop titles row
    df = df.iloc[1:]

    # when less available players
    if nextPick+1 > len(df):
        comps = len(df)
    else:
        comps = nextPick+1

    temp = {}
    for i in range(comps):
        ppg = df.iat[i, 4]
        opp = df.iat[i, 5]
        temp[i] = float(ppg) + float(0.2*opp)

    values = {}
    values_keys = sorted(temp, key=temp.get, reverse=True)
    for k in values_keys:
        values[k] = temp[k]

    for index, key in enumerate(values):
        if index == 0:
            # use marker to save key of best RB so we can retrieve name later
            firstPPG = values[key]
            secondPPG = values[key]
            marker = key
        if rd == 1:
            target = int(round(14/20 * nextPick))
            if index == target:
                secondPPG = values[key]
        if rd == 2:
            target = int(max(round(9/20 * nextPick), 1))
            if index == target:
                secondPPG = values[key]
        else:
            target = int(max(round(6.5/20 * nextPick), 1))
            if index == target:
                secondPPG = values[key]

    diff = float(firstPPG) - float(secondPPG)

    return (df.iat[marker, 1], diff, 'RB')


def wrvalueAdded(df, nextPick, rd):
    # drop titles row
    df = df.iloc[1:]

    # when less available players
    if nextPick+1 > len(df):
        comps = len(df)
    else:
        comps = nextPick+1

    temp = {}
    for i in range(comps):
        ppg = df.iat[i, 4]
        opp = df.iat[i, 5]
        temp[i] = float(ppg) + float(0.5*opp)

    values = {}
    values_keys = sorted(temp, key=temp.get, reverse=True)
    for k in values_keys:
        values[k] = temp[k]

    for index, key in enumerate(values):
        if index == 0:
            firstPPG = values[key]
            secondPPG = values[key]
            marker = key
        if rd < 3:
            target = int(max(round(6/20 * nextPick), 1))
            if index == target:
                secondPPG = values[key]
        if rd >= 3 and rd < 6:
            target = int(round(11/20 * nextPick))
            if index == target:
                secondPPG = values[key]
        if rd >= 6:
            target = int(max(round(7/20 * nextPick), 1))
            if index == target:
                secondPPG = values[key]

    diff = float(firstPPG) - float(secondPPG)

    return (df.iat[marker, 1], diff, 'WR')


def tevalueAdded(df, nextPick, rd):
    # drop titles row
    df = df.iloc[1:]

    # when less available players
    if nextPick+1 > len(df):
        comps = len(df)
    else:
        comps = nextPick+1

    temp = {}
    for i in range(comps):
        ppg = df.iat[i, 4]
        opp = df.iat[i, 5]
        temp[i] = float(ppg) + float(0.3*opp)

    values = {}
    values_keys = sorted(temp, key=temp.get, reverse=True)
    for k in values_keys:
        values[k] = temp[k]

    for index, key in enumerate(values):
        if index == 0:
            firstPPG = values[key]
            secondPPG = values[key]
            marker = key
        if rd < 5:
            target = int(max(round(1/20 * nextPick), 1))
            if index == target:
                secondPPG = values[key]
        if rd == 5:
            target = int(max(round(2/20 * nextPick), 1))
            if index == target:
                secondPPG = values[key]
        else:
            target = int(max(round(3/20 * nextPick), 1))
            if index == target:
                secondPPG = values[key]

    diff = float(firstPPG) - float(secondPPG)

    return (df.iat[marker, 1], diff, 'TE')
