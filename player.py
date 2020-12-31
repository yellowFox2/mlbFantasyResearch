#WANTS: Apply/test "hit value" coefficients, noSQL db, gameday dataset (import mlbgame), baseballsavant dataset, define variables that correlate to trends, regression testing module (?)

import argparse
import statsapi
import re
import json
import time
from pymongo import MongoClient

#TO-DO: add/change/delete player in noSQL
class player:

	def savePlayer2File(self):
		db = self._connection['players']
		collections = db.list_collection_names()
		if str(self._playerID) in collections:
			print(f'\nMongodDB record found for {self._playerID}, {self.fullName}')
			playerDbCollection = db[str(self._playerID)]
		else:
			print(f'Adding {self.fullName} to players db....')
			result = db[str(self._playerID)].insert_one(self._playerStats)
			time.sleep(5)
		#OLD --> f = open(f".\\out\\{(self.fullName).replace(' ','')}{self._playerID}.txt",'w+')


	def appendYearlyPlayerStats(self,stats,season):
		statsDict = {}
		statsDict[season] = stats
		self._playerStats[str(self._playerID)][season] = statsDict[season]

	def getYearlyPlayerStats(self):
		for years in statsapi.player_stat_data(self._playerID, type='yearByYear')['stats']:
			if(years.get('group') == self._playerStats[str(self._playerID)]['type']):
				self.appendYearlyPlayerStats(years.get('stats'),years.get('season'))

	def setPlayerInfo(self):
		for record in self._playerBase['people']:
			if record['fullName'] == self.fullName:
				self._playerID = record['id']
				self.fullName = record['fullName']            
				self.mainPos = record['primaryPosition']['abbreviation']
				self.playerType = 'hitting' if self.mainPos != 'P' else 'pitching'
				self._playerStats[str(self._playerID)] = {}
				self._playerStats[str(self._playerID)]['fullName'] = self.fullName
				self._playerStats[str(self._playerID)]['pos'] = self.mainPos 				
				self._playerStats[str(self._playerID)]['type'] = self.playerType 
				break

	def __init__(self,searchYear,playerBase,fullName,dbRef):
		self._connection = dbRef
		self._searchYear = searchYear
		self._playerBase = playerBase
		self.fullName = fullName
		self._playerStats = {}
		self.setPlayerInfo()
		try:
			self.getYearlyPlayerStats()
		except:
			print(f"ERROR: couldn't find player stats for {self.fullName}")

	def __del__(self):
		class_name = self.__class__.__name__
		print(f'\nobject: "{class_name}", playerID: {self._playerID}, {self.fullName}, destroyed....\n')       