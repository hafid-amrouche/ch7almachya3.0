from django.db import models
from ch7almachya.notification_sending_management import send

# Create your models here.

class Message(models.Model):
  sender = models.ForeignKey('user.Account', on_delete = models.CASCADE, related_name="sent_messages")
  reciever = models.ForeignKey('user.Account', on_delete = models.SET_NULL, related_name="recivied_messages", blank=True, null=True,)
  text = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True, null=True)
  def save(self, *args, **kwargs):
      try:
        icon = self.sender.profile.picture_150
        first_name = self.sender.first_name
        if not icon :
          icon =  f'/static/images/letters/{first_name[0]}.jpg'
        send(self.reciever, first_name, self.text, f'/messages/{ self.sender.id }/', icon, type=self.sender.id)
      except:
         pass
      print()
      super(Message, self).save(*args, **kwargs)

  def __str__(self):
      return str(self.sender) + ' | ' + str(self.reciever) + ' | ' + str(self.text)[:20] + " ..."
    

  