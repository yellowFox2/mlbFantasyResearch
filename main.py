import statsapi
import json
import re

def get_players(year):
    print("Getting player IDs....")
    playersDict = {}
    players = statsapi.get('sports_players',{'season':year})

    for people in players['people']:
        playersDict[people.get('id')] = {}
        playersDict[people.get('id')]['fullName'] = people.get('fullName')
        playersDict[people.get('id')]['pos'] = people['primaryPosition'].get('abbreviation')

    return playersDict
        
def getYearlyHittingStats(playerID):
    for years in statsapi.player_stat_data(playerID, type="yearByYear")['stats']:
        if(years.get('group') == 'hitting'):
            print(years.get('season'))
            print(json.dumps(years.get('stats'),indent=4))

def getYearlyPitchingStats(playerID):
    for years in statsapi.player_stat_data(playerID, type="yearByYear")['stats']:
        if(years.get('group') == 'pitching'):
            print(years.get('season'))
            print(json.dumps(years.get('stats'),indent=4))

def checkForPlayerNames(playerDict,playerInput):
    foundPlayerNames = {}
    for player in playerDict:
        if re.search(rf"\b(?=\w){playerInput}\b(?!\w)",playerDict[player]['fullName'],flags=re.IGNORECASE):
            foundPlayerNames[player] = (playerDict[player]['fullName'])
    return foundPlayerNames

def searchForPlayers(playersDict):
    playerInput = input("find yearly stats of player: ")
    names = {}
    names = checkForPlayerNames(playersDict,playerInput)
    print(f'Players found: {names}')
    for key in names.keys():
        if playersDict[key]['pos'] == 'P':
            print("Pitcher found")
            getYearlyPitchingStats(key)
        else:
            print("Batter found")
            getYearlyHittingStats(key)

def main():
    currentYear = 2020
    players = get_players(currentYear)
    searchForPlayers(players)
    #print(players)

if __name__ == "__main__":
    main()