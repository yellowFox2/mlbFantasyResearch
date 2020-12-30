#PURPOSE: Just for fantasy baseball research; I DO NOT OWN MLB-StatsAPI. 
#Give probable fantasy output by evaluating trends
#REQUIREMENTS: Python3, MLB-StatsAPI (github.com/toddrob99/MLB-StatsAPI -> run setup.py -- this requires 'import requests'),
#WANTS: Apply/test "hit value" coefficients, noSQL db, gameday dataset (import mlbgame), baseballsavant dataset, define variables that correlate to trends, regression testing module (?)

import argparse
import statsapi
import re
import json

#TO-DO: add player to noSQL db based on playerID
class player:
    def savePlayer2File(self):
        print('\nSaving output to ".\\out"....\n')
        print(json.dumps(self._playerStats,indent=4))
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

    def findCurrentPlayerInfo(self):
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
        self.findCurrentPlayerInfo()
        self.getYearlyPlayerStats()

    def __del__(self):
        class_name = self.__class__.__name__
        print(f'\nobject: {class_name}, playerID: {self._playerID}, {self.fullName}, destroyed....\n')       

def getPlayerIDs(playersDict,userInput):
    foundPlayerNames = {}
    for player in playersDict['people']:
        if re.search(rf'\b(?=\w){userInput}\b(?!\w)',player['fullName'],flags=re.IGNORECASE) or userInput == '*':
            foundPlayerNames[player['id']] = {}
            foundPlayerNames[player['id']] = player['fullName']
    return foundPlayerNames

def userMenu(playersDict, currentYear):
    print(f'\n==Main Menu==\n\nWorking with {currentYear} player set\n')
    userInput = input('Find yearly stats of player ("quit" to exit search): ')
    if userInput.lower() != 'quit' and userInput.lower() != 'q':
        IDs2names = {}
        IDs2names = getPlayerIDs(playersDict,userInput)
        print(f'\nPlayers found: {IDs2names}\n')
        players = []
        for count,key in enumerate(IDs2names.keys()):
            players.append(player(currentYear,playersDict,IDs2names[key]))
            players[count].savePlayer2File()
            print(json.dumps(players[count]._playerStats,indent=4))
        return True
    else:
        print('\nExiting....\n')
        return False 

def getPlayerBase(searchYear):
        return statsapi.get('sports_players',{'season':(searchYear)})

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', '--year')
    parser.add_argument('-p', '--playerName')
    parser.add_argument('-t', '--teamName')
    return parser.parse_args()        

#TO-DO: give options for team stats, etc.
def main():
    run = True
    args = getArgs()
    currentYear = 2020 if args.year == None else args.year
    playerBase = getPlayerBase(currentYear)
    while run == True:
        run = userMenu(playerBase,currentYear)

if __name__ == '__main__':
    main()