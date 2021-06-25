# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from actions.procesamiento.controlStrategy import ControlStrategy

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
 
import json
from typing import Dict, Callable

from rasa_sdk.events import SlotSet

import requests
from actions.event_handling import EventPublisher
controlStrategy=ControlStrategy()
publisher=EventPublisher("log_eventos")

url='http://localhost:5005/webhooks/rest/webhook/'
def response(sender:str, message:str, metadata:str):
    myobj = {
        "message": message,
        "sender": sender,
        "metadata": {"text": metadata}
    }
    x = requests.post(url, json = myobj)

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent_name=tracker.latest_message['intent'].get('name')
        artefacto=""
        id_reunion=""
        agile_bots=""
        if intent_name == "reunion":
            texto=tracker.latest_message.get('text')
            list_text=texto.split(";")
            i=0
            for palabra in list_text:
                print(palabra)
                if (i==0):
                    agile_bots=palabra
                else:
                    if (i==1):
                        artefacto=palabra
                    else:
                        if (i==2):
                            message=palabra
                        else:
                            if (i==3):
                                id_reunion=palabra
                i=i+1
            dispatcher.utter_message(text="Generar: "+str(artefacto)+" id: "+str(id_reunion)+ " Participan: "+ str(agile_bots))
        if intent_name == "propuesta_reunion":
            texto=tracker.latest_message.get('text')
            list_text=texto.split(" ")
            i=0
            equipo=""
            fecha=""
            for palabra in list_text:
                if (i==3):
                    equipo=palabra
                else:
                    if (i==4):
                        fecha=palabra
                i=i+1
            dispatcher.utter_message(text="Irrelevante al proceso: Posible reunion+" + "id:" +str(equipo)+ "Fecha: "+ str(fecha))
        if intent_name == "confirmacion_propuesta_reunion":
            texto=tracker.latest_message.get('text')
            list_text=texto.split(" ")
            i=0
            equipo=""
            fecha=""
            for palabra in list_text:
                print(palabra)
                if (i==4):
                    equipo=palabra
                else:
                    if (i==5):
                        fecha=palabra
                i=i+1
            dispatcher.utter_message(text="Generar reunion " + "Equipo: " +str(equipo)+ " Fecha: "+ str(fecha))
        sender_id = tracker.current_state()['sender_id']
        dispatcher.utter_message(text="Sender id: "+str(sender_id))
        return []

class ActionStrategy(Action):

    def name(self) -> Text:
        return "action_strategy"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent_name=tracker.latest_message['intent'].get('name')
        ent = next(tracker.get_latest_entity_values("id_reunion"), None)
        d_send={"intent": str(intent_name), "data": {"id": str(ent)}}
        print(d_send)
        dispatcher.utter_message(text="Reunion "+str(ent)+ " finalizada")
        #event_publisher.publish(str(intent_name),d_send)
        return []

def get_list_string (palabra : str) -> List:
    task_string=palabra.split("[")
    print(task_string)
    task_string2=str(task_string[1]).split("]")
    task_string3=str(task_string2[0]).split(",")
    task_string4=[]
    for x in task_string3:
        x_string=str(x)
        if x_string.find(" ") == -1:
            task_string4.append(x_string)
        else:
            x_string=x_string[1:]
            task_string4.append(x_string)
    return task_string4

def metricas_tareas(tracker: Tracker, dispatcher: CollectingDispatcher) -> dict:
    task_string=str(tracker.latest_message.get("text")).split("[")
    task_string2=str(task_string[1]).split("]")
    if len(task_string)> 2: # Si se agrega "y fui a las reuniones [1]"
        reuniones=get_list_string(str("[")+task_string[2])
        dispatcher.utter_message(text="El agilebot asistio a las reuniones: "+str(reuniones))
    task_string3=str(task_string2[0]).split(",")
    dict_tareas={}
    lista_tareas=[]
    for x in task_string3:
        x_string=str(x)
        list_horas=x_string.split(":")
        dict_tarea={}
        id_tarea=""
        horas_trabajadas=""
        horas_totales=""
        i=0
        for items in list_horas:
            if (i==0):
                if str(items).find(" ") == -1:
                    id_tarea=str(items)
                else:
                    id_tarea=str(items)
                    id_tarea=id_tarea[1:]
            if (i==1):
                horas_trabajadas=items
            if (i==2):
                horas_totales=items
            i=i+1
            print(str(items))
        d_horas={"horas_trabajadas":str(horas_trabajadas), "horas_totales":str(horas_totales)}
        dict_tarea[str(id_tarea)]=d_horas
        lista_tareas.append(dict_tarea)
    dict_tareas={"Tareas":lista_tareas}
    return dict_tareas

class ActionTasks(Action):

    def name(self) -> Text:
        return "action_tasks"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #Gets the lattest_message from the tracker 
        # and returns a dictionary
        #{Tasks: ["task_id": {hours_worked: value, total_hours: value}]
        dict_data=metricas_tareas(tracker,dispatcher)
        dict_tareas={"intent": "working_on_tha_tasks", "data":dict_data}
        message=controlStrategy.process_intent(dict_tareas)
        response("ProcessActionBot","notificar a Josh",message)
        dispatcher.utter_message(message)
        return []

class ActionGoMeeting(Action):

    def name(self) -> Text:
        return "action_go_meeting"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ent_reunion = next(tracker.get_latest_entity_values("id_reunion"), None)
        ent_agilebot= next(tracker.get_latest_entity_values("id_agilebot"), None)
        dispatcher.utter_message("El agilebot: "+str(ent_agilebot)+" debe ir a la reunion: "+str(ent_reunion))
        return []

class ActionFacilitador(Action):

    def name(self) -> Text:
        return "action_facilitador"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ent_agilebot= next(tracker.get_latest_entity_values("id_facilitador"), None)
        dispatcher.utter_message("El agilebot: "+str(ent_agilebot)+" será el ScrumMaster / facilitador de la Daily")
        return []

class ActionMeetings(Action):

    def name(self) -> Text:
        return "action_meetings"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #intent_name=tracker.latest_message['intent'].get('name')
        palabra=str(tracker.latest_message.get("text"))
        task_string=get_list_string(palabra)
        message="El agilebot asistio a las reuniones: "+str(task_string)
        response("ProcessActionBot","notificar a Josh",message)
        dispatcher.utter_message(text=message)
        return []

class ActionStartMeeting(Action):

    def name(self) -> Text:
        return "action_start_meeting"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ent_fecha= next(tracker.get_latest_entity_values("fecha"), None)
        ent_hora= next(tracker.get_latest_entity_values("hora"), None)
        dispatcher.utter_message("La fecha de inicio de la reunion es: "+str(ent_fecha)+" y la hora es: "+str(ent_hora))
        return [SlotSet("fecha_start", str(ent_fecha)),SlotSet("hora_start", str(ent_hora))]

class ActionEndedMeeting(Action):

    def name(self) -> Text:
        return "action_ended_meeting"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ent_fecha= next(tracker.get_latest_entity_values("fecha"), None)
        ent_hora= next(tracker.get_latest_entity_values("hora"), None)
        ent_idreunion=next(tracker.get_latest_entity_values("id_reunion"), None)
        fecha_start=tracker.get_slot("fecha_start")
        hora_start=tracker.get_slot("hora_start")
        dispatcher.utter_message("La fecha de inicio de la reunion es: "+str(fecha_start)+ ", su hora: "+str(hora_start)+". La fecha de finalización de la reunion es: " + str(ent_fecha)+" y la hora es: "+str(ent_hora))
        fecha_inicio=str(fecha_start)+str(" ")+str(hora_start)
        fecha_fin=str(ent_fecha)+str(" ")+str(ent_hora)
        d_intent={"intent":"ended_meeting","data":{"id":str(ent_idreunion),"fecha_start": str(fecha_inicio),"fecha_ended":str(fecha_fin)}}
        if (fecha_start is not None) and (hora_start is not None):
            message=controlStrategy.process_intent(d_intent)
            response("ProcessActionBot","notificar a Josh",message)
            dispatcher.utter_message(message)
        return []


