from app.helpers import *
import pandas


class Draft:
    def __init__(self, teams, rounds):
        self.teams = teams
        self.rounds = rounds
        self.rosters = {}


class Team(Draft):
    def __init__(self, teams, rounds, pos, name, user):
        super().__init__(teams, rounds)
        self.players = []
        self.nextPick = pos
        self.draftPos = pos
        self.name = name
        self.user = user
        self.count = 0
        self.qbs = 0
        self.rbs = 0
        self.wrs = 0
        self.tes = 0

    def completePick(self, df, player, position):
        print(self.name + " selected " + player)

        self.players.append(player)
        self.count += 1

        if position == 'QB':
            self.qbs += 1
            playerName = df.columns.values[1]
            df.drop(df[df[playerName] == player].index, inplace=True)
            df.to_csv('qbs.csv', index=False)
        elif position == 'RB':
            self.rbs += 1
            playerName = df.columns.values[1]
            df.drop(df[df[playerName] == player].index, inplace=True)
            df.to_csv('rbs.csv', index=False)
        elif position == 'WR':
            self.wrs += 1
            playerName = df.columns.values[1]
            df.drop(df[df[playerName] == player].index, inplace=True)
            df.to_csv('wrs.csv', index=False)
        elif position == 'TE':
            self.tes += 1
            playerName = df.columns.values[1]
            df.drop(df[df[playerName] == player].index, inplace=True)
            df.to_csv('tes.csv', index=False)

    def pick(self):
        qbtable = pandas.read_csv('qbs.csv')
        rbtable = pandas.read_csv('rbs.csv')
        wrtable = pandas.read_csv('wrs.csv')
        tetable = pandas.read_csv('tes.csv')

        if self.count % 2 == 0:
            self.nextPick = (self.teams-self.draftPos)*2+1
        else:
            self.nextPick = self.draftPos*2+1

        # key = playerName, value = valueAdded, pos = position
        qbvalue = qbvalueAdded(qbtable, self.nextPick, self.count+1)
        rbvalue = rbvalueAdded(rbtable, self.nextPick, self.count+1)
        wrvalue = wrvalueAdded(wrtable, self.nextPick, self.count+1)
        tevalue = tevalueAdded(tetable, self.nextPick, self.count+1)

        if self.qbs >= 1:
            newqb = (qbvalue[0], 0.1*qbvalue[1], qbvalue[2])
        else:
            newqb = qbvalue

        if self.rbs - self.wrs >= 2 or self.rbs >= 3:
            newrb = (rbvalue[0], 0.1*rbvalue[1], rbvalue[2])
        else:
            newrb = rbvalue

        if self.wrs - self.rbs >= 2 or self.wrs >= 3:
            newwr = (wrvalue[0], 0.1*wrvalue[1], wrvalue[2])
        else:
            newwr = wrvalue

        if self.tes >= 1:
            newte = (tevalue[0], 0.1*0.6*tevalue[1], tevalue[2])
        else:
            newte = (tevalue[0], 0.6*tevalue[1], tevalue[2])

        vals = [newqb, newrb, newwr, newte]
        res = 0
        for pair in vals:
            if pair[1] > res:
                res = pair[1]
                player = pair[0]
                position = pair[2]

        if position == 'QB':
            self.completePick(qbtable, player, 'QB')
        elif position == 'RB':
            self.completePick(rbtable, player, 'RB')
        elif position == 'WR':
            self.completePick(wrtable, player, 'WR')
        elif position == 'TE':
            self.completePick(tetable, player, 'TE')

    def prompt(self):
        qbtable = pandas.read_csv('qbs.csv')
        rbtable = pandas.read_csv('rbs.csv')
        wrtable = pandas.read_csv('wrs.csv')
        tetable = pandas.read_csv('tes.csv')

        if self.count % 2 == 0:
            self.nextPick = (self.teams-self.draftPos)*2+1
        else:
            self.nextPick = self.draftPos*2+1

        while True:
            print("It's " + self.name + " turn to pick.")
            search = input("Search by position, or type ALL: ")
            count = input("Number of players displayed: ")

            if search.lower() == 'qb':
                lst = qbPicks(qbtable, count)

                for tup in lst:
                    print(tup[0] + "|" + tup[1] + "|" + str(tup[2]) + " PPG")

                pick = input("Select a player by last name, or BACK: ")
                if pick.lower() != 'back':
                    picked = False
                    for tup in lst:
                        temp = tup[0].split(" ")
                        if pick.lower() == temp[1].lower():
                            picked = True
                            player = tup[0]

                            self.completePick(qbtable, player, 'QB')
                            break

                    if picked:
                        break
                    else:
                        print("No player from set selected.")

            elif search.lower() == 'rb':
                lst = otherPicks(rbtable, count)

                for tup in lst:
                    print(tup[0] + "|" + tup[1] + "|" + str(tup[2]) + " PPG|" +
                          str(tup[3]) + " OppPG")

                pick = input("Select a player by last name, or BACK: ")
                if pick.lower() != 'back':
                    picked = False
                    for tup in lst:
                        newstr = tup[0].replace("*", "")
                        newstr2 = newstr.replace("+", "")
                        temp = newstr2.split(" ")
                        if pick.lower() == temp[1].lower():
                            picked = True
                            player = tup[0]

                            self.completePick(rbtable, player, 'RB')

                    if picked:
                        break
                    else:
                        print("No player from set selected.")

            elif search.lower() == 'wr':
                lst = otherPicks(wrtable, count)

                for tup in lst:
                    print(tup[0] + "|" + tup[1] + "|" + str(tup[2]) + " PPG|" +
                          str(tup[3]) + " TgtsPG")

                pick = input("Select a player by last name, or BACK: ")
                if pick.lower() != 'back':
                    picked = False
                    for tup in lst:
                        newstr = tup[0].replace("*", "")
                        newstr2 = newstr.replace("+", "")
                        temp = newstr2.split(" ")
                        if pick.lower() == temp[1].lower():
                            picked = True
                            player = tup[0]

                            self.completePick(wrtable, player, 'WR')

                    if picked:
                        break
                    else:
                        print("No player from set selected.")

            elif search.lower() == 'te':
                lst = otherPicks(tetable, count)

                for tup in lst:
                    print(tup[0] + "|" + tup[1] + "|" + str(tup[2]) + " PPG|" +
                          str(tup[3]) + " TgtsPG")

                pick = input("Select a player by last name, or BACK: ")
                if pick.lower() != 'back':
                    picked = False
                    for tup in lst:
                        newstr = tup[0].replace("*", "")
                        newstr2 = newstr.replace("+", "")
                        temp = newstr2.split(" ")
                        if pick.lower() == temp[1].lower():
                            picked = True
                            player = tup[0]

                            self.completePick(tetable, player, 'TE')

                    if picked:
                        break
                    else:
                        print("No player from set selected.")
