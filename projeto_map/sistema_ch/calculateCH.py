from abc import ABC, abstractmethod

class CalculateCH(ABC):
    @abstractmethod
    def calculateCH(self, atividade) -> int:
        pass

class CalculateWorkshopCH(CalculateCH):
    def calculateCH(self, atividade) -> int:
        return atividade.horas
    
class CalculatePalestraCH(CalculateCH):
    def calculateCH(self, atividade) -> int:
        return atividade.horas 
        
class CalculateCursoCH(CalculateCH):
    def calculateCH(self, atividade) -> int:
        return atividade.horas  