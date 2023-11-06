
from time import mktime
from datetime import datetime as dt, timezone
from django.utils.translation import gettext

def last_active(request):
    if request.user.is_authenticated:
        request.user.profile.last_active = dt.now(timezone.utc)
        request.user.profile.save()

def user_is_active(user, delta_max):
        delta = dt.now(timezone.utc) - user.profile.last_active 
        return delta.total_seconds() < delta_max 


def get_ip_address(request):
    return request.session.session_key

def substract_time_messages(value1, value2):
    if not value2:
        value2 = dt.now(timezone.utc)
    delta = value1 - value2
    delta = delta.total_seconds()
    print(delta)
    if delta <60:
        delta = str(int(delta)) + gettext(" s")
    elif 60 <= delta and delta < 3600:
        delta = int(delta/60) + 1
        delta = str(int(delta)) + gettext(" m")
    elif 3600 <= delta and delta < 86400:
        delta = int(delta/3600)
        delta = f"{int(delta)}" + gettext("h")
    elif 86400 <= delta and delta < 604800:
        delta = delta / 86400
        delta = f"{int(delta)}"+ gettext(" d")
    elif 604800 <= delta and delta < 31536000:
        delta = delta / 604800
        delta = f"{int(delta)}" + gettext(" w")
    elif 31536000 <= delta :
        delta = delta / 31536000
        delta = f"{int(delta)}" + gettext(" y")  
    return delta

def sub_time(request, cd):
    ct = dt.now(timezone.utc)
    delta = ct - cd
    delta = delta.total_seconds()
    
    if request.LANGUAGE_CODE == 'en':
        if delta <60:
            delta = 'Just now'

        elif 60 <= delta and delta < 3600:
            delta = int(delta/60) + 1
            delta = str(int(delta)) + ' minutes ago'

        elif 3600 <= delta and delta < 86400:
            delta = int(delta/3600)
            delta = str(int(delta)) + ' hours ago'

        elif 86400 <= delta and delta < 604800:
            delta = delta / 86400
            delta = str(int(delta)) + ' days ago'

        elif 604800 <= delta and delta < 31536000:
            delta = delta / 604800
            delta = str(int(delta)) + ' weeks ago'

        elif 31536000 <= delta :
            delta = delta / 31536000
            delta = str(int(delta)) + ' years ago' 

        return delta
    
    elif request.LANGUAGE_CODE == 'fr':
        if delta <60:
            delta = 'Juste maintenant'

        elif 60 <= delta and delta < 3600:
            delta = int(delta/60) + 1
            delta = "Il y a " + str(int(delta)) + ' minutes'

        elif 3600 <= delta and delta < 86400:
            delta = int(delta/3600)
            delta = "Il y a " + str(int(delta)) + ' heures'

        elif 86400 <= delta and delta < 604800:
            delta = delta / 86400
            delta = "Il y a " + str(int(delta)) + ' jours'

        elif 604800 <= delta and delta < 31536000:
            delta = delta / 604800
            delta = "Il y a " + str(int(delta)) + ' semaines'

        elif 31536000 <= delta :
            delta = delta / 31536000
            delta = "Il y a " + str(int(delta)) + ' années' 

        return delta
    
    else:
        if delta < 60:
            delta = 'منذ لحظات'

        elif 60 <= delta and delta < 3600:
            delta = int(delta/60) + 1
            delta = "منذ " + str(int(delta)) + ' دقيقة'

        elif 3600 <= delta and delta < 86400:
            delta = int(delta/3600)
            delta = "Il y a " + str(int(delta)) + ' ساعات'

        elif 86400 <= delta and delta < 604800:
            delta = delta / 86400
            delta = "منذ " + str(int(delta)) + ' أيام'

        elif 604800 <= delta and delta < 31536000:
            delta = delta / 604800
            delta = "منذ " + str(int(delta)) + ' أسابيع'

        elif 31536000 <= delta :
            delta = delta / 31536000
            delta = "منذ " + str(int(delta)) + ' سنوات' 

        return delta