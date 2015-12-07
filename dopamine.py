import urllib2
import json
import hashlib
from datetime import datetime
import calendar
import time
import sys

# Define Dopamine Class
class Dopamine:
	def __init__(self, appID, devKey, productionKey, token, versionID):
		self.appID = appID
		self.devKey = devKey
		self.productionKey = productionKey
		self.versionID = versionID
		self.token = token
		self.rewardFunctions = []
		self.feedbackFunctions = []
		self.identity = []
		self.build = ""
		self.actionNames = []
		self.actionPairings = []
		self.clientOS = "python"
		self.clientOSVersion = sys.version
		self.clientAPIVersion = "0.1.0"

	def pairAction(self, pairing):
		if self.actionNames.count(pairing['actionName']) == 0:
			self.actionNames.append(pairing['actionName'])
			newPairing = {'actionName': pairing['actionName'], 'reinforcers':[]}
			for thisReward in pairing['rewardFunctions']:
				if self.rewardFunctions.count(thisReward) == 0:
					self.rewardFunctions.append(thisReward)
				newPairing['reinforcers'].append({'functionName': thisReward, 'type':'Reward', 'constraint': [], 'objective': []})
			for thisFeedback in pairing['feedbackFunctions']:
				if self.feedbackFunctions.count(thisFeedback) == 0:
					self.feedbackFunctions.append(thisFeedback)
				newPairing['reinforcers'].append({'functionName': thisFeedback, 'type':'Feedback', 'constraint': [], 'objective': []})
			self.actionPairings.append(newPairing)

	def prepBuild(self):
		# create build
		buildString = json.dumps(self.actionPairings)
		hashObject = hashlib.sha1(buildString);
		return hashObject.hexdigest()

	def prepTime(self):
		#prep UTC, localTime
		utcDateTime = datetime.utcnow()
		timeObj = {"utc": calendar.timegm(utcDateTime.utctimetuple()) * 1000, "localTime": time.time() * 1000}
		return timeObj

	def init(self):
		# use prepTime to prepare timestamps
		timeObj = self.prepTime()

		# prep JSON object for transmission
		callObj = json.dumps({"appID": self.appID, "key": self.devKey, "identity": [{'user':'INIT'}], "versionID": self.versionID, "build":self.prepBuild(), "token":self.token, "UTC": timeObj['utc'], "localTime":timeObj['localTime'], "ClientOS":self.clientOS, "ClientOSVersion": self.clientOSVersion, "ClientAPIVersion" : self.clientAPIVersion, "rewardFunctions": self.rewardFunctions, "feedbackFunctions": self.feedbackFunctions, "actionPairings": self.actionPairings})
		
		# launch POST request
		req = urllib2.Request('http://172.27.5.236/v2/app/' + self.appID + '/init/', callObj, {'Content-Type': 'application/json'})
		f = urllib2.urlopen(req)
		response = f.read()
		return response
		

	def track(self, identity, eventName, metaData):
		timeObj = self.prepTime()
		callObj = json.dumps({"appID": self.appID, "key": self.devKey, "identity": identity, "eventName": eventName, "versionID": self.versionID, "build":self.prepBuild(), "token":self.token, "UTC": timeObj['utc'], "localTime":timeObj['localTime'], "ClientOS":self.clientOS, "ClientOSVersion": self.clientOSVersion, "ClientAPIVersion" : self.clientAPIVersion, "rewardFunctions": self.rewardFunctions, "feedbackFunctions": self.feedbackFunctions, "actionPairings": self.actionPairings})
		
		# launch POST request
		req = urllib2.Request('http://172.27.5.236/v2/app/' + self.appID + '/track/', callObj, {'Content-Type': 'application/json'})
		f = urllib2.urlopen(req)
		response = f.read()
		return response

	def reinforce(self, identity, eventName, metaData):
		timeObj = self.prepTime()
		callObj = json.dumps({"appID": self.appID, "key": self.devKey, "identity": identity, "eventName": eventName, "versionID": self.versionID, "build":self.prepBuild(), "token":self.token, "UTC": timeObj['utc'], "localTime":timeObj['localTime'], "ClientOS":self.clientOS, "ClientOSVersion": self.clientOSVersion, "ClientAPIVersion" : self.clientAPIVersion, "rewardFunctions": self.rewardFunctions, "feedbackFunctions": self.feedbackFunctions, "actionPairings": self.actionPairings})
		
		# launch POST request
		req = urllib2.Request('http://172.27.5.236/v2/app/' + self.appID + '/reinforce/', callObj, {'Content-Type': 'application/json'})
		f = urllib2.urlopen(req)
		response = f.read()
		return response
		


# Create the Dopamine object
dopamineInstance = Dopamine("565fe47d0361f0bba4087f30", "f6849dcad26da272bfe488d49728b1851dfb37d9", "751cc30225f295fca8b04000113308999d6f3f18", "38284383807331325565fe47d0361f0bba4087f30", "newVersionID")

# Pair your actions and Reinforcement Functions
dopamineInstance.pairAction({'actionName': 'newAction', 'rewardFunctions':['rf1', 'rf2'], 'feedbackFunctions':['ff1', 'ff2']})

# Send your init call
# print dopamineInstance.init()

# Send tracking call for analytics
# print dopamineInstance.track([{'userID': 1138}], "testEvent1", [{'metaData':'value'}])

def rewardFunctionOne():
	print "WOOHOO!"

def rewardFunctionTwo():
	print "AWESOME!"

def feedbackFunctionOne():
	print "Acknowledged."

def feedbackFunctionTwo():
	print "Received."

# Send reinforce call. Use response in a switch
optimalReinforcement = json.loads(dopamineInstance.reinforce([{'userID': 1138}], "newAction", [{'metaData':'value'}]))
if optimalReinforcement['status'] == 200:
	if optimalReinforcement['reinforcementFunction'] == 'rf1':
		rewardFunctionOne()
	elif optimalReinforcement['reinforcementFunction'] == 'rf2':
		rewardFunctionTwo()
	elif optimalReinforcement['reinforcementFunction'] == 'ff1':
		feedbackFunctionOne()
	elif optimalReinforcement['reinforcementFunction'] == 'ff2':
		feedbackFunctionTwo()
else:
	print "COMMUNICATION ERROR"
	# Exceedingly rare error case where API can't be reached