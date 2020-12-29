#END-GOAL: give probable fantasy output by evaluating trends
#NEEDS: noSQL db, gameday dataset (import mlbgame), baseballsavant dataset, define variables that correlate to trends, regression testing module (?)

import argparse
import statsapi
import re
import json

#TO-DO: add to eventual noSQL db
def appendYearlyPlayerStats(playersDict,playerID,season,stats):
    statsDict = {}
    statsDict[season] = stats
    playersDict[playerID][season] = statsDict[season]

def getYearlyPlayerStats(playerID,playersDict):
    for years in statsapi.player_stat_data(playerID, type='yearByYear')['stats']:
        if(years.get('group') == playersDict[playerID]['type']):
            appendYearlyPlayerStats(playersDict,playerID,years.get('season'),years.get('stats'))

def checkForPlayerNames(playerDict,playerInput):
    foundPlayerNames = {}
    for player in playerDict:
        if re.search(rf'\b(?=\w){playerInput}\b(?!\w)',playerDict[player]['fullName'],flags=re.IGNORECASE):
            foundPlayerNames[player] = (playerDict[player]['fullName'])
    return foundPlayerNames

def userSearchForYearlyPlayerStats(playersDict):
    playerInput = input('Find yearly stats of player ("quit" to exit search): ')
    if playerInput != 'quit':
        names = {}
        names = checkForPlayerNames(playersDict,playerInput)
        print(f'\nPlayers found: {names}\n')
        for key in names.keys():
            getYearlyPlayerStats(key,playersDict)
            print(json.dumps(playersDict[key],indent=4))
        return True
    else:
        print('\nExiting....\n')
        return False
  
def get_players(year):
    print(f'\nGetting player IDs from {year}....\n')
    playersDict = {}
    players = statsapi.get('sports_players',{'season':year})
    for people in players['people']:
        playersDict[people.get('id')] = {}
        playersDict[people.get('id')]['fullName'] = people.get('fullName')
        playersDict[people.get('id')]['pos'] = people['primaryPosition'].get('abbreviation')
        playersDict[people.get('id')]['type'] = 'hitting' if playersDict[people.get('id')]['pos'] != 'P' else 'pitching'
    return playersDict

#TO-DO: give options for team stats, etc.
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', '--year')
    parser.add_argument('-p', '--playerName')
    parser.add_argument('-t', '--teamName')
    args = parser.parse_args()
    players = get_players(2020) if args.year is None else get_players(args.year)
    while userSearchForYearlyPlayerStats(players):
        print('\n==Main Menu==\n')
        

if __name__ == '__main__':
    main()