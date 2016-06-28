# What is DopamineKit?
Boost retention and user engagement in your python app

DopamineKit provides wrappers for accessing the DopamineAPI and expressive UI reinforcements for your app.

Get your free API key at [http://dashboard.usedopamine.com/](http://dashboard.usedopamine.com/)

Learn more at [http://usedopamine.com](http://usedopamine.com)

### Looking for an Android Example App?

Check test.py for an example of how to use this package in your code.

## Set up DopamineKit

  1. First, make sure you have received your API key and other credentials, which are in the configuration file __dopamineproperties.json__ automatically generated from the [Dopamine Developer Dashboard](http://dashboard.usedopamine.com). 

  2. Import DopamineKit by copying the source code from [`/dopaminekit/dopaminekit.py`](dopaminekit/dopaminekit.py)' or by using `pip` or `easy_install`
  ```
  easy_install dopaminekit
  ```

  3. To use DopamineKit from library

  ```python
  from dopaminekit import DopamineKit
  ```
    
  4. 
  
  5. Start using Dopamine! The main features of DopamineAPI are the `reinforce()` and `track()` functions. These should be added into the response functions of any _action_ to be reinforced or tracked.
  

### Actions that represent Habits

Reinforce your apps ​_essential_​ actions; what users come to your app to do. Three actions is definitely enough, and one is often best. 

Our "To Do List" app ​_exists_​ to help uses be more productive by completing items on their list. So we will reinforce that. 

![Workspace screenshot](readme/Opaque workspace.png)

 - __Note:__ The possible return strings ["stars", "medalStar", "thumbsUp"] were configured on the [developer dashboard](http://dashboard.usedopamine.com).

### Responding to an Action
When the user completes a task, they will swipe it off of their check-list. When this happens, `DopamineKit.reinforce()` is called. 

 - __Note:__ The chosen form of reinforcement in this example app is using a `CandyBar` from DopamineKit. Developers should use visual reinforcement that meshes well with their UX, and the `CandyBar` is shown as a general solution.

There are 4 possible paths, shown by the `if-else` statements, that can be taken based on the resulting `reinforcement` string:

 - 3 out of the 4 paths were chosen by the app developer on the [Dopamine Developer Dashboard](http://dashboard.usedopamine.com).

 - The default case, or “neutral response", no reward will be delivered. This builds anticipation for the next surprising reward.
  
  
## Super Users

There are additional parameters for the `track()` and `reinforce()` functions that are used to gather rich information from your app and better create a user story of better engagement.

========

####Tracking Calls

A tracking call should be used to record and communicate to DopamineAPI that a particular action has been performed by the user, each of these calls will be used to improve the reinforcement model used for the particular user. The tracking call itself is asynchronous and non-blocking. Failed tracking calls will not return errors, but will be noted in the log.

######General syntax

```
Dopamine.track(context, actionID, metaData, secondaryIdentity)
```

######Parameters:

 - `context: Context` - is used to get API credentials from `res/raw/dopamineproperties.json` of the context's package
 
 - `actionID: String` - is a unique name for the action that the user has performed

 - `metaData: Map<String, String>` - (optional) is any additional data to be sent to the API

 - `secondaryIdentity: String` - (optional) is an extra identifier (like login credentials) used to identify a particular user

========

####Reinforcement Calls

A reinforcement call should be used when the user has performed a particular action that you wish to become a 'habit', the reinforcement call will return the name of the feedback function that should be called to inform, delight or congratulate the user. The names of the reinforcement functions, the feedback functions and their respective pairings may be found and configured on the developer dashboard.

######General syntax

```
Dopamine.reinforce(context, actionID, metaData, secondaryIdentity, callback)
```

######Parameters:

 - `context: Context` - is used to get API credentials from `res/raw/dopamineproperties.json` of the context's package
 
 - `actionID: String` - is a unique name for the action that the user has performed

 - `metaData: Map<String, String>` - (optional) is any additional data to be sent to the API

 - `secondaryIdentity: String` - (optional) is an extra identifier (like login credentials) used to identify a particular user across apps

 - `callback: DopamineKit.ReinforcementCallback` - is an object on which `onReinforcement(String reinforcement)` is called when a response is received

The reinforcement call itself takes the actionID as a required parameter, as well as a DopamineKit.ReinforcementCallback object, which is triggered as a callback for the reinforcement response.

========

####dopamineproperties.json

`dopamineproperties.json ` _must_ be contained within the directory _`app/src/main/res/raw`_. This property list contains configuration variables needed to make valid calls to the API, all of which can be found on your developer dashboard:

 - `appID: String` - uniquely identifies your app, get this from your [developer dashboard](http://dev.usedopamine.com).

 - `versionID: String` -  this is a unique identifier that you choose that marks this implementation as unique in our system. This could be something like 'summer2015Implementation' or 'ClinicalTrial4'. Your `versionID` is what we use to keep track of what users are exposed to what reinforcement and how to best optimize that.

 - `inProduction: Bool` - indicates whether app is in production or development mode, when you're happy with how you're integrating Dopamine and ready to launch set this argument to `true`. This will activate optimized reinforcement and start your billing cycle. While set to `false` your app will receive dummy reinforcement, new users will not be registered with our system, and no billing occurs.

 - `productionSecret: String` - secret key for production

 - `developmentSecret: String` - secret key for development
