# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import requests
import pandas as pd
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import joblib

def cont_res_ret():
    api_url = "http://127.0.0.1:8000/api/content-detail/"
    content_id = "http://127.0.0.1:8000/api/content-id/"
        
    resid = requests.get(content_id).json()
    cid = resid['itemid']
       
    content_id = str(cid)
    URL = api_url+content_id
    response = requests.get(URL).json() 
    return response

def item_res_ret():
    api_url = "http://127.0.0.1:8000/api/item-detail/"
    item_id = "http://127.0.0.1:8000/api/content-id/"
        
    resid = requests.get(item_id).json()
    cid = resid['itemid']
       
    content_id = str(cid)
    URL = api_url+content_id
    response = requests.get(URL).json() 
    return response

def username():
    infou = "http://127.0.0.1:8000/api/content-id/"
    response = requests.get(infou).json()
    username = response['usern'] 
    return username

rl =[]
class ActionCI(Action):

    def name(self) -> Text:
        return "action_cost"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        ent = tracker.latest_message['entities']
        api_url = "http://127.0.0.1:8000/api/content-detail/"
        content_id = "http://127.0.0.1:8000/api/content-id/"
        
        resid = requests.get(content_id).json()
        cid = resid['itemid']
        
        content_id = str(cid)
        URL = api_url+content_id
        response = requests.get(URL).json()

        for e in ent:
            if e['entity'] == 'info':
                val = e['value']
                if val.lower()=='cost' or val.lower()== 'price':
                    msg = str(response['cost'])
                    rl.append(response['cost'])
                    # dispatcher.utter_message(text=msg)
                else:
                    msg="No details"    
            dispatcher.utter_message(text=msg)
        

        return []


class ActionRec(Action):

    def name(self) -> Text:
        return "action_recommendn"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ent = tracker.latest_message['entities']     
        lis=joblib.load("prediction/costknn.pkl")

        model = lis[0]
        df = lis[1]
        response_it = item_res_ret()
        response_con = cont_res_ret()    

        it = response_it['title']
        ds = response_con['specs']
        print(it,ds)
        q_df = df[df['item_copy'].str.contains(it) & df['Description_copy'].str.contains(ds)]
        if q_df is not None:
            i = q_df['item'].values
            j = q_df['Description'].values
            x = pd.DataFrame([[i[0],j[0]]])
            recomp = int(model.predict(x)[0])
            rl.append(recomp)
            pred = str(recomp)
        else:
            pred = "Not Found any records"  
        msg = "Present Market Price is {}".format(pred)
        dispatcher.utter_message(text=msg)
        
        if int(pred) > response_con['cost']:
            dispatcher.utter_message(text="PNECBS is showing the best price")
        else:
            dispatcher.utter_message(text= "Dont worry, We are providing some extra benefits")
        return []

trade=[]
class ActionPR(Action):

    def name(self) -> Text:
        return "action_Postrec"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ent = tracker.latest_message['entities']    
        response_con = cont_res_ret()   
        response_it = item_res_ret()
        
        if response_con['cost'] <= rl[-1]:
            print(rl[-1])
            print(response_con['cost'])
            msg = "Sorry {}, This is the best price that U could get.".format(username())    
            dispatcher.utter_message(text= msg)
        else:
                
            lis=joblib.load("prediction/costknn.pkl")
            df = lis[1]

            l = []
            it = response_it['title']
            ds = response_con['specs']
            q_df = df[df['item_copy'].str.contains(it) & df['Description_copy'].str.contains(ds)]

            minv = response_con['cost']

            x =int(q_df['Min'].values[0])    
            if minv > x:
                minv = x
            LB = minv + 0.1*(minv)
            print(LB)
            l.append(response_con['cost'])
            l.append(int(rl[0]))

            if len(trade) == 0:
                msg = (l[0]+l[1])/2
                trade.append(msg)
            print(trade)    

            if LB > trade[-1]:
                print(LB)
                msgx = "Sorry, {} is the best and final price that U could get.".format(trade[-1])    
                dispatcher.utter_message(text= msgx)
            else:
                msg = (trade[-1]) - 0.09*(trade[-1])    
                trade.append(msg)
                msgx = str(trade[-1])
                dispatcher.utter_message(text= msgx)
                dispatcher.utter_message(text= "We are providing all the necessary Accessories")
                dispatcher.utter_message(text= "U might not get these things anywhere else")
        return []

class ActionCart(Action):

    def name(self) -> Text:
        return "action_cart"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ent = tracker.latest_message['entities']    
        msg = "Ok,{} taking you to cart".format(username())
        dispatcher.utter_message(text=msg)
        if len(trade)!=0:            
            msg = "Your final price is {}".format(trade[-1])
            dispatcher.utter_message(text=msg)
        else:
            msg = "Your final price is {}".format(rl[-1])
            dispatcher.utter_message(text=msg)

        return []

class ActionFinal(Action):

    def name(self) -> Text:
        return "action_final"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ent = tracker.latest_message['entities'] 
        response_con = cont_res_ret()      
        
        if len(trade)==0:
            dispatcher.utter_message(text=str(response_con['cost']))

        elif len(trade)==3:
            dispatcher.utter_message(text="Would u like to see another comodity of same specs?")
            lis=joblib.load("prediction/costknn.pkl")
            df = lis[1]
            response_it = item_res_ret()
            l = []
            it = response_it['title']
            ds = response_con['specs']
            q_df = df[df['item_copy'].str.contains(it) & ~df['Description_copy'].str.contains(ds)]
            dispatcher.utter_message(text="There is an alternative commodity - {}".format(q_df['Description_copy']))
        else:
            dispatcher.utter_message(text=str(trade[-1]))
            dispatcher.utter_message(text="Sorry {}, This is the best price that U could get.".format(username()))
        print(trade)
        return []
