from datetime import date
import threading
import logging


class Artefacto:
    cantidad_artefactos = 0  # Variable de clase o estatica

    def __init__(self, nombre, descripcion, fecha_inicio, fecha_cumplimiento):
        Artefacto.cantidad_artefactos += 1

        self._id = Artefacto.cantidad_artefactos
        self._nombre = nombre
        self._descripcion = descripcion
        self._fecha_creacion = date.today()
        self._fecha_inicio = fecha_inicio
        self._fecha_cumplimiento = fecha_cumplimiento
        # Cuando finaliza se setea con la fecha del dia que finalizo
        self._fecha_fin = None
        self.actores =list()
        self._lock=threading.Lock()

    def is_finalizado(self):
        return False if self._fecha_fin is None else False

    def finalizar(self):
        with self._lock:
            self._fecha_fin = date.today()

    def get_dependencias(self):
        """Por defecto un artefacto no tiene ninguna dependencia.
        """
        return []

    def get_id(self):
        return self._id

    def get_descripcion(self):
        return self._descripcion

    def set_descripcion(self, descripcion):
        with self._lock:
            self._descripcion = descripcion

    def get_fecha_creacion(self):
        return self._fecha_creacion

    def get_fecha_inicio(self):
        return self._fecha_inicio

    def set_fecha_inicio(self, fecha_inicio):
        with self._lock:
            self._fecha_inicio = fecha_inicio

    def get_fecha_fin(self):
        return self._fecha_fin

    def getActores(self):
        return self.actores

    def get_fecha_cumplimiento(self):
        return self._fecha_cumplimiento

    def set_fecha_cumplimiento(self, fecha_cumplimiento):
        with self._lock:
            self._fecha_cumplimiento = fecha_cumplimiento

    def get_nombre(self):
        return self._nombre

    def set_nombre(self, nombre):
        with self._lock:    
            self._nombre = nombre

    def add_actor(self, id):
        with self._lock:
            self.actores.append(id)
    
    def contains_actor(self, id):
        return self.actores.__contains__(id)
