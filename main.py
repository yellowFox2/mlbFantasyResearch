#REQUIREMENTS: Python3, MLB-StatsAPI (github.com/toddrob99/MLB-StatsAPI -> run setup.py -- this requires 'import requests'),
#END-GOAL: give probable fantasy output by evaluating trends
#WANTS: apply hit value coefficients, noSQL db, gameday dataset (import mlbgame), baseballsavant dataset, define variables that correlate to trends, regression testing module (?)

import argparse
import statsapi
import re
import json

#TO-DO: add to eventual noSQL db
class player:
    _searchYear = 2020
    _playerInfoDict = {}
    _playerID = None 
    fullName = None
    mainPos = None 
    playerType = None
    _playerStats = {}  

    def savePlayer2File(self):
        print('\nSaving output to local dir....\n')
        print(json.dumps(self._playerStats,indent=4))
        fileInput = json.dumps(self._playerStats,indent=4)
        f = open(f"{(self.fullName).replace(' ','')}{self._playerID}.txt",'w+')
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

    def getPlayerStats(self):
        return statsapi.player_stat_data(self._playerID, type='yearByYear')['stats']

    def findCurrentPlayerInfo(self):
        for record in self._playerInfoDict['people']:
            if record['fullName'] == self.fullName:
                print('found')
                self._playerID = record['id']
                self.fullName = record['fullName']            
                self.mainPos = record['primaryPosition']['abbreviation']
                self.playerType = 'hitting' if self.mainPos != 'P' else 'pitching'
                if self._playerStats:
                    self._playerStats.clear()
                self._playerStats[self._playerID] = {}
                self._playerStats[self._playerID]['type'] = self.playerType 
                break

    def __init__(self,searchYear,playerInfo,fullName):
        self._searchYear = searchYear
        self._playerInfoDict = playerInfo
        self.fullName = fullName
        self.findCurrentPlayerInfo()
        self.getYearlyPlayerStats()

    def __del__(self):
        class_name = self.__class__.__name__
        print(f'\nobject: {class_name}, playerID: {self._playerID}, {self.fullName}, destroyed....\n')       

def checkForPlayerNames(playersDict,userInput):
    foundPlayerNames = {}
    for player in playersDict['people']:
        if re.search(rf'\b(?=\w){userInput}\b(?!\w)',player['fullName'],flags=re.IGNORECASE) and userInput != '*':
            foundPlayerNames[player['id']] = {}
            foundPlayerNames[player['id']] = player['fullName']
        elif userInput == '*':
            foundPlayerNames[player['id']] = {}
            foundPlayerNames[player['id']] = player['fullName']
    return foundPlayerNames

def getPlayerBase(option,searchYear):
        return statsapi.get('sports_players',{'season':(searchYear)})

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', '--year')
    parser.add_argument('-p', '--playerName')
    parser.add_argument('-t', '--teamName')
    return parser.parse_args()  

def userMenu(playersDict, currentYear):
    print(f'\n==Main Menu==\n\nWorking with {currentYear} player set\n')
    userInput = input('Find yearly stats of player ("quit" to exit search): ')
    if userInput.lower() != 'quit' and userInput.lower() != 'quit()':
        names = {}
        names = checkForPlayerNames(playersDict,userInput)
        print(f'\nPlayers found: {names}\n')
        players = []
        for count,key in enumerate(names.keys()):
            players.append(player(currentYear,playersDict,names[key]))
            players[count].savePlayer2File()
            print(json.dumps(players[count]._playerStats,indent=4))
        return True
    else:
        print('\nExiting....\n')
        return False        

#TO-DO: give options for team stats, etc.
def main():
    run = True
    args = parseArgs()
    currentYear = 2020 if args.year == None else args.year
    playerBase = getPlayerBase('playersInfo',currentYear)
    while run == True:
        run = userMenu(playerBase,currentYear)

if __name__ == '__main__':
    main()