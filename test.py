
from dopamine import Dopamine

app_id = '543715d85b6b234b6e2c83ee'
dev_key = '12be497b39cb5b8a3b7ccbc5129b24a0ee166706'
prod_key = 'fdb803e8384f9cf7015e9b28e828ece3074df6e8'
token = '32284346502274275543715d85b6b234b6e2c83ee'

# Create the Dopamine object
dopa = Dopamine(app_id, dev_key, prod_key, token, "newVersionID", False)

# Pair your actions and Reinforcement Functions
# dopa.pair_actions({'actionName': 'newAction', 'rewardFunctions':['rf1', 'rf2'], 'feedbackFunctions':['ff1', 'ff2']})
dopa.pair_action_to_reinforcement('action_name', 'name_for_feeback_function_1', reward=False)
dopa.pair_action_to_reinforcement('action_name', 'name_for_reward_function_1', reward=True, constraint=[], objective=[])
dopa.pair_action_to_reinforcement('action_name', 'name_for_reward_function_2', reward=True, constraint=[], objective=[])

dopa.pair_action_to_reinforcement('a_different_action_name', 'name_for_feeback_function_2', reward=False)
dopa.pair_action_to_reinforcement('a_different_action_name', 'name_for_reward_function_3', reward=True, constraint=[], objective=[])

# Send your init call
dopa.init()

# Send tracking call for analytics
dopa.track([{'userID': 1138}], "testEvent1", [{'metaData':'value'}])

# Define reward functions
def rewardFunctionOne():
    print "WOOHOO!"

def rewardFunctionTwo():
    print "AWESOME!"

def rewardFunctionThree():
    print "WOW!"

def feedbackFunctionOne():
    print "Acknowledged."

def feedbackFunctionTwo():
    print "Received."

# Associate reward fucntions with their code-names
reinforcement_functions = {
    'name_for_reward_function_1': rewardFunctionOne,
    'name_for_reward_function_2': rewardFunctionTwo,
    'name_for_reward_function_3': rewardFunctionThree,
    'name_for_feeback_function_1': feedbackFunctionOne,
    'name_for_feeback_function_2': feedbackFunctionTwo
}

# Send reinforce call. Use response in a switch
response = dopa.reinforce([{'userID': 1137}], "action_name", [{'metaData':'value'}])

optimal_reinforcement = response
if optimal_reinforcement['reinforcementFunction'] not in reinforcement_functions.keys():
    raise Exception('Error: reinforcement function not found.')
else:
    reinforcement_functions[optimal_reinforcement['reinforcementFunction']]()

