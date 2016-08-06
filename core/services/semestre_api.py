from constance import config as live_config

from core import models as core_models

def get_current_semester():
    return core_models.Semestre.objects.get(id=live_config.SEMESTER)
