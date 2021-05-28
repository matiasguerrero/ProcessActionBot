from datetime import datetime
import threading

class Fase:
    # TODO Bruno: revisar concepto de fases.
    def __init__(self, id_fase, inicio, duracion_estimada):
        self._id = id_fase
        self._fecha_inicio = inicio
        self._fecha_fin = None
        self._actores = {}
        self._artefactos = {}
        self._duracion_estimada = duracion_estimada
        self._lock=threading.Lock()
    
    def add_actor(self, actor):
        with self._lock:
            self._actores[actor] = actor

    def add_artefacto(self, artefacto):
        with self._lock:
            self._artefactos[artefacto.get_id()] = artefacto

    def delete_actor(self, actor):
        with self._lock:
            self._actores.pop(actor)

    def delete_artefacto(self, artefacto):
        with self._lock:
            self._artefactos.pop(artefacto.get_id())

    def set_fecha_inicio(self, fecha_inicio):
        with self._lock:
            self._fecha_inicio = fecha_inicio

    def finalizar(self):
        with self._lock: 
            self._fecha_fin = datetime.today()

    def cumplio_duracion_estimada(self):
        if self._fecha_fin is None:
            return False

        # TODO Las fechas tienen que estar en formato datetime para que la
        #  comparacion se pueda hacer.
        return self._duracion_estimada >= self._fecha_fin - self._fecha_inicio

    def get_id(self):
        return self._id

    def get_fecha_fin(self):
        return self._fecha_fin
    
    def get_fecha_inicio(self):
        return self._fecha_inicio

    def get_duracion_estimada(self):
        return self._duracion_estimada

    def get_actores(self):
        return self._actores
    
    def get_artefactos(self):
        return self._artefactos

    def set_id(self, id_fase):
        with self._lock:
            self._id = id_fase

    def contains_actor(self,id):
        return self._actores.keys.__contains__(id)