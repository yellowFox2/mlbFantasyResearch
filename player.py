#WANTS: Apply/test "hit value" coefficients, noSQL db, gameday dataset (import mlbgame), baseballsavant dataset, define variables that correlate to trends, regression testing module (?)

import argparse
import statsapi
import re
import json
import time
import traceback
#from pymongo import MongoClient

#TO-DO: change/delete player in noSQL
class player:

	def savePlayer2db(self,dbRef):
#		db = self._connection['players']
		collections = dbRef['players'].list_collection_names()
		if str(self._playerID) in collections:
			print(f'\nMongodDB record found for {self._playerID}, {self.fullName}')
			playerDbCollection = dbRef[str(self._playerID)]
		else:
			print(f'Adding {self.fullName} to players db....')
			result = dbRef['players'][str(self._playerID)].insert_one(self._playerStats)

	def getYearlyPlayerStats(self):
		for years in statsapi.player_stat_data(self._playerID, type='yearByYear')['stats']:
			if(years.get('group') == self._playerStats[str(self._playerID)]['type']):
				statsDict = {}
				statsDict[years.get('season')] = years.get('stats')
				self._playerStats[str(self._playerID)][years.get('season')] = statsDict[years.get('season')]
				

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

	def __init__(self,playerBase,fullName):
		self._playerBase = playerBase
		self.fullName = fullName
		self._playerStats = {}
		self.setPlayerInfo()
		try:
			self.getYearlyPlayerStats()
		except Exception:
			print(f"ERROR: couldn't find player stats for {self.fullName}")
			print(traceback.format_exc())

	def __del__(self):
		class_name = self.__class__.__name__
		print(f'\nobject: "{class_name}", playerID: {self._playerID}, {self.fullName}, destroyed....\n')       