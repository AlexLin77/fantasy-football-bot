# -*- coding: utf-8 -*-

import unittest
import pandas
from app.data import *
from app.helpers import *

url = 'https://www.pro-football-reference.com/years/2020/fantasy.htm'

class TestBotFunctions(unittest.TestCase):

    df = parser(url)
    sub = processor(df, 'QB')
    sub2 = processor(df, 'RB')
    sub3 = processor(df, 'WR')
    sub4 = processor(df, 'TE')

    sub.to_csv('qbs.csv')
    sub2.to_csv('rbs.csv')
    sub3.to_csv('wrs.csv')
    sub4.to_csv('tes.csv')

    qbtable = pandas.read_csv('qbs.csv')
   
    def test_qbvalueAdded(self):
        self.assertEquals(qbvalueAdded(qbtable, 5, 2), ("Patrick Mahomes *", 2.16, 'QB'))
        self.assertEquals(qbvalueAdded(qbtable, 5, 7), ("Patrick Mahomes *", 2.16, "QB"))
        self.assertEquals(qbvalueAdded(qbtable, 12, 7), ("Josh Allen *", 2.39, "QB"))
        self.assertEquals(qbvalueAdded(qbtable, 18, 7), ("Aaron Rodgers *+", 3.16, "QB"))
    
    


if __name__ == '__main__':
    unittest.main()