import json
from typing import Callable

import event_handling
# from Server.mundo_sintetico.proceso.controlador.controlStrategy import ControlStrategy
import requests

from event_handling.event_handling import EventSubscriber


class AccessChatbot:

    def __init__(self):
        self.url = 'https://pserveronline.herokuapp.com/webhooks/rest/webhook'
        #'http://localhost:5005/webhooks/rest/webhook/'  ##change rasablog with your app name

    def response(self, mensaje, sender):
        myobj = {
            "message": str(mensaje),
            "sender": str(sender),
        }
        request_response = requests.post(self.url, json=myobj)
        return request_response

class ProcessActionBot:

    def __init__(self):
        # publisher = event_handling.EventPublisher("log_eventos")
        self.process_action_bot = AccessChatbot()
        self.consumer = EventSubscriber("log_eventos")
        self.consumer.subscribe("message", self.callbackProcess)
        self.consumer.subscribe("starting_meeting", self.callbackStartMeet)
        self.consumer.subscribe("ended_meeting", self.get_callback_time_meeting("ended"))
        self.consumer.start_listening()

    def callbackProcess(self,ch, method, properties, body):
        body_json = json.loads(body)
        if 'message' in body_json:
            print(body_json['message'])
            sender = "Server"
            if 'from' in body_json:
                sender = body_json["from"]
            message_receive = self.process_action_bot.response(body_json['message'], sender).json()
            self.print_message(message_receive)
        # publisher.publish("process_to_agile_bot", {"text": message_receive["text"]})
        return self.callbackProcess


    def callbackStartMeet(self,ch, method, properties, body):
        body_json = json.loads(body)
        message = ""
        if ("time" in body_json) and ("meeting_id" in body_json):
            message = "The meeting " + str(body_json["meeting_id"]) + " started: " + str(body_json["time"])
            print(message)
            message_receive = self.process_action_bot.response(message, "Server").json()
            self.print_message(message_receive)
        return self.callbackStartMeet


    def get_mensaje(self,meeting_id: str, time: str, timeinit: str) -> str:
        message = "The meeting " + meeting_id + " " + timeinit + ": " + time
        return message


    def get_message_participations(self,d : dict) -> str:
        message = ""
        if "participations" in d:
            participaciones = d["participations"]
            message = "The participations of the team members in the meeting are: ["
            list_particip = []
            for key, value in participaciones.items():
                item_participacion = str(key) + ":" + str(len(value))
                list_particip.append(item_participacion)
            for item in list_particip:
                message = message + str(item) + ","
            message = message[:-1]  # Elimina la ultima coma
            message = message + "]"
        return message

    def get_callback_time_meeting(self,type: str) -> Callable:
        def callbackTimeMeet(ch, method, properties, body):
            body_json = json.loads(body)
            if ("time" in body_json) and ("meeting_id" in body_json):
                message = self.get_mensaje(str(body_json["meeting_id"]), str(body_json["time"]), type)
                print(message)
                message_receive = self.process_action_bot.response(message, "Server").json()
                self.print_message(message_receive)
            if ("participations" in body_json):
                message = self.get_message_participations(body_json)
                print(message)
                message_receive = self.process_action_bot.response(message, "Server").json()
                self.print_message(message_receive)
        return callbackTimeMeet

    def print_message(self, message_receive):
        i=0
        for x in message_receive:
            if i==0:
                print("Message from: "+str(x['recipient_id']))
            print("ProcessActionBot: "+str(x['text']))
            i=i+1
        print(" ")
process=ProcessActionBot()
