# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import json
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
from gensim.models.doc2vec import Doc2Vec
from gensim.parsing.preprocessing import preprocess_string
import spacy


with open('kb.json', 'r') as f:
    data = json.load(f)


def isWordPresent(sentence, word):
 
    word = word.upper()
    sentence = sentence.upper()
    lis = sentence.split()
    if(lis.count(word) > 0):
        return True
    else:
        return False



class ActionCompanyInfo(Action):
    def name(self) -> Text:
        return 'action_company_info'

    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        userMessage = tracker.latest_message['text']

        if isWordPresent(userMessage, 'ceo'):
            reply = [(item["value"], item['entity']) for item in data if item["attribute"] == 'CEO']
            for i in range(len(reply)):
                dispatcher.utter_message(text=reply[i][0] + ' is the CEO of ' + reply[i][1])
                
        elif isWordPresent(userMessage, 'subsidiaries'):
            reply = [(item["value"], item['entity']) for item in data if item["attribute"] == 'SUBSIDIARY_OF']
            for i in range(len(reply)):
                dispatcher.utter_message(text=reply[i][1] + ' is the Subsidiary of ' + reply[i][0])

        elif isWordPresent(userMessage, 'founders'):
            reply = [(item["value"], item['entity']) for item in data if item["attribute"] == 'FOUNDED_BY']
            for i in range(len(reply)):
                dispatcher.utter_message(text=reply[i][0] + ' founded ' + reply[i][1])
        
        elif isWordPresent(userMessage, 'headquarters'):
            reply = [(item["value"], item['entity']) for item in data if item["attribute"] == 'HEADQUARTERS']
            for i in range(len(reply)):
                dispatcher.utter_message(text=reply[i][0] + ' is the headquarter of ' + reply[i][1])
        
        elif isWordPresent(userMessage, 'foundation'):
            reply = [(item["value"], item['entity']) for item in data if item["attribute"] == 'DATE_FOUNDED']
            for i in range(len(reply)):
                dispatcher.utter_message(text=reply[i][1] + ' was founded on ' + reply[i][0])

        return []
