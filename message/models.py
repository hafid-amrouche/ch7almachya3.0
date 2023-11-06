from django.db import models
from ch7almachya.notification_sending_management import send
from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import LastMessage

# Create your models here.


def register_to_last_messages(self):
    sender = self.sender
    reciever = self.reciever
    message = self
    user_last_message =  LastMessage.objects.filter(user=sender, friend=reciever)
    reciever_last_message = LastMessage.objects.filter(user=reciever, friend=sender)
    if user_last_message:
        user_last_message = user_last_message[0]
        user_last_message.message = message
        user_last_message.is_seen = True
        user_last_message.save()
        reciever_last_message = reciever_last_message[0]
        reciever_last_message.message = message
        reciever_last_message.is_seen = False
        reciever_last_message.is_acknowleged = False
        reciever_last_message.save()
    else:
        LastMessage.objects.create(
            user = sender,
            message = message,
            friend = reciever,
            is_seen = True,
        )
        LastMessage.objects.create(
            friend = sender,
            message = message,
            user = reciever,
        )
        
    sender.friendlist.add_friend(reciever)
    reciever.friendlist.add_friend(sender)

def send_push_notification(instance) :
    try:
      icon = instance.sender.profile.picture_150
      first_name = instance.sender.first_name
      if not icon :
        icon =  f'/static/images/letters/{first_name[0]}.jpg'
      send(instance.reciever, first_name, instance.text, f'/messages/{ instance.sender.id }/', icon, type=f'message-{instance.sender.id}', notification_category="message")
    except:
        print('ERROR AT message.models.send_push_notification')
  

class Message(models.Model):
  sender = models.ForeignKey('user.Account', on_delete = models.CASCADE, related_name="sent_messages")
  reciever = models.ForeignKey('user.Account', on_delete = models.SET_NULL, related_name="recivied_messages", blank=True, null=True,)
  text = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True, null=True)
     
  def __str__(self):
      return str(self.sender) + ' | ' + str(self.reciever) + ' | ' + str(self.text)[:20] + " ..."
    

  
@receiver(post_save, sender=Message)
def post_message_save(instance, created, **kwargs):
    if created:
      register_to_last_messages(instance)
      send_push_notification(instance) 