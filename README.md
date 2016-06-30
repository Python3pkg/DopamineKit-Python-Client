# What is DopamineKit?
Boost retention and user engagement in your python app

DopamineKit provides wrappers for accessing the DopamineAPI and expressive UI reinforcements for your app.

Get your free API key at [http://dashboard.usedopamine.com/](http://dashboard.usedopamine.com/)

Learn more at [http://usedopamine.com](http://usedopamine.com)

### Looking for an example?

Check [/test.py](./test.py) for an example of how to use this package in your code.

## Set up DopamineKit

  1. First, make sure you have received your API key and other credentials, which are automatically generated from the [Dopamine Developer Dashboard](http://dashboard.usedopamine.com). 

  2. Import DopamineKit by copying the source code from [`/dopaminekit/dopaminekit.py`](dopaminekit/dopaminekit.py)' or by using `pip` or `easy_install`
  
  ```
  pip install dopaminekit
  ```

  3. First import the class `DopamineKit` from the library `dopamine`

  ```python
  from dopamine import DopamineKit
  ```
    
  4. Create a DopamineKit object with your credentials passed in as Strings
  
    ```
    app_id = 'genereated from dashboard.usedopamine.com'
    development_secret = 'genereated from dashboard.usedopamine.com'
    production_secret = 'genereated from dashboard.usedopamine.com'
    versionID = 'testing'
    production_mode = False
    debug_mode = True		# Prints out the sent/received data

    
    dopaminekit = DopamineKit(app_id, development_secret, production_secret, versionID, production_mode, debug_mode)
    ...
    
    dopaminekit.track('testEvent1', '1138', [{'metaDataKey':'value'}])
    ...
    reinforcementFunction = dopaminekit.reinforce('action1', '1137')
    
    ```
    
  5. Start using Dopamine! The main features of DopamineAPI are the `reinforce()` and `track()` functions. These should be added into the response functions of any _action_ to be reinforced or tracked.
  
  
## Super Users

There are additional parameters for the `track()` and `reinforce()` functions that are used to gather rich information from your app and better create a user story of better engagement.

========

####Object Initialization

The object initialization takes in the API credentials (appID, development and production secrets, and the versionID). There are also the options inProduction, which selects between the development and billed production mode, and debugmode, which prints out the sent and received API calls when set to True.

######General syntax

```
dopaminekit = DopamineKit(appID, developmentSecret, productionSecret, versionID, inProduction, debugmode=False)
```

######Parameters:
 - `appID: str` - Uniquely identifies your app, get this from your [developer dashboard](http://dev.usedopamine.com).

 - `developmentSecret : str` - secret key for development

 - `productionSecret : str` - secret key for production

 - `versionID : str` -  this is a unique identifier that you choose that marks this implementation as unique in our system. This could be something like 'summer2015Implementation' or 'ClinicalTrial4'. Your `versionID` is what we use to keep track of what users are exposed to what reinforcement and how to best optimize that.

 - `inProduction : bool` - indicates whether app is in production or development mode, when you're happy with how you're integrating Dopamine and ready to launch set this argument to `true`. This will activate optimized reinforcement and start your billing cycle. While set to `false` your app will receive dummy reinforcement, new users will not be registered with our system, and no billing occurs.

 - `debugmode : bool` - Enables debug mode, where the sent and received data are printed


========

####Tracking Calls

A tracking call should be used to record and communicate to DopamineAPI that a particular action has been performed by the user, each of these calls will be used to improve the reinforcement model used for the particular user. The tracking call itself is asynchronous and non-blocking. Failed tracking calls will not return errors, but will be noted in the log.

######General syntax

```
Dopamine.track(actionID, identity, metaData=None)
```

######Parameters:
 - `actionID : str` - A descriptive name for action that the user has performed

 - `identity : str` - A string used to identify a particular user, such as an email or username or UUID.

 - `metaData : dict = None` - An optional dictionary containing extra data about the user or environment to generate better results.

========

####Reinforcement Calls

A reinforcement call should be used when the user has performed a particular action that you wish to become a 'habit', the reinforcement call will return the name of the feedback function that should be called to inform, delight or congratulate the user. The names of the reinforcement functions, the feedback functions and their respective pairings may be found and configured on the developer dashboard.

######General syntax

```
Dopamine.reinforce(actionID, identity, metaData=None, timeout=5)
```

######Parameters:

 - `actionID : str` - A descriptive name for action that the user has performed

 - `identity : str` - A string used to identify a particular user, such as an email or username or UUID.

 - `metaData : dict = None` - An optional dictionary containing extra data about the user or environment to generate better results.

- `timeout : int = 5` - An optional timeout parameter in seconds to wait for a response. Default is 5.

