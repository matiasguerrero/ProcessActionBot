import abc
import datetime
from typing import Dict, Any

from actions.procesamiento.tarea import Tarea
from actions.procesamiento.fase import Fase


class CalculationStrategy(metaclass=abc.ABCMeta):
    """Interfaz que define el comportamiento basico requerido por una estrategia
    usada en el calculo de metricas.

    Autor: Matias G.
    """

    @abc.abstractmethod
    def process_event(self, event: Dict) -> None:
        """Procesa el evento.

        Autor: Bruno.

        :param event: evento a procesar.
        :return: None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def calculate_value(self) -> Any:
        """Calcula el valor de la estrategia.

        Autor: Bruno.

        :return: Any.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_name(self) -> str:
        """Calcula el valor de la estrategia.

        Autor: Matias G.

        :return: Any.
        """
        raise NotImplementedError


class MeetingParticipations(CalculationStrategy):
    """Cuenta las participaciones de todos los TeamMembers/AgileBots que forman
    parte de un proyecto en AgileTalk.

    Autor: Matias G.
    """

    def __init__(self):  # Componente.getReuniones()
        """Constructor.
        Args:
        """
        self._n_occurrences = 0
        self._d_ocurrences = {}
        self.result=""

    def __str__(self) -> str:
        return "(MeetingParticipations: {})".format(self._n_occurrences)
    
    def get_name(self) -> str:
        return "MeetingParticipations"

    def process_event(self, event: Dict) -> None:
        """A partir de un evento cuenta las participaciones generales por
        persona.

        Autor: Matias G.

        :param event: evento a procesar. El formato del evento es:
                      {'Participations': [{'1': {'cant_particip': '3'}},
                       {'2': {'cant_particip': '2'}}, {'3': {'cant_particip': '3'}}]}
        :return: None.
        """
        self.result=""
        participations = event["Participations"]
        for x in participations:
            for key, value in x.items():
                self.result=self.result+"El miembro del equipo "+str(key)+" participó "+str(value["cant_particip"])+" veces en la reunión. "

    def calculate_value(self) -> str:
        """Devuelve todas las participaciones en reuniones dentro de un
        proyecto.

        Autor: Matias G.

        :return: Str.
        """
        return self.result


class MeetAsistance(CalculationStrategy):
    """Calcula el porcentaje de asistencia a una reunion.

    Autor: Matias G.
    """
    def __init__(self):  # Componente.getReuniones()
        self._n_asistance = 0

    def __str__(self) -> str:
        return "(MeetAsistance: {})".format(self._n_asistance)

    def get_name(self) -> str:
        return "MeetAsistance"

    def process_event(self, event: Dict) -> None:
        """Establece el porcentaje de TeamMembers/AgileBots que participaron en
        la reunion.

        Autor: Matias G.

        :param event: evento a procesar. El formato del evento es:
                      {"event_id": "", "time": "", "id_reunion": "",
                       "participaciones": {"bruno": 5, "matias": 7}}
        :return: None.
        """
        # TODO Se requiere que todos los TeamMembers/AgileBots que tengan que
        #  participar en la reunion aparezcan en event["participaciones"],
        #  aunque sea con un valor de cero participaciones.
        reunion = event["participaciones"]
        total_asistance = 0
        for meet_user, ocurrence in reunion.items():
            if ocurrence > 0:
                total_asistance += 1
        cant = len(reunion)
        if cant > 0:
            self._n_asistance = total_asistance / cant

    def calculate_value(self) -> float:
        """Devuelve el porcentaje de asistencia a la reunion.

        Autor: Matias G.

        :return: Dict.
        """
        return self._n_asistance


class EstimatedDeadline(CalculationStrategy):
    """Calcula el porcentaje de asistencia a una reunion.

    Autor: Matias G.
    """
    def __init__(self):  # Componente getFase
        """Constructor.
        Args:
        """
        # La fase self.meet debería ser provista por un componente que brinde
        # el artefacto
        self.fecha_init= datetime.datetime.utcnow()
        self.fecha_fin= datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        self._fase = Fase(1, self.fecha_init.strftime("%Y-%m-%d %H:%M:%S"), self.fecha_fin.strftime("%Y-%m-%d %H:%M:%S"))
        self._fase.add_actor("actor1")
        self._fase.add_actor("actor1")
        self._fase.add_actor("actor1")

        self._estimated_time = datetime.date.today()
        self._real_time = datetime.date.today()

    def __str__(self) -> str:
        return " "

    def get_name(self) -> str:
        return "EstimatedDeadline"

    def process_event(self, event: dict) -> None:
        """Compara el plazo de finalización estimado de una fase con su
        finalizacion real.

        Autor: Matias G.

        :param event: evento "FinFase" a procesar.
        :return: None.
        """
        d={"id":1,"fecha_start":"fecha","fecha_ended":"fecha"}

        date_format = "%Y-%m-%d %H:%M:%S"

        self._fase.set_id(event["id"])
        self._fase.finalizar()
        #real_end_date=self._fase.get_fecha_fin()

        end_date = datetime.datetime.strptime(
            str(self._fase.get_duracion_estimada()), date_format)
        start_date = datetime.datetime.strptime(
            str(self._fase.get_fecha_inicio()), date_format)

        real_end_date=datetime.datetime.strptime(
            str(event["fecha_ended"]), date_format)
        real_start_date=datetime.datetime.strptime(
            str(event["fecha_start"]), date_format)

        self._estimated_time = end_date - start_date
        self._real_time = real_end_date - real_start_date

    def calculate_value(self) -> int:
        """Retorna la cantidad de segundos existentes entre el plazo estimado
        y el plazo real de finalizacion.

        Si la cantidad es negativa -> realTime < estimatedTime
        Si la cantidad es positiva -> realTime > estimatedTime

        Autor: Matias G.

        :return: int.
        """
        self._real_time = self._real_time.total_seconds()
        self._estimated_time = self._estimated_time.total_seconds()
        difference_sec = self._real_time - self._estimated_time
        return difference_sec


class ControlTask(CalculationStrategy):
    """Calcula el porcentaje de asistencia a una reunion.

    Autor: Matias G.
    """
    def __init__(self):  # Componente.getReuniones()
        self._n_asistance = 0
        self.tareas=[]
        self.result={}
        self.valor=""
        self.horashechas=0

    def __str__(self) -> str:
        return "(ControlTask: {})".format(self._n_asistance)

    def get_name(self) -> str:
        return "ControlTask"

    def process_event(self, event: dict) -> None:
        #d={"tareas":[{"id": 1, "horas":5},{"id":2, "horas":5}]}
        print(event)
        self.valor=""
        self.horashechas=0
        list_tareas=event["Tareas"]
        for x in list_tareas:
            for key, value in x.items():
                horas=int(value["horas_totales"]) - int(value["horas_trabajadas"])
                self.valor=self.valor+"La tarea "+ str(key)+ " necesita "+str(horas)+" hora/s más para ser finalizada. "
                #t = Tarea(x["id"],"desc",datetime.datetime.today(),datetime.datetime.today(),"agile","asd","in progress",10)
                #self.tareas.append(t)
                #self.result["id"]=t.get_puntos_restantes(x["horas"])
                self.horashechas=self.horashechas+int(value["horas_trabajadas"])
   
    def calculate_value(self) -> str:
        resultado=self.valor+" El miembro del equipo trabajó "+str(self.horashechas)+" horas diarias."
        #for x in range(0,len(self.tareas)):
        return resultado