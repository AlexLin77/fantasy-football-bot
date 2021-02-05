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
        assert True
    
    


if __name__ == '__main__':
    unittest.main()