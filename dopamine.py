import urllib2
import json
import hashlib
from datetime import datetime
import calendar
import time
import sys

STATUS = {
    'OK': 200,
    'ERROR': 100
}

class Dopamine(object):
    """
    # Dopamine API interface class

    # appID -
    # dev_key -
    # production_key -
    # token -
    # versionID -

    """

    reward_functions = []       # list of all reward function names (positive reinforcers)
    feedback_functions = []     # list of all feedback function names (neutral reinforcement)
    identity = []

    actions = []                # [ actionName1, actionName2, actionName3, ... ]
    pairings = {}               # { actionName: [reinforcers], ... }

    _client_os = 'python'
    _client_os_version = sys.version
    _client_sdk_version = '0.1.0'
    _server_url = 'https://api.usedopamine.com'

    _debug = True               # debug flag set to true for console messages

    def __init__(self, appID, dev_key, production_key, token, versionID, inProduction, pairings=None):

        self.appID = appID
        self.dev_key = dev_key
        self.production_key = production_key
        self.token = token
        self.versionID = versionID
        self.inProduction = inProduction

        if isinstance(pairings, dict):
            pairings = [pairings]
        if isinstance(pairings, list):
            [self.pair_actions(pairing) for pairing in pairings]

        return

    def call(self, call_type, call_data, timeout=30):
        """
        # sends a call to the api and returns the response as a string
        # call_type - should be one of: init, track, reinforce
        # call_data - dictionary of call specific data
        # timeout - in seconds
        """

        # prepare the api call data structure
        data = {
            'appID': self.appID,
            'token': self.token,
            'versionID': self.versionID,
            'build': self.build,
            'ClientOS': self._client_os,
            'ClientOSVersion': self._client_os_version,
            'ClientAPIVersion' : self._client_sdk_version
        }

        if(self.inProduction):
            data['key'] = self.production_key
        else:
            data['key'] = self.dev_key

        # add the specific call data
        data.update(call_data)

        # append the current local and utc timestamps
        data.update(make_time())

        # launch POST request
        url = '{}/v2/app/{}/{}/'.format(self._server_url, self.appID, call_type)

        if self._debug:
            print('[Debug] api call, type: {}'.format(call_type))

        req = urllib2.Request(url, json.dumps(data), {'Content-Type': 'application/json'})
        try:
            raw_data = urllib2.urlopen(req, timeout=timeout).read()
            response = json.loads(raw_data)

            if response['status'] != STATUS['OK']:
                raise Exception('Error: request to dopamine api failed, bad status code.\n{}'.format(response))

        except urllib2.HTTPError:
            Exception('Error: request to dopamine api failed, bad call format.\n{}'.format(data))
            return None

        except ValueError:
            Exception('Error: request to dopamine api failed, bad server response.\n{}'.format(response))
            return None

        except:
            return None

        #if self._debug:
            #print('[Debug] api response:\n{}'.format(response))

        return response

    def init(self):
        """ init api call, only needs to be run once to register app internally """

        init_call = {
            'identity': [{'user': 'INIT'}],
            'rewardFunctions': self.reward_functions,
            'feedbackFunctions': self.feedback_functions,
            'actionPairings': self.action_pairings
        }

        return self.call('init', init_call)

    def track(self, identity, eventName, metaData):
        """ tracking api call """

        track_call = {
            'identity': identity,
            'eventName': eventName,
            'metaData': metaData
        }

        return self.call('track', track_call)

    def reinforce(self, identity, eventName, metaData, timeout=10):
        """ reinforce api call, will respond with default feedback function if response fails """

        reinforce_call = {
            'identity': identity,
            'eventName': eventName,
            'metaData': metaData
        }

        response = self.call('reinforce', reinforce_call, timeout=timeout)
        if response:
            return response

        # if the response from the server fails, use the first feedback (non-reward) function
        for reinforcer in self.pairings[eventName]:
            if reinforcer['type'] == 'Feedback':
                return {
                    'status': STATUS['ERROR'],
                    'reinforcementFunction': reinforcer['functionName']
                }

    @property
    def action_pairings(self):
        """ get the action pairings in the javascript friendly structure """

        return [
            {
                'actionName': name,
                'reinforcers': self.pairings[name]
            }
            for name in self.actions
        ]

    @property
    def build(self):
        return make_hash(self.action_pairings)

    def pair_action_to_reinforcement(self, action_name, function_name, reward=False, constraint=[], objective=[]):
        """ pair an action to a response function, set reward to true for reinforcing responses """

        pairing = {
            'functionName': function_name,
            'constraint': constraint,
            'objective': objective,
        }

        if action_name not in self.actions:
            self.actions.append(action_name)

        if reward:
            pairing['type'] = 'Reward'
            if function_name not in self.reward_functions:
                self.reward_functions.append(function_name)
        else:
            pairing['type'] = 'Feedback'
            if function_name not in self.feedback_functions:
                self.feedback_functions.append(function_name)

        for pair in self.pairings.setdefault(action_name, []):
            if function_name == pair['functionName']:
                #if self._debug:
                    #print('[Debug] function {} already paired to action {}'.format(function_name, action_name))
                break
        else:
            self.pairings[action_name].append(pairing)
            #if self._debug:
                #print('[Debug] function {} paired to action {}'.format(function_name, action_name))

        return

def make_time():
    """ return a dictionary with the current UTC and localTime """

    utcDateTime = datetime.utcnow()
    return {
        'UTC': calendar.timegm(utcDateTime.utctimetuple()) * 1000,
        'localTime': time.time() * 1000
    }

def make_hash(obj):
    """ create a SHA1 hexadecimal digest of a JSON compatible object """

    string = json.dumps(obj, sort_keys=True, indent=4, separators=(': ', ', '))
    hash_obj = hashlib.sha1(string);
    return hash_obj.hexdigest()



