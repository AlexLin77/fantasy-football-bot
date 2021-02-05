from app.helpers import *
from app.data import *
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
        
        print("It's " + self.name + " turn to pick.")

        auto = input("Turn on autodraft? (Y/N) ")
        if auto.lower() == 'y':
            self.user = False
            self.pick()
        else:
            while True:
                search = input("Search by position: ")
                count = input("How many players to display? ")

                if search.lower() == 'qb':
                    lst = qbPicks(qbtable, count)

                    for tup in lst:
                        print(tup[0] + "|" + tup[1] + "|" + tup[2] + "|" 
                              + str(tup[3]) + " PPG")

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

                                self.completePick(qbtable, player, 'QB')
                                break

                        if picked:
                            break
                        else:
                            print("No player from set selected.")

                elif search.lower() == 'rb':
                    lst = otherPicks(rbtable, count)

                    for tup in lst:
                        print(tup[0] + "|" + tup[1] + "|" + tup[2] + "|" 
                        + str(tup[3]) + " PPG|" + str(tup[4]) + " OppPG")

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
                                break

                        if picked:
                            break
                        else:
                            print("No player from set selected.")

                elif search.lower() == 'wr':
                    lst = otherPicks(wrtable, count)

                    for tup in lst:
                        print(tup[0] + "|" + tup[1] + "|" + tup[2] + "|" + 
                        str(tup[3]) + " PPG|" + str(tup[4]) + " TgtsPG")

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
                                break

                        if picked:
                            break
                        else:
                            print("No player from set selected.")

                elif search.lower() == 'te':
                    lst = otherPicks(tetable, count)

                    for tup in lst:
                        print(tup[0] + "|" + tup[1] + "|" + tup[2] + "|" 
                        + str(tup[3]) + " PPG|" + str(tup[4]) + " TgtsPG")

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
                                break

                        if picked:
                            break
                        else:
                            print("No player from set selected.")
                
                else:
                    print("Not a valid position. Please enter QB, RB, WR, or TE")
      
    def entry(self):
        pick = input("Enter the selected player's last name and position: ")
        picklst = pick.split(" ")

        if picklst[1].lower() == 'qb':
            qbtable = pandas.read_csv('qbs.csv')
            lst = qbPicks(qbtable, 30)

            for tup in lst:
                newstr = tup[0].replace("*", "")
                newstr2 = newstr.replace("+", "")
                temp = newstr2.split(" ")
                if picklst[0].lower() == temp[1].lower():
                    player = tup[0]
                    self.completePick(qbtable, player, 'QB')
                    break

        elif picklst[1].lower() == 'rb':
            rbtable = pandas.read_csv('rbs.csv')
            lst = otherPicks(rbtable, 30)

            for tup in lst:
                newstr = tup[0].replace("*", "")
                newstr2 = newstr.replace("+", "")
                temp = newstr2.split(" ")
                if picklst[0].lower() == temp[1].lower():
                    player = tup[0]
                    self.completePick(rbtable, player, 'RB')
                    break

        elif picklst[1].lower() == 'wr':
            wrtable = pandas.read_csv('wrs.csv')
            lst = otherPicks(wrtable, 30)

            for tup in lst:
                newstr = tup[0].replace("*", "")
                newstr2 = newstr.replace("+", "")
                temp = newstr2.split(" ")
                if picklst[0].lower() == temp[1].lower():
                    player = tup[0]
                    self.completePick(wrtable, player, 'WR')
                    break

        elif picklst[1].lower() == 'te':
            tetable = pandas.read_csv('tes.csv')
            lst = otherPicks(tetable, 30)

            for tup in lst:
                newstr = tup[0].replace("*", "")
                newstr2 = newstr.replace("+", "")
                temp = newstr2.split(" ")
                if picklst[0].lower() == temp[1].lower():
                    player = tup[0]
                    self.completePick(tetable, player, 'TE')
                    break

 
def simulate():
    url = 'https://www.pro-football-reference.com/years/2020/fantasy.htm'

    df = parser(url)
    sub = processor(df, 'QB')
    sub2 = processor(df, 'RB')
    sub3 = processor(df, 'WR')
    sub4 = processor(df, 'TE')

    sub.to_csv('qbs.csv')
    sub2.to_csv('rbs.csv')
    sub3.to_csv('wrs.csv')
    sub4.to_csv('tes.csv')

    teams = int(input("Number of teams in the league: "))
    rounds = int(input("Number of rounds in the draft: "))
    d = Draft(teams, rounds)

    for i in range(teams):
        userControl = input(
            "Should this team be controlled by a human? (Y/N) ")
        if userControl.lower() == 'y':
            name = input("Enter a name for this team: ")
            d.rosters["team"+str(i+1)] = Team(teams, rounds, i+1, name, True)
        elif userControl.lower() == 'n':
            name = "Computer"+str(i+1)
            d.rosters["team"+str(i+1)] = Team(teams, rounds, i+1, name, False)

    for i in range(rounds):
        # print("Round: " + str(i+1))
        if i % 2 == 0:
            for i in range(len(d.rosters)):
                team = d.rosters["team"+str(i+1)]
                if team.user:
                    team.prompt()
                else:
                    team.pick()
        else:
            for i in reversed(range(len(d.rosters))):
                team = d.rosters["team"+str(i+1)]
                if team.user:
                    team.prompt()
                else:
                    team.pick()

    # print(d.rosters["team5"].players)
    # print(d.rosters["team2"].players)
    # # print(d.rosters["team10"].players)

def manual():
    url = 'https://www.pro-football-reference.com/years/2020/fantasy.htm'

    df = parser(url)
    sub = processor(df, 'QB')
    sub2 = processor(df, 'RB')
    sub3 = processor(df, 'WR')
    sub4 = processor(df, 'TE')

    sub.to_csv('qbs.csv')
    sub2.to_csv('rbs.csv')
    sub3.to_csv('wrs.csv')
    sub4.to_csv('tes.csv')

    teams = int(input("Number of teams in the league: "))
    rounds = int(input("Number of rounds in the draft: "))
    draftPos = int(input("Enter your draft position: "))
    d = Draft(teams, rounds)

    for i in range(teams):
        if i+1 == draftPos:
            name = input("Enter a name for this team: ")
            d.rosters["team"+str(i+1)] = Team(teams, rounds, i+1, name, True)
        else:
            name = "Computer"+str(i+1)
            d.rosters["team"+str(i+1)] = Team(teams, rounds, i+1, name, False)
    
    for i in range(rounds):
        if i % 2 == 0:
            for i in range(len(d.rosters)):
                team = d.rosters["team"+str(i+1)]
                if team.user:
                    team.prompt()
                else:
                    team.entry()
        else:
            for i in reversed(range(len(d.rosters))):
                team = d.rosters["team"+str(i+1)]
                if team.user:
                    team.prompt()
                else:
                    team.entry()