import urllib2
import json
import hashlib
from datetime import datetime
import calendar
import time
import sys

STATUS_OK = 200

# Define Dopamine Class
class Dopamine(object):

    clientOS = 'python'
    clientOSVersion = sys.version
    clientAPIVersion = '0.1.0'
    rewardFunctions = []
    feedbackFunctions = []
    identity = []
    build = ""
    actionNames = []
    actionPairings = []
    serverAddress = 'http://172.27.5.236/v2/app/'

    def __init__(self, appID, devKey, productionKey, token, versionID):
        self.appID = appID
        self.devKey = devKey
        self.productionKey = productionKey
        self.versionID = versionID
        self.token = token
        return

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
        return

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
        return self.apiCall(callObj, 'init')

    def track(self, identity, eventName, metaData):
        timeObj = self.prepTime()
        callObj = json.dumps({"appID": self.appID, "key": self.devKey, "identity": identity, "eventName": eventName, "versionID": self.versionID, "build":self.prepBuild(), "token":self.token, "UTC": timeObj['utc'], "localTime":timeObj['localTime'], "ClientOS":self.clientOS, "ClientOSVersion": self.clientOSVersion, "ClientAPIVersion" : self.clientAPIVersion, "rewardFunctions": self.rewardFunctions, "feedbackFunctions": self.feedbackFunctions, "actionPairings": self.actionPairings})
        return self.apiCall(callObj, 'track')

    def reinforce(self, identity, eventName, metaData):
        timeObj = self.prepTime()
        callObj = json.dumps({"appID": self.appID, "key": self.devKey, "identity": identity, "eventName": eventName, "versionID": self.versionID, "build":self.prepBuild(), "token":self.token, "UTC": timeObj['utc'], "localTime":timeObj['localTime'], "ClientOS":self.clientOS, "ClientOSVersion": self.clientOSVersion, "ClientAPIVersion" : self.clientAPIVersion, "rewardFunctions": self.rewardFunctions, "feedbackFunctions": self.feedbackFunctions, "actionPairings": self.actionPairings})
        return self.apiCall(callObj, 'reinforce')

    def apiCall(self, callObj, callType):

        # launch POST request
        url = '{}{}/{}/'.format(self.serverAddress, self.appID, callType)
        req = urllib2.Request(url, callObj, {'Content-Type': 'application/json'})

        try:
            response = urllib2.urlopen(req)
        except:
            Exception('Error: could not connect to dopamine api')

        # test to check for valid response from the dopamine api
        return response.read()

# her Exceedingly rare error case where API can't be reached
