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

	# def careerStats(self):
	# 	gamesPlayed
	# 	groundOuts
	# 	airOuts
	# 	runs
	# 	doubles
	# 	triples
	# 	homeRuns
	# 	strikeOuts
	# 	baseOnBalls
	# 	intentionalWalks
	# 	hits
	# 	hitByPitch
	# 	avg
	# 	atBats
	# 	obp
	# 	slg
	# 	ops
	# 	caughtStealing
	# 	stolenBases
	# 	stolenBasePercentage
	# 	groundedIntoDoublePlay
	# 	numberOfPitches
	# 	plateAppearances
	# 	totalBases
	# 	rbi
	# 	leftOnBase
	# 	sacBunts
	# 	sacFlies
	# 	babip
	# 	groundOutsToAirouts
	# 	atBatsPerHomeRun

	# def getFullSeasonRate(self,stat,games):
	# 	return (stat/games) * 162
	# def getYearlyPlayerRunVal(self,dbRef):
		#Per Tom Tango's The Book, run environment from 1999 - 2002:
		#HR=1.397
		#3B=1.07
		#2B=.776
		#1B=.475
		#K==-.301
		#BB=.323
		#HBP=.352
		#IBB=.179
		#SACBUNT=-.096
		#SB=.175
		#CS=-.467




	def savePlayer2db(self,dbRef):
#		db = self._connection['players']
		collections = dbRef['players'].list_collection_names()
		if str(self._playerID) in collections:
			print(f'\nMongodDB record found for {self._playerID}, {self.fullName}')
		else:
			print(f'Adding {self.fullName} to players db....')
			result = dbRef['players'][str(self._playerID)].insert_one(self._playerStats)

	def setYearlyPlayerStats(self):
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



	def printYearlyPlayerStats(self,dbRef,yearRange):
		curPlayerColl = dbRef.players[str(self._playerID)]
		for year in yearRange:
			print('------------------------------------------------')
			print('year: ', year)
			data = curPlayerColl.find_one({},{'_id':0,f'{str(self._playerID)}.{year}':1})
			for value in data[str(self._playerID)].values():
				for nestedKey, nestedVal in value.items():
					print(nestedKey, ': ', nestedVal)

	#!!Fix
	def getYearsActive(self,dbRef):
		curPlayerColl = dbRef.players[str(self._playerID)]	
		yearRange = []	
		yearRegex = re.compile('^[1|2]{1}[0-9]{3}$')
		print(yearRegex)
		test = curPlayerColl.find({},{'_id':0,f'{str(self._playerID)}.{yearRegex}':1})
		for cursor in test:
			for key, value in cursor.items():
				print(key)
				print(value)
			#print(cursor.items())
		# for key, value in test.items():
		# 	print(f'{key} : {value}\n')
			#yearRange.append(year)					

	def __init__(self,playerBase,fullName):
		self._playerBase = playerBase
		self.fullName = fullName
		self._playerStats = {}
		self.setPlayerInfo()
		try:
			self.setYearlyPlayerStats()
		except Exception:
			print(f"ERROR: couldn't find player stats for {self.fullName}")
			print(traceback.format_exc())

	def __del__(self):
		class_name = self.__class__.__name__
		print(f'\nobject: "{class_name}", playerID: {self._playerID}, {self.fullName}, destroyed....\n')       