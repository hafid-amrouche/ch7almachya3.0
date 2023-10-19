from django.db import models

# Create your models here.

class Message(models.Model):
  sender = models.ForeignKey('user.Account', on_delete = models.CASCADE, related_name="sent_messages")
  reciever = models.ForeignKey('user.Account', on_delete = models.SET_NULL, related_name="recivied_messages", blank=True, null=True,)
  text = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True, null=True)


  def __str__(self):
      return str(self.sender) + ' | ' + str(self.reciever) + ' | ' + str(self.text)[:20] + " ..."
    

  