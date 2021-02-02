from app.data import *
from app.engine import *
import pandas

url = 'https://www.pro-football-reference.com/years/2020/fantasy.htm'


def main():
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
        userControl = input("Should this team be controlled by a human? (Y/N) ")
        if userControl == 'y':
            name = input("Enter a name for this team: ")
            d.rosters["team"+str(i+1)] = Team(teams, rounds, i+1, name, True)
        elif userControl == 'n':
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


if __name__ == "__main__":
    main()
