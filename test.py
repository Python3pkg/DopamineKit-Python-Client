# using library installed from pip or easy_install
from dopamine import DopamineKit

app_id = '570ffc491b4c6e9869482fbf'
production_secret = '20af24a85fa00938a5247709fed395c31c89b142'
development_secret = 'd388c7074d8a283bff1f01eb932c1c9e6bec3b10'
versionID = 'testing'
production_mode = False

# Create the Dopamine object

# DopamineKit.__init__(self, appID, developmentSecret, productionSecret, versionID, inProduction, debugmode = False):
dopaminekit = DopamineKit(app_id, development_secret, production_secret, versionID, production_mode)
dopaminekit._debugmode = True    # Prints out the sent/received data


"""
Tracking Calls
	Send tracking call for analytics to the DopamineAPI

Syntax:
----------
	dopaminekit.track(str actionID, str identity, dict metaData = None)

Parameters:
----------
	- actionID : str
	    A descriptive name for the action to be tracked.

	- identity : str
	    A string to identity the user, such as an email or username or UUID.

	- metaData : dict = None
	    An optional dictionary containing extra data about the user or environment to generate better results.
"""

dopaminekit.track('action1', '1138', {'key':'value'})


"""
Reinforcement Calls
	Sends a reinforcement call to the DopamineAPI and returns the reinforcement decision

Syntax:
----------
	response = dopaminekit.reinforce(str actionID, str identity, dict metaData = None, timeout = 5)

Parameters:
----------
	- actionID : str
	    A descriptive name for the action to be tracked.

	- identity : str
	    A string to identity the user, such as an email or username or UUID.

	- metaData : dict = None
	    An optional dictionary containing extra data about the user or environment to generate better results.

	- timeout : int = 5
	    An optional timeout parameter in seconds to wait for a response. Default is 5.

"""

reinforcementFunction = dopaminekit.reinforce('action1', '1137')
print("Reinforcement decision: ", reinforcementFunction)

# Within the demo, the possible responses are:
# [   'stars'
#     'thumbsUp'
#     'medalStar'
#     # Show nothing! This is called a neutral response,
#     # and builds up the good feelings for the next surprise!
#     'neutralResponse'
# ]
