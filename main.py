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
from player import player


def getPlayerIDs(playersDict,userInput):
    foundPlayerNames = {}
    for player in playersDict['people']:
        if re.search(rf'\b(?=\w){userInput}\b(?!\w)',player['fullName'],flags=re.IGNORECASE) or userInput == '*':
            foundPlayerNames[player['id']] = {}
            foundPlayerNames[player['id']] = player['fullName']
    return foundPlayerNames

def playersInit(IDsDict, playersList, year, playersDict, timer):
    for count,key in enumerate(IDsDict.keys()):
        playersList.append(player(year,playersDict,IDsDict[key]))
        playersList[count].savePlayer2File()
        formattedJson = json.dumps(playersList[count]._playerStats,indent=7)
        colorJson = highlight(formattedJson, lexers.JsonLexer(), formatters.TerminalFormatter())
        print(formattedJson)
    print(f"Queried in {time.perf_counter() - timer:0.4f} seconds")
    return True

def getPlayerBase(searchYear):
        return statsapi.get('sports_players',{'season':(searchYear)})

def userMenu(playersDict, currentYear):
    print(f'\n==Main Menu==\n\nWorking with {currentYear[0]} player set\n')
    userInput = input(f'\nFind yearly stats of player ("quit" to exit search): \n')
    start = time.perf_counter()
    if userInput.lower() == '-yearChange' or userInput.lower() == '--yc':
        currentYear[0] = input(f'\nInput new player set year: \n')
        tmp = getPlayerBase(currentYear[0])
        return userMenu(tmp,currentYear)
    elif userInput.lower() != 'quit' and userInput.lower() != 'q':
        IDs2names = {}
        IDs2names = getPlayerIDs(playersDict,userInput)
        print(f'\nPlayers found: {IDs2names}\n')
        players = []
        return playersInit(IDs2names,players,currentYear[0],playersDict, start)
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
    currentYear = []
    currentYear.append(2020) if args.year == None else currentYear.append(args.year)
    playerBase = getPlayerBase(currentYear[0])
    while run == True:
        run = userMenu(playerBase,currentYear)

if __name__ == '__main__':
    main()