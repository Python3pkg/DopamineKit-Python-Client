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
    # """
    # Dopamine API interface class

    # appID -
    # dev_secret -
    # production_secret -
    # token -
    # versionID -

    # """

    identity = []
    _client_os = 'python'
    _client_os_version = sys.version
    _client_sdk_version = '0.1.0'
    _server_url = 'https://staging-api.usedopamine.com'

    _debug = True               # debug flag set to true for console messages

    def __init__(self, appID, dev_secret, production_secret, versionID, inProduction):

        self.appID = appID
        self.dev_secret = dev_secret
        self.production_secret = production_secret
        self.versionID = versionID
        self.inProduction = inProduction
        return

    def call(self, call_type, call_data, timeout=2):
        # """
        # sends a call to the api and returns the response as a string
        # call_type - should be one of: init, track, reinforce
        # call_data - dictionary of call specific data
        # timeout - in seconds
        # """

        # prepare the api call data structure
        data = {
            'appID': self.appID,
            'versionID': self.versionID,
            'clientOS': self._client_os,
            'clientOSVersion': self._client_os_version,
            'clientSDKVersion' : self._client_sdk_version
        }
        if(self.inProduction):
            data['secret'] = self.production_secret
        else:
            data['secret'] = self.dev_secret

        # add the specific call data
        data.update(call_data)

        # append the current local and utc timestamps
        data.update(make_time())

        # launch POST request
        url = '{}/v3/app/{}/'.format(self._server_url, call_type)

        if self._debug:
            print('[Debug] api call, type: {}'.format(call_type))

        req = urllib2.Request(url, json.dumps(data), {'Content-Type': 'application/json'})
        try:
            response = urllib2.urlopen(req, timeout=timeout).read()
            data = json.loads(response)

            if data['status'] != STATUS['OK']:
                raise Exception('Error: request to dopamine api failed, bad status code.\n{}'.format(response))

        except urllib2.HTTPError:
            Exception('Error: request to dopamine api failed, bad call format.\n{}'.format(data))
            return None

        except ValueError:
            Exception('Error: request to dopamine api failed, bad server response.\n{}'.format(response))
            return None

        except:
            return None

        if self._debug:
            print('[Debug] api response:\n{}'.format(response))

        return response

    def track(self, identity, actionID, metaData):
        # """ tracking api call """

        track_call = {
            'primaryIdentity': identity,
            'actionID': actionID,
            'metaData': metaData
        }

        return json.loads(self.call('track', track_call))

    def reinforce(self, identity, actionID, metaData, timeout=2):
        # """ reinforce api call, will respond with default feedback function if response fails """

        reinforce_call = {
            'primaryIdentity': identity,
            'actionID': actionID,
            'metaData': metaData
        }

        response = self.call('reinforce', reinforce_call, timeout=timeout)
        if response:
            return json.loads(response)


def make_time():
    # """ return a dictionary with the current UTC and localTime """

    utcDateTime = datetime.utcnow()
    return {
        'UTC': calendar.timegm(utcDateTime.utctimetuple()) * 1000,
        'localTime': time.time() * 1000
    }