import threading

from actions.procesamiento.artefacto import Artefacto


class ArtefactoDescriptor(Artefacto):
    def __init__(self, nombre, descripcion, fecha_inicio, fecha_cumplimiento,
                 autor, archivo):
        super().__init__(nombre, descripcion, fecha_inicio, fecha_cumplimiento)
        self._autor = autor
        self._archivo = archivo
        self._lock= threading.Lock()

    def set_autor(self, autor):
        with self._lock:
            #loggin.debug("Thread %s has autor lock", name)
            self._autor = autor

    def get_autor(self):
        return self._autor

    def set_archivo(self, archivo):
        with self._lock:
            #loggin.debug("Thread %s has archivo lock", name)
            self._archivo = archivo

    def get_archivo(self):
        return self._archivo
