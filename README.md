# DopamineAPI_Python-Client
Boost retention and user engagement in your python app

Check test.py for an example of how to use this package. 

The methods explained

The ```call``` method makes all of the https requests and preforms general validations on the responses. 

The ```init```, ```track```, and ```reinforce``` calls package data for the call method and preform call-type specific validation checks.


```pair_action_to_reinforcement``` tells the doapmine algorythm that a particular reinforement function is apropriate for a particular action. ```action_pairings``` gets all the reinforcement/action pairings in a format that the API can understand. 