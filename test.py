import json

from dopamine import Dopamine, STATUS_OK

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

reinforcement = {
    'rf1': rewardFunctionOne,
    'rf2': rewardFunctionTwo,
    'ff1': feedbackFunctionOne,
    'ff2': feedbackFunctionTwo
}

# Send reinforce call. Use response in a switch
optimalReinforcement = json.loads(dopamineInstance.reinforce([{'userID': 1138}], "newAction", [{'metaData':'value'}]))

if optimalReinforcement['status'] != STATUS_OK:
    raise Exception('Error: communication error')

if optimalReinforcement['rewardFunction'] not in reinforcement.keys():
    raise Exception('Error: reinforcement function not found.')
else:
    reinforcement[optimalReinforcement['reinforcementFunction']]()

if optimalReinforcement['status'] == STATUS_OK:
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
    #
