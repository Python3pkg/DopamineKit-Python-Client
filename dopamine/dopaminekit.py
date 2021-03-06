import urllib.request, urllib.error, urllib.parse
import json
from datetime import datetime
import calendar
import time
import sys

class DopamineKit(object):
    def __init__(self, appID, developmentSecret, productionSecret, versionID, inProduction, debugmode = False):
        """
        Creates a DopamineKit object to communicate with the DopamineAPI

        Parameters:
        ----------
        - appID : str
            Uniquely identifies your app, get this from your [developer dashboard](http://dev.usedopamine.com).

        - developmentSecret : str
            Secret key for development.

        - productionSecret : str
            Secret key for production.

        - versionID : str
            This is a unique identifier that you choose that marks this implementation as unique in our system. This could be something like 'summer2015Implementation' or 'ClinicalTrial4'. Your `versionID` is what we use to keep track of what users are exposed to what reinforcement and how to best optimize that.

        - inProduction : bool
            Indicates whether app is in production or development mode, when you're happy with how you're integrating Dopamine and ready to launch set this argument to `true`. This will activate optimized reinforcement and start your billing cycle. While set to `false` your app will receive dummy reinforcement, new users will not be registered with our system, and no billing occurs.

        - debugmode : bool = False
            Enables debug mode, where the sent and received data are printed
        """

        self.appID = appID
        self.developmentSecret = developmentSecret
        self.productionSecret = productionSecret
        self.versionID = versionID
        self.inProduction = inProduction
        self._debugmode = debugmode

        return


    def track(self, actionID, identity, metaData=None):
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

        """

        if isinstance(actionID, str)==False:
            print(('[DopamineKit] - tracking() has invalid "actionID"-"{}"'.format(actionID)))
            return
        if isinstance(identity, str)==False:
            print(('[DopamineKit] - tracking() has invalid "identity"-"{}"'.format(identity)))
            return

        track_call = {
            'primaryIdentity': identity,
            'actionID': actionID,
        }
        if metaData!=None and isinstance(metaData, dict)==False:
            print(('[DopamineKit] - tracking() has invalid "metaData"-"{}" - ignoring metaData and sending call'.format(metaData)))
        else:
            track_call['metaData'] = metaData

        return self.call('track', track_call, 5)


    def reinforce(self, actionID, identity, metaData=None, timeout=5):
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

        """

        reinforce_call = {
            'primaryIdentity': identity,
            'actionID': actionID,
            'metaData': metaData
        }

        response = self.call('reinforce', reinforce_call, timeout)
        return response



############
## Internal / Private
############

    _client_os = 'python'
    _client_os_version = str(sys.api_version)
    _client_sdk_version = '3.0.0'
    _server_url = 'https://api.usedopamine.com/v3/app'

    # _debugmode = False               # Set to true to print sent/received messages. Set in __init__

    
    def call(self, call_type, call_data, timeout):
        """
        Sends a call to the DopamineAPI and returns the response as a string

        Parameters:
        ----------
        - call_type : str
            Has to be either 'track' or 'reinforce'

        - call_data : dict
            Dictionary of call-specific data

        - timeout : int
            Time to wait for a response in seconds
        """

        if(call_type != 'track' and call_type != 'reinforce'):
            print(('[DopamineKit] - invalid call_type:{}'.format(call_type)))
            return None

        # prepare the api call data structure
        data = {
            'appID': self.appID,
            'versionID': self.versionID,
            'clientOS': self._client_os,
            'clientOSVersion': self._client_os_version,
            'clientSDKVersion' : self._client_sdk_version
        }

        if(self.inProduction):
            data['secret'] = self.productionSecret
        else:
            data['secret'] = self.developmentSecret

        # add the specific call data
        data.update(call_data)

        # append the current local and utc timestamps
        data.update(self.get_time_utc_local())

        # launch POST request
        url = '{}/{}/'.format(self._server_url, call_type)

        if self._debugmode:
            print(('[DopamineKit] - api call type: {} to url: {}'.format(call_type, url)))
            print(('[DopamineKit] - call data: {}'.format(data)))

        req = urllib.request.Request(url, json.dumps(data), {'Content-Type': 'application/json'})
        try:
            raw_data = urllib.request.urlopen(req, timeout=timeout).read()
            response = json.loads(raw_data)
            if self._debugmode:
                print(('[DopamineKit] - api response:\n{}'.format(response)))

        except urllib.error.HTTPError as e:
            print(('[DopamineKit] - HTTPError:\n' + str(e)))
            return None
        except urllib.error.URLError as e:
            print(('[DopamineKit] - URLError:\n' + str(e)))
            return None
        except httplib.HTTPException as e:
            print(('[DopamineKit] - HTTPException:\n' + str(e)))
            return None
        except Exception:
            import traceback
            print(('[DopamineKit] - generic exception:\n' + traceback.format_exc()))
            return None


        if(call_type == 'reinforce'):
            try:
                if response['status'] == 200:
                    return response['reinforcementDecision']
                else:
                    print(('[DopamineKit] - request to DopamineAPI failed, bad status code. Returning "neutralResponse"\n{}'.format(json.dumps(response, indent=4))))
                    return "neutralResponse"
            except KeyError as e:
                print(('[DopamineKit] - bad response received, no "reinforcementDecision" found:\n{}'.format(json.dumps(response, indent=4))))
        else:
            return response

    def get_time_utc_local(self):
        """ 
        Returns a dictionary with the current 'UTC' and 'localTime' 
        """

        utcDateTime = datetime.utcnow()
        return {
            'UTC': calendar.timegm(utcDateTime.utctimetuple()) * 1000,
            'localTime': time.time() * 1000
        }


