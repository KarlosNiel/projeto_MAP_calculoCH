from .calculate_ch import CalculateWorkshopCH, CalculatePalestraCH, CalculateCursoCH

STRATEGIES = {
    'WORKSHOP': CalculateWorkshopCH(),
    'PALESTRA': CalculatePalestraCH(),
    'CURSO': CalculateCursoCH(),
}

def get_strategy(submission):
    return STRATEGIES.get(submission.type)