def get_participations(tracker: Tracker) -> dict:
    task_string=str(tracker.latest_message.get("text")).split("[")
    print(task_string)
    task_string2=str(task_string[1]).split("]")
    task_string3=str(task_string2[0]).split(",")
    dict_participations={}
    lista_particip=[]
    for x in task_string3:
        x_string=str(x)
        list_horas=x_string.split(":")
        dict_particip={}
        id_agilebot=""
        cant_particip=""
        i=0
        for items in list_horas:
            if (i==0):
                if str(items).find(" ") == -1:
                    id_agilebot=str(items)
                else:
                    id_agilebot=str(items)
                    id_agilebot=id_agilebot[1:]
            if (i==1):
                cant_particip=items
            i=i+1
            print(str(items))
        d_horas={"cant_particip":str(cant_particip)}
        dict_particip[str(id_agilebot)]=d_horas
        lista_particip.append(dict_particip)
    dict_participations={"Participations":lista_particip}
    return dict_participations

class ActionParticipations(Action):

    def name(self) -> Text:
        return "action_participations"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        d=get_participations(tracker)
        d_intent={"intent":"participations","data":d}
        message=controlStrategy.process_intent(d_intent)
        response("ProcessActionBot","notificar a Josh",message)
        dispatcher.utter_message(message)
        return []
    
class ActionControlMeetingFalse(Action):

    def name(self) -> Text:
        return "action_controlmeeting_false"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #Gets the lattest_message from the tracker 
        # and returns a dictionary
        #{Tasks: ["task_id": {hours_worked: value, total_hours: value}]
        ent_idreunion=next(tracker.get_latest_entity_values("id_reunion"), None)
        publisher.publish("message",{"message":"La reunion "+str(ent_idreunion)+" no fue realizada", "from": "ProcessActionBot", "to":"Scrum Master"})
        response("ProcessActionBot","notificar a Josh","La reunion "+str(ent_idreunion)+" no fue realizada")
        dispatcher.utter_message(text="Se informará al Scrum Master")
        return []

class ActionControlMeetingTrue(Action):

    def name(self) -> Text:
        return "action_controlmeeting_true"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #Gets the lattest_message from the tracker 
        # and returns a dictionary
        #{Tasks: ["task_id": {hours_worked: value, total_hours: value}]
        ent_idreunion=next(tracker.get_latest_entity_values("id_reunion"), None)
        publisher.publish("message",{"message":"La reunion "+str(ent_idreunion)+" fue realizada sin problemas", "from": "ProcessActionBot", "to":"Scrum Master"})
        response("ProcessActionBot","notificar a Josh","La reunion "+str(ent_idreunion)+" fue realizada sin problemas")
        dispatcher.utter_message(text="Se informará al Scrum Master")
        return []

class ActionHizoMeet(Action):

    def name(self) -> Text:
        return "action_hizo_meet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ent_membersmeeting=""
        ent_idreunion=next(tracker.get_latest_entity_values("id_reunion"), None)
        for entity in tracker.get_latest_entity_values("members_meeting"):
            if ent_membersmeeting=="":
                ent_membersmeeting=ent_membersmeeting+str(entity)
            else:
                ent_membersmeeting=ent_membersmeeting+", "+str(entity)
        if str(tracker.latest_message['intent']['name'])=="hizo_reunion":
            publisher.publish("message",{"message":"La reunion "+str(ent_idreunion)+" fue realizada sin problemas con el equipo formado por: "+str(ent_membersmeeting), "from": "ProcessActionBot", "to":"Scrum Master"})
            response("ProcessActionBot","notificar a Josh","La reunion "+str(ent_idreunion)+" fue realizada sin problemas con el equipo formado por: "+str(ent_membersmeeting))
        else:
            publisher.publish("message",{"message":"La reunion "+str(ent_idreunion)+" del equipo formado por: "+str(ent_membersmeeting)+" no se realizó", "from": "ProcessActionBot", "to":"Scrum Master"})
            response("ProcessActionBot","notificar a Josh","La reunion "+str(ent_idreunion)+" del equipo formado por: "+str(ent_membersmeeting)+" no se realizó")
        dispatcher.utter_message(text="Se informará al Scrum Master")
        return []

class ActionTareaHizo(Action):

    def name(self) -> Text:
        return "action_tareahizo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ent_agilebot= next(tracker.get_latest_entity_values("id_agilebot"), None)
        dispatcher.utter_message("El agilebot estuvo trabajando en la tarea: "+str(ent_agilebot))
        return []
