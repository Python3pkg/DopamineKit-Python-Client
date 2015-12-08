import json

from dopamine import Dopamine

api_key = '543715d85b6b234b6e2c83ee'
dev_key = '12be497b39cb5b8a3b7ccbc5129b24a0ee166706'
prod_key = 'fdb803e8384f9cf7015e9b28e828ece3074df6e8'
token = '32284346502274275543715d85b6b234b6e2c83ee'

# Create the Dopamine object
dopa = Dopamine(api_key, dev_key, prod_key, token, "newVersionID")

# Pair your actions and Reinforcement Functions
dopa.pair_actions({'actionName': 'newAction', 'rewardFunctions':['rf1', 'rf2'], 'feedbackFunctions':['ff1', 'ff2']})

dopa.pair('anotherAction', 'anotherResponse', reward=False)
dopa.pair('anotherAction', 'anotherReward', reward=True, constraint=[], objective=[])

# Send your init call
dopa.init()

# Send tracking call for analytics
dopa.track([{'userID': 1138}], "testEvent1", [{'metaData':'value'}])

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
response = dopa.reinforce([{'userID': 1137}], "newAction", [{'metaData':'value'}])
optimalReinforcement = json.loads(response)
if optimalReinforcement['reinforcementFunction'] not in reinforcement.keys():
    raise Exception('Error: reinforcement function not found.')
else:
    reinforcement[optimalReinforcement['reinforcementFunction']]()

