from actions.procesamiento import factor_strategies


class ControlStrategy:
    """
        Controlador del proceso:
        Se suscribe a los eventos correspondientes
        Procesa los eventos disparados mediante metricas/estrategias y publica nuevos eventos
    """

    def __init__(self):
        self._d_intentStrateg = self.get_intent_strategies()

    def get_intent_strategies(self) -> dict:
        return {
            "ended_meeting": {
                "strategies": {
                    "EstimatedDeadline": {
                        "Constructor": factor_strategies.EstimatedDeadline()
                    }
                }
            },
            "working_on_tha_tasks": {
                "strategies": {
                    "ControlTask": {
                        "Constructor": factor_strategies.ControlTask()
                    }
                }
            },
            "participations": {
                "strategies": {
                    "MeetingParticipations": {
                        "Constructor": factor_strategies.MeetingParticipations()
                    }
                }
            }
        }


    def process_result(self,strategy, value)-> str: 
        result=""
        if strategy.get_name() == "EstimatedDeadline":
            valor=int(value)
            if valor < 0:
                valor=valor*(-1)
                result="La reunion finalizo "+str(valor)+" segundos antes del plazo."
            else:
                result="La reunion finalizo "+str(valor)+" segundos después del plazo."
        else:
            if (strategy.get_name() == "ControlTask") or (strategy.get_name() == "MeetingParticipations"):
                result=str(value)
        return result

    def execute_strategies(self, intent_name: str, data: dict) -> str:
        result = ""
        if intent_name in self._d_intentStrateg:
            strategies = self._d_intentStrateg[intent_name]["strategies"]
            for key_strategy, data_strategy in strategies.items():
                result = result + "Métrica calculada: " + str(key_strategy) + " "
                strategy = data_strategy["Constructor"]
                strategy.process_event(data)
                result = result + " Result: " + self.process_result(strategy,strategy.calculate_value())
                #Result: The function has the metric calculation in the form of a String
        return result

    def process_intent(self, kwargs:dict) -> str:
        intent_name = ""
        data = ""
        result = ""
        if "intent" in kwargs:
            intent_name = kwargs["intent"]
            if "data" in kwargs:
                data = kwargs["data"]
                result = self.execute_strategies(str(intent_name), data)
            else:
                result = "No se encuentra key data"
        else:
            result = "No se encuentra key intent"
        return result
