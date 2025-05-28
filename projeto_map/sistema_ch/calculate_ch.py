from .models import ActivitySubmission
from abc import ABC, abstractmethod

class CalculateCH(ABC):
    @abstractmethod
    def calculate_ch(self, submission: ActivitySubmission) -> int:
        pass

class CalculateWorkshopCH(CalculateCH):
    def calculate_ch(self, submission):
        return submission.hours

class CalculatePalestraCH(CalculateCH):
    def calculate_ch(self, submission):
        return submission.hours

class CalculateCursoCH(CalculateCH):
    def calculate_ch(self, submission):
        return submission.hours
