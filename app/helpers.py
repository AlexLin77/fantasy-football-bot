
def qbvalueAdded(df, nextPick, rd):
    # drop titles row
    df = df.iloc[1:]

    firstPPG = df.iat[0, 4]
    # before round 5, ~1 QB per rotation
    if rd < 5:
        secondPPG = df.iat[1, 4]
    # after round 5, ~3 QB per rotation
    else:
        secondPPG = df.iat[3, 4]
    diff = float(firstPPG) - float(secondPPG)

    return (df.iat[0, 1], diff, 'QB')


def rbvalueAdded(df, nextPick, rd):
    # drop titles row
    df = df.iloc[1:]

    values = {}
    for i in range(nextPick+1):
        ppg = df.iat[i, 4]
        opp = df.iat[i, 5]
        values[i] = float(ppg) + float(0.2*opp)

    # sort by combined performance & opportunity value
    sorted(values.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)

    if rd == 1:
        target = int(round(14/20 * nextPick))
        for index, key in enumerate(values):
            if index == 0:
                # use marker to save key of best RB so we can retrieve name later
                firstPPG = values[key]
                marker = key
            if index == target:
                secondPPG = values[key]
    elif rd == 2:
        target = int(round(9/20 * nextPick))
        for index, key in enumerate(values):
            if index == 0:
                firstPPG = values[key]
                secondPPG = values[key]
                marker = key
            if index == target:
                secondPPG = values[key]
    else:
        target = int(round(6.5/20 * nextPick))
        for index, key in enumerate(values):
            if index == 0:
                firstPPG = values[key]
                secondPPG = values[key]
                marker = key
            if index == target:
                secondPPG = values[key]

    diff = float(firstPPG) - float(secondPPG)

    return (df.iat[marker, 1], diff, 'RB')


def wrvalueAdded(df, nextPick, rd):
    # drop titles row
    df = df.iloc[1:]

    values = {}
    for i in range(nextPick+1):
        ppg = df.iat[i, 4]
        opp = df.iat[i, 5]
        values[i] = float(ppg) + float(0.5*opp)

    sorted(values.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)

    for index, key in enumerate(values):
        if index == 0:
            firstPPG = values[key]
            secondPPG = values[key]
            marker = key
        if rd < 3:
            target = int(round(6/20 * nextPick))
            if index == target:
                secondPPG = values[key]
        if rd >= 3 and rd < 6:
            target = int(round(11/20 * nextPick))
            if index == target:
                secondPPG = values[key]
        if rd >= 6:
            target = int(round(7/20 * nextPick))
            if index == target:
                secondPPG = values[key]

    diff = float(firstPPG) - float(secondPPG)

    return (df.iat[marker, 1], diff, 'WR')


def tevalueAdded(df, nextPick, rd):
    # drop titles row
    df = df.iloc[1:]

    values = {}
    for i in range(nextPick+1):
        ppg = df.iat[i, 4]
        opp = df.iat[i, 5]
        values[i] = float(ppg) + float(0.3*opp)

    sorted(values.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)

    for index, key in enumerate(values):
        if index == 0:
            firstPPG = values[key]
            secondPPG = values[key]
            marker = key
        if rd < 5:
            target = int(round(1/20 * nextPick))
            if index == target:
                secondPPG = values[key]
        if rd == 5:
            target = int(round(2/20 * nextPick))
            if index == target:
                secondPPG = values[key]
        else:
            target = int(round(3/20 * nextPick))
            if index == target:
                secondPPG = values[key]

    diff = float(firstPPG) - float(secondPPG)

    return (df.iat[marker, 1], diff, 'TE')
