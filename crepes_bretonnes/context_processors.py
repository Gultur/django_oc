from django import template
register = template.Library()

from datetime import datetime



def get_infos(request):
    date_actuelle = datetime.now()
    return {'date_actuelle': date_actuelle}
