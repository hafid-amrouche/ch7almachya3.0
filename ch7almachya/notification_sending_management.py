
import json
from pyfcm import FCMNotification


FCM_API_KEY = "AAAA1kBgl_Q:APA91bHszWCi9ItE_y-F9ngHJAr3q70cCoxVowQgs8rmDeH5pXoYP6FN_XYNezI3mjxt790NchStphjZaV95FSuTG3pIgXp_RRzVYppoBpoOCkYo_kUG1g5_Hu_iZTVB0uonqqrAwzFh"

def NMCount(user):
    try:
        return [user.notified_notifications.filter(is_acknowleged=False).count(), user.last_messages.filter(is_acknowleged=False).count()]

    except:
        return ["", ""]

def send_notification(user, resgistration_token, title, body, link, icon, type):
    push_service = FCMNotification(api_key=FCM_API_KEY)

    data_message = {
        "FCM_type" : "Notification",
        "link": link,
        "type" : type,
        "NMCount": NMCount(user),
    }

    push_service.notify_single_device(
        registration_id=resgistration_token,
        message_title=title,
        message_body=body,
        message_icon= icon,
        data_message=data_message,
    )

  
def send(user, title="", body="", link="", icon="", type=""):
    for token in json.loads(user.notifications_token.tokens_list):
        send_notification(user, token, title, body, link, icon, type)
