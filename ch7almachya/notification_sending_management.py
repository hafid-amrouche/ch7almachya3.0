
import json
from pyfcm import FCMNotification
from funtions import user_is_active


FCM_API_KEY = "AAAA1kBgl_Q:APA91bHszWCi9ItE_y-F9ngHJAr3q70cCoxVowQgs8rmDeH5pXoYP6FN_XYNezI3mjxt790NchStphjZaV95FSuTG3pIgXp_RRzVYppoBpoOCkYo_kUG1g5_Hu_iZTVB0uonqqrAwzFh"

def NMCount(user):
    try:
        NMCount = [user.notified_notifications.filter(is_acknowleged=False).count(), user.last_messages.filter(is_acknowleged=False).count()]
        return NMCount

    except:
        print('ERROR AT NMCount')
        return ["", ""]

def NCount(user):
    try:
        NCount = [user.notified_notifications.filter(is_acknowleged=False).count(),-1]
        return NCount

    except:
        print('ERROR AT NMCount')
        return ["", ""]
    

def MCount(user):
    try:
        MCount = [-1, user.last_messages.filter(is_acknowleged=False).count()]
        return MCount

    except:
        print('ERROR AT NMCount')
        return ["", ""]

def send_notification(user, resgistration_token, title, body, link, icon, type, notification_category):
    if user_is_active(user, 300):
        if notification_category == 'notification':
            data = NCount(user)
        elif notification_category == 'message':
            data = MCount(user)
    else :
        data = [-1, -1]

    push_service = FCMNotification(api_key=FCM_API_KEY)
    data_message = {
        "FCM_type" : "Notification",
        "link": link,
        "type" : type,
        "NMCount": data,
    }

    push_service.notify_single_device(
        registration_id=resgistration_token,
        message_title=title,
        message_body=body,
        message_icon= icon,
        data_message=data_message,
    )

  
def send(user, title="", body="", link="", icon="", type="", notification_category=""):
    for token in json.loads(user.notifications_token.tokens_list):
        send_notification(user, token, title, body, link, icon, type, notification_category)
