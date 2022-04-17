from typing import Any, Text, Dict, List
import json
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from collections import Counter
import spacy
nlp = spacy.load("en_core_web_sm")


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

def extractNamedEntity(sentence):
    out = nlp(sentence)
    entity = ''
    named_entities = []
    tag_lst = []
    for word in out:
        entity = ''
        named_entity = None
        term = word.text 
        tag = word.ent_type_
        
        if tag:
            
            entity = ' '.join([entity, term])
            entity = entity.strip()
            named_entity = (entity, tag)
            named_entities.append(named_entity)
            tag_lst.append(tag)
        else:
          continue

    return named_entities, tag_lst

def returnNamedEntity(text):

    named_entities, tag_lst = extractNamedEntity(text)

    count_tags = Counter(tag_lst)
    count_tags_keys = list(count_tags.keys())

    entities = []
    for count_tag_key in count_tags_keys:
        value = count_tags[count_tag_key]
        entity = ''
        for named_entity in named_entities:
    
            if count_tag_key == named_entity[1]:
                entity = ' '.join([entity, named_entity[0]])
        entities.append((entity.strip(), count_tag_key))

    return entities




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


class ActionCustomQuery(Action):
    def name(self) -> Text:
        return 'action_custom_query'

    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        userMessage = tracker.latest_message['text']
        entity = returnNamedEntity(userMessage)
        for ent in entity:
            if ent[1] == 'DATE':
                reply = [(item["value"], item['entity']) for item in data if item["attribute"] == 'DATE_FOUNDED']
                for rep in reply:
                    if rep[0] == ent[0]:
                        dispatcher.utter_message(text=rep[1] + ' was founded in ' + rep[0])

            elif ent[1] == 'ORG':
                reply = [(item["entity"], item['attribute'], item['value']) for item in data if item["entity"] == ent[0] or item["value"] == ent[0]]
                if reply == []:
                    dispatcher.utter_message(text='No data available')
                for rep in reply:
                    if rep[1] == 'FOUNDED_BY':
                        dispatcher.utter_message(text=rep[2] + ' was founded by ' + rep[0])
                    elif rep[1] == 'CEO':
                        dispatcher.utter_message(text=rep[2] + ' is the CEO of ' + rep[0])
                    elif rep[1] == 'HEADQUARTERS':
                        dispatcher.utter_message(text=rep[2] + ' is the headquater of ' + rep[0])
                    
        return []
