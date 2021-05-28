from actions.procesamiento.artefacto_descriptor import ArtefactoDescriptor


class Tarea(ArtefactoDescriptor):
    def __init__(self, nombre, descripcion, fecha_inicio, fecha_cumplimiento,
                 autor, archivo, estado_actual,puntos_asignados):
        super().__init__(nombre, descripcion, fecha_inicio, fecha_cumplimiento,
                         autor, archivo)
        self._estado_actual = estado_actual
        self._cambios_estado = [estado_actual]
        self.puntosasignados=puntos_asignados
        self.puntosrestantes=self.puntosasignados
        #self._lock=threading.Lock()

    def __repr__(self):
        return "tarea "+str(self.get_id())

    def get_cambios_estado(self):
        return self._cambios_estado

    def cambiar_estado(self, nuevo_estado,name):
        with self._lock:
         #   logging.debug("Thread %s  has CAMBIAR ESTADO lock",name)
            self._estado_actual = nuevo_estado
            self._cambios_estado.append(nuevo_estado)
    def get_puntos_restantes(self, horas)-> int:
        self.puntosrestantes=self.puntosrestantes - (horas / 2)
        return self.puntosrestantes
    def get_estado_actual(self):
       # logging.debug(self._estado_actual)
        return self._estado_actual
""" 
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.DEBUG,datefmt="%H:%M:%S")
tarea= Tarea("tarea1", "una tarea", None, None, "sofia", None, "to-do")
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    for i in range(10):
        if i%2==0:
            executor.map(tarea.cambiar_estado("done",i), range(3))
        else:
            executor.map(tarea.cambiar_estado("in progress",i), range(3))
        executor.map(tarea.get_estado_actual(),range(3))
logging.debug(tarea.get_cambios_estado()) """