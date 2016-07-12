# using library installed from pip or easy_install
from dopaminekit import DopamineKit

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
	Sends a tracking call to the DopamineAPI

	Parameters:
	----------
	- actionID : str
	    A descriptive name for action that the user has performed

	- identity : str
	    A string used to identify a particular user, such as an email or username or UUID.

	- metaData : dict = None
	    An optional dictionary containing extra data about the user or environment to generate better results.

	Returns:
	----------
	- responseStatus : json
	    Contains the key "status". If "status" is not 200, then also contains the key "errors"
"""

metaData = {"calories":"200"}
dopaminekit.track('appOpened', '1138', metaData)





""" 
	Sends a reinforcement call to the DopamineAPI and returns the reinforcement decision

	Parameters:
	----------
	- actionID : str
	    A descriptive name for action that the user has performed

	- identity : str
	    A string used to identify a particular user, such as an email or username or UUID.

	- metaData : dict = None
	    An optional dictionary containing extra data about the user or environment to generate better results.

	- timeout : int = 5
	    An optional timeout parameter in seconds to wait for a response. Default is 5.

	Returns:
	----------
	- reinforcementDecision : str
	    A reinforcement decision configured on dashboard.usedopamine.com, otherwise 'neutralResponse'.
"""

reinforcementFunction = dopaminekit.reinforce('action1', '1137', None, 1.4)
print "Reinforcement decision: ", reinforcementFunction

# Within the demo, the possible responses are:
# [   'stars'
#     'thumbsUp'
#     'medalStar'
#     # Show nothing! This is called a neutral response,
#     # and builds up the good feelings for the next surprise!
#     'neutralResponse'
# ]
