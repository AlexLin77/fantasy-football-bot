from app.data import *
from app.engine import *
import pandas

url = 'https://www.pro-football-reference.com/years/2020/fantasy.htm'


def main():
    mode = input("Enter S for simulated draft and M for manual entry: ")
    if mode.lower() == 's':
        simulate()
    elif mode.lower() == 'm':
        manual()


if __name__ == "__main__":
    main()
