#from bs4 import BeautifulSoup
#from . import helpers
import pandas
import requests
import math


def parser(url):
    df = pandas.read_html(url)[0]

    df = df.drop(df.columns[[0]], axis=1)

    return df

# create separate tables for positions


def processor(df, position):
    pos = df.columns.values[2]

    group = df[(df[pos] == position)]

    if position == 'QB':
        group = group.iloc[:, [0, 1, 2, 4, 25, 26, 30, 31]]

        # add ppg column and sort
        avg = []
        for i in range(len(group)):
            total = group.iat[i, 5]
            gamesPlayed = group.iat[i, 3]
            num = round((float(total) / float(gamesPlayed)), 2)
            avg.append(num)

        group.insert(loc=3, column='ppg', value=avg)
        group.sort_values(by=['ppg'], inplace=True, ascending=False)

        posrank = group.columns.values[len(group.columns)-2]
        group[posrank] = group[posrank].astype(int)
        group.drop(group[group[posrank] > 40].index, inplace=True)

    elif position == 'RB':
        group = group.iloc[:, [0, 1, 2, 4, 11, 15, 25, 26, 30, 31]]

        avg = []
        opp = []
        for i in range(len(group)):
            total = group.iat[i, 7]
            gamesPlayed = group.iat[i, 3]
            touches = int(group.iat[i, 4]) + int(group.iat[i, 5])

            num = round((float(total) / float(gamesPlayed)), 2)
            num2 = round((float(touches) / float(gamesPlayed)), 2)
            avg.append(num)
            opp.append(num2)

        group.insert(loc=3, column='ppg', value=avg)
        group.insert(loc=4, column='opp', value=opp)
        group.sort_values(by=['ppg'], inplace=True, ascending=False)

        posrank = group.columns.values[len(group.columns)-2]
        group[posrank] = group[posrank].astype(int)
        group.drop(group[group[posrank] > 90].index, inplace=True)

    else:
        group = group.iloc[:, [0, 1, 2, 4, 15, 25, 26, 30, 31]]

        avg = []
        opp = []
        for i in range(len(group)):
            total = group.iat[i, 6]
            gamesPlayed = group.iat[i, 3]
            tgts = group.iat[i, 4]

            num = round((float(total) / float(gamesPlayed)), 2)
            num2 = round((float(tgts) / float(gamesPlayed)), 2)
            avg.append(num)
            opp.append(num2)

        group.insert(loc=3, column='ppg', value=avg)
        group.insert(loc=4, column='opp', value=opp)
        group.sort_values(by=['ppg'], inplace=True, ascending=False)

        posrank = group.columns.values[len(group.columns)-2]
        group[posrank] = group[posrank].astype(int)
        if position == 'TE':
            group.drop(group[group[posrank] > 60].index, inplace=True)

    return group
