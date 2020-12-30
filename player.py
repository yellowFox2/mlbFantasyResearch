#PURPOSE: Just for fantasy baseball research; I DO NOT OWN MLB-StatsAPI. 
#Give probable fantasy output by evaluating trends
#REQUIREMENTS: Python3, MLB-StatsAPI (github.com/toddrob99/MLB-StatsAPI -> run setup.py -- this requires 'import requests'),
#WANTS: Apply/test "hit value" coefficients, noSQL db, gameday dataset (import mlbgame), baseballsavant dataset, define variables that correlate to trends, regression testing module (?)

import argparse
import statsapi
import re
import json
import time
from pygments import highlight, lexers, formatters

#TO-DO: add player to noSQL db based on playerID
class player:
    # def getSeasonHitVal(self):
    #     print(type(str(self._searchYear)))
    #     tmp = {}
    #     tmp = self._playerStats[self._playerID][str(self._searchYear)]
    #     print(tmp['runs'])

    def savePlayer2File(self):
        print('\nSaving output to ".\\out"....\n')
        fileInput = json.dumps(self._playerStats,indent=4)
        f = open(f".\\out\\{(self.fullName).replace(' ','')}{self._playerID}.txt",'w+')
        f.write(fileInput)
        f.close()

    def appendYearlyPlayerStats(self,stats,season):
        statsDict = {}
        statsDict[season] = stats
        self._playerStats[self._playerID][season] = statsDict[season]

    def getYearlyPlayerStats(self):
        for years in statsapi.player_stat_data(self._playerID, type='yearByYear')['stats']:
            if(years.get('group') == self._playerStats[self._playerID]['type']):
                self.appendYearlyPlayerStats(years.get('stats'),years.get('season'))

    def setPlayerInfo(self):
        for record in self._playerInfoDict['people']:
            if record['fullName'] == self.fullName:
                self._playerID = record['id']
                self.fullName = record['fullName']            
                self.mainPos = record['primaryPosition']['abbreviation']
                self.playerType = 'hitting' if self.mainPos != 'P' else 'pitching'
                self._playerStats[self._playerID] = {}
                self._playerStats[self._playerID]['type'] = self.playerType 
                break

    def __init__(self,searchYear,playerInfo,fullName):
        self._searchYear = searchYear
        self._playerInfoDict = playerInfo
        self.fullName = fullName
        self._playerStats = {}
        self.setPlayerInfo()
        self.getYearlyPlayerStats()
        #self.getSeasonHitVal()

    def __del__(self):
        class_name = self.__class__.__name__
        print(f'\nobject: {class_name}, playerID: {self._playerID}, {self.fullName}, destroyed....\n')       