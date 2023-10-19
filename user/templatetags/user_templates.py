from django import template
from time import mktime
from datetime import datetime as dt, timezone
from django.utils.translation import gettext


register = template.Library()

def substract_time_notifications(value1, value2):
    delta = mktime( value1.timetuple()) - mktime(value2.timetuple())
    if delta <60:
        delta = str(int(delta)) + gettext(" seconds ago")
    elif 60 <= delta and delta < 3600:
        delta = int(delta/60) + 1
        delta = str(delta) + gettext(" minutes ago")
    elif 3600 <= delta and delta < 86400:
        delta = int(delta/3600) + 1
        delta = gettext("less than ") + str(delta) + gettext(" hours ago")
    elif 86400 < delta :
        delta = value2
    return delta

def substract_time_last_seen(value1, value2):
    delta = mktime( value1.timetuple()) - mktime(value2.timetuple())
    if delta < 60 :
        return None
    else :
        return substract_time_messages(value1, value2)

def substract_time_messages(value1, value2):
    if not value2:
        value2 = dt.now(timezone.utc)
    delta = mktime( value1.timetuple()) - mktime(value2.timetuple())
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

def substarct_time_product_ar(value1, value2):
    delta = int(mktime( value1.timetuple()) - mktime(value2.timetuple()))
    if delta <60:
        delta = f"منذ { delta } ثانية"
    elif 60 <= delta and delta < 3600:
        delta = int(delta/60) + 1
        delta = f"منذ { delta } دقيقة"
    elif 3600 <= delta and delta < 86400:
        delta = int(delta/3600) + 1
        delta = f"منذ { delta } ساعة"
    elif 86400 <= delta and delta < 604800:
        delta = int(delta / 86400)
        delta = f"منذ { delta } أيام"
    elif 604800 <= delta and delta < 31536000:
        delta = int(delta / 604800)
        delta = f"منذ { delta } أسابيع"
    elif 31536000 <= delta :
        delta = int(delta / 31536000)
        delta = f"منذ { delta } سنة"
    return delta

def substarct_time_product(value1, value2):
    delta = int(mktime( value1.timetuple()) - mktime(value2.timetuple()))
    if delta <60:
        delta = gettext("{} seconds ago").format(delta)
    elif 60 <= delta and delta < 3600:
        delta = int(delta/60) + 1
        delta = gettext("{} minutes ago").format(delta)
    elif 3600 <= delta and delta < 86400:
        delta = int(delta/3600) + 1
        delta = gettext("{} hours ago").format(delta)
    elif 86400 <= delta and delta < 604800:
        delta = int(delta / 86400)
        delta = gettext("{} days ago").format(delta)
    elif 604800 <= delta and delta < 31536000:
        delta = int(delta / 604800)
        delta = gettext("{} weeks ago").format(delta)
    elif 31536000 <= delta :
        delta = int(delta / 31536000)
        delta = gettext("{} years ago").format(delta)
    return delta

def order_by(model, parameter):
    return model.order_by(parameter)


@register.filter
def split(string, sep):
    return string.split(sep)

register.filter('substract_time_notifications', substract_time_notifications)
register.filter('substract_time_messages', substract_time_messages)
register.filter('substract_time_last_seen', substract_time_last_seen)
register.filter('substarct_time_product_ar', substarct_time_product_ar)
register.filter('substarct_time_product', substarct_time_product)
register.filter('order_by', order_by)



