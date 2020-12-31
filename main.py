#WANTS: Apply/test "hit value" coefficients, noSQL db, gameday dataset (import mlbgame), baseballsavant dataset, define variables that correlate to trends, regression testing module (?)

import argparse
import statsapi
import re
import json
import time
from player import player
from pymongo import MongoClient


def getPlayerIDs(playersDict,userInput):
    foundPlayerNames = {}
    for player in playersDict['people']:
        if re.search(rf'\b(?=\w){userInput}\b(?!\w)',player['fullName'],flags=re.IGNORECASE) or userInput == '*':
            foundPlayerNames[player['id']] = {}
            foundPlayerNames[player['id']] = player['fullName']
    return foundPlayerNames

def playersInit(IDsDict, playersList, year, playersDict, timer,dbRef):
    playerBuffer = 0
    for count,key in enumerate(IDsDict.keys()):
        if playerBuffer == 10:
            playersList.clear()
            playerBuffer = 0
        playersList.append(player(year,playersDict,IDsDict[key],dbRef))
        playersList[playerBuffer].savePlayer2File()
        playerBuffer += 1
    print(f"Queried in {time.perf_counter() - timer:0.4f} seconds")
    return True

#!!FIX
#Alternate to getLocalPlayerBase
#For use without local json
#def getPlayerBase(searchYear):
#       return statsapi.get('sports_players',{'season':(searchYear)})

def getLocalPlayerBase():
    return json.load(open('.\\src\\playersGenInfo.json',))


def userMenu(playersDict, currentYear,dbRef):
    print(f'\n==Main Menu==\n\nWorking with {currentYear[0]} player set\n')
    userInput = input(f'\nFind yearly stats of player ("quit" to exit search): \n')
    start = time.perf_counter()
    #!!FIX
    #if userInput.lower() == '-yearChange' or userInput.lower() == '--yc':
        #currentYear[0] = input(f'\nInput new player set year: \n')
        #tmp = getPlayerBase(currentYear[0])
        #return userMenu(tmp,currentYear)
    if userInput.lower() != 'quit' and userInput.lower() != 'q':
        IDs2names = {}
        IDs2names = getPlayerIDs(playersDict,userInput)
        print(f'\nPlayers found: {IDs2names}\n')
        players = []
        return playersInit(IDs2names,players,currentYear[0],playersDict,start,dbRef)
    else:
        print('\nExiting....\n')
        return False 

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
    dbRef = MongoClient('mongodb://localhost:27017')
    currentYear = []
    currentYear.append(2020) if args.year == None else currentYear.append(args.year)
    #!!FIX
    #playerBase = getPlayerBase(currentYear[0])
    playerBase = getLocalPlayerBase()
    while run == True:
        run = userMenu(playerBase,currentYear,dbRef)

if __name__ == '__main__':
    main()