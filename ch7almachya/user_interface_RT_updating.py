
import json
from pyfcm import FCMNotification


FCM_API_KEY = "AAAA1kBgl_Q:APA91bHszWCi9ItE_y-F9ngHJAr3q70cCoxVowQgs8rmDeH5pXoYP6FN_XYNezI3mjxt790NchStphjZaV95FSuTG3pIgXp_RRzVYppoBpoOCkYo_kUG1g5_Hu_iZTVB0uonqqrAwzFh"


def send_notification(data, resgistration_token):
    push_service = FCMNotification(api_key=FCM_API_KEY)
    data_message = {
        "FCM_type" : "NMCount",
        "NMCount": data,
    }

    push_service.notify_single_device(
        registration_id=resgistration_token,
        data_message=data_message,
    )

  
def update_NMCount(user):
    for token in json.loads(user.notifications_token.tokens_list):
        try:
            NMCount = [user.notified_notifications.filter(is_acknowleged=False).count(), user.last_messages.filter(is_acknowleged=False).count()]
            send_notification(NMCount, token)

        except:
            print('ERROR AT NMCount')
            return ["", ""]

def update_NCount(user):
    for token in json.loads(user.notifications_token.tokens_list):
        NCount = [user.notified_notifications.filter(is_acknowleged=False).count(), -1]
        send_notification(NCount, token)

def update_MCount(user):
    for token in json.loads(user.notifications_token.tokens_list):
        MCount = [-1, user.last_messages.filter(is_acknowleged=False).count()]
        send_notification(MCount, token)
