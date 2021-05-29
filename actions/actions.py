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

import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from rasa_sdk.events import SlotSet

controlStrategy=ControlStrategy()

class EventPublisher:
    """Clase para publicar eventos en un servidor y exchange determinado.

    La documentacion de RabbitMQ recomienda separar la conexion de publicaciones
    de la de subscripciones. Tambien recomienda un canal por thread.

    Autor: Bruno.
    """

    def __init__(self, exchange_name: str, host: str = "amqps://urfvnqok:kDPF6YteXqwoKytSirWyl_HAisUjTGYl@woodpecker.rmq.cloudamqp.com/urfvnqok"):
        """Constructor.
        Crea una conexion al servidor de eventos solo para publicaciones.

        Autor: Bruno.

        :param exchange_name: nombre del exchange donde se publican los eventos.
        :param host: host donde esta corriendo el servidor de eventos.
        """
        self._exchange_name = exchange_name
        self._exchange_type = "topic"

        # Crea conexion y canal para publicaciones.
        self._publish_connection = pika.BlockingConnection(
            pika.URLParameters(host))
        self._publish_channel = self._publish_connection.channel()
        # Crea el exchange (si no existe).
        self._publish_channel.exchange_declare(
            # TODO Si salta una excepcion de pika poner en True.
            durable=False,
            exchange=self._exchange_name, exchange_type=self._exchange_type)

    def publish(self, event: str, payload: Dict) -> None:
        """Publica el evento dado en el exchange, junto con un diccionario
        que almacena su informacion.

        Autor: Bruno.

        :param event: evento a publicar.
        :param payload: diccionario con datos del evento.
        :return: None.
        """
        self._publish_channel.basic_publish(
            self._exchange_name, routing_key=event, body=json.dumps(payload))

    def close_connections(self) -> None:
        """Cierra el canal y la conexion realizada en el servidor de eventos.

        Autor: Bruno.

        :return: None.
        """
        self._publish_channel.close()
        self._publish_connection.close()

#event_publisher=EventPublisher("log_eventos")

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

def get_list_string (tracker: Tracker) -> List:
    task_string=str(tracker.latest_message.get("text")).split("[")
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

def metricas_tareas(tracker: Tracker) -> dict:
    task_string=str(tracker.latest_message.get("text")).split("[")
    print(task_string)
    task_string2=str(task_string[1]).split("]")
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
        #intent_name=tracker.latest_message['intent'].get('name')
        #task_string=get_list_string(tracker)
        #dispatcher.utter_message(text="Tareas "+str(task_string))
        dict_data=metricas_tareas(tracker)
        dict_tareas={"intent": "working_on_tha_tasks", "data":dict_data}
        dispatcher.utter_message(controlStrategy.process_intent(dict_tareas))
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
        task_string=get_list_string(tracker)
        dispatcher.utter_message(text="El agilebot asistio a las reuniones: "+str(task_string))
        return []

class ActionStartMeeting(Action):

    def name(self) -> Text:
        return "action_start_meeting"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ent_fecha= next(tracker.get_latest_entity_values("fecha"), None)
        ent_hora= next(tracker.get_latest_entity_values("hora"), None)
        dispatcher.utter_message("La fecha es: "+str(ent_fecha)+" y la hora es: "+str(ent_hora))
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
        dispatcher.utter_message("La fecha de inicio es: "+str(fecha_start)+ ", su hora: "+str(hora_start)+".La fecha de finalización es: " + str(ent_fecha)+" y la hora es: "+str(ent_hora))
        fecha_inicio=str(fecha_start)+str(" ")+str(hora_start)
        fecha_fin=str(ent_fecha)+str(" ")+str(ent_hora)
        d_intent={"intent":"ended_meeting","data":{"id":str(ent_idreunion),"fecha_start": str(fecha_inicio),"fecha_ended":str(fecha_fin)}}
        dispatcher.utter_message(controlStrategy.process_intent(d_intent))
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
        dispatcher.utter_message(controlStrategy.process_intent(d_intent))
        return []