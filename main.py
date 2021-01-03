#WANTS: Apply/test "hit value" coefficients, noSQL db, gameday dataset (import mlbgame), baseballsavant dataset, define variables that correlate to trends, regression testing module (?)

import argparse
import statsapi
import re
import json
import time
from player import player
from pymongo import MongoClient

def getPlayerBaseByYear(searchYear):
    print(f'\nPulling {searchYear} general player info from MLB-statsAPI....\n')
    return statsapi.get('sports_players',{'season':(searchYear)})

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
        playersList.append(player(playersDict,IDsDict[key]))
        playersList[playerBuffer].savePlayer2db(dbRef)
        #!!FIX
        #playersList[playerBuffer].getYearsActive(dbRef)
        years = ['2019','2020']
        playersList[playerBuffer].printYearlyPlayerStats(dbRef,years)        
        playerBuffer += 1
    print(f"\nQueried in {time.perf_counter() - timer:0.4f} seconds\n")
    return True

#Rename json to '2020 default player names'
def getLocalPlayerBase():
    return json.load(open('.\\src\\playersGenInfo.json',))

def userMenu(playersDict, currentYear,dbRef):
    print(f'\n==Main Menu==\n\nWorking with {currentYear[0]} player set\n')
    userInput = input(f'\nFind yearly stats of player ("-quit" to exit search, "-yrchng" to change player base): \n')
    start = time.perf_counter()
    if userInput.lower() == '-yrchange' or userInput.lower() == '-yrchng':
        currentYear[0] = input(f'\nWhich year?\n')
        playersDict = getPlayerBaseByYear(currentYear[0])
        return userMenu(playersDict,currentYear,dbRef)
    elif userInput.lower() == '-quit' or userInput.lower() == '-q':
        print('\nExiting....\n')
        return False         
    # if userInput.lower() == '-paavgs':
    #     pass
    else:
        IDs2names = {}
        IDs2names = getPlayerIDs(playersDict,userInput)
        print(f'\nPlayers found: {IDs2names}\n')
        players = []
        return playersInit(IDs2names,players,currentYear[0],playersDict,start,dbRef)

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
    connectionString = 'mongodb://localhost:27017'
    try:
        dbRef = MongoClient(connectionString)
        print('from main:')
        print(type(dbRef))
        print(f'\nConnected to {connectionString}\n')
    except:
        print(f'\nError: did not connect to db via: {connectString}\nExiting....\n')
        quit()
    currentYear = []
    currentYear.append(2020) if args.year == None else currentYear.append(args.year)
    playerBase = getLocalPlayerBase()
    while run == True:
        run = userMenu(playerBase,currentYear,dbRef)

if __name__ == '__main__':
    main()