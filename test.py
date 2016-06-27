from dopaminekit import DopamineKit

debug_mode = True

app_id = '570ffc491b4c6e9869482fbf'
dev_secret = 'd388c7074d8a283bff1f01eb932c1c9e6bec3b10'
prod_secret = '20af24a85fa00938a5247709fed395c31c89b142'

# Create the Dopamine object
dopa = DopamineKit(app_id, dev_secret, prod_secret, "testing", False)
dopa._debug = debug_mode

# Send tracking call for analytics
dopa.track([{'userID': 1138}], "testEvent1", [{'metaDataKey':'value'}])

# Define reward functions
def rewardFunctionOne():
    print "WOOHOO!"
    transitionUI()

def rewardFunctionTwo():
    print "AWESOME!"
    transitionUI()

def rewardFunctionThree():
    print "WOW!"
    transitionUI()

def transitionUI():
    # continue the flow of your app
    print "..."

# Associate reward fucntions with their code-names
reinforcement_functions = {
    'stars': rewardFunctionOne,
    'thumbsUp': rewardFunctionTwo,
    'medalStar': rewardFunctionThree,
    'neutralResponse': transitionUI
}

# Send reinforce call. Use response in a switch
reinforcementFunction = dopa.reinforce([{'userID': 1137}], "action1", [{'metaDataKey':'value'}])
reinforcement_functions[reinforcementFunction]()
# print reinforcementFunction

