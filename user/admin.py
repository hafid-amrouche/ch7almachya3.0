from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, FriendList, State, Profile, Notification, LastMessage, FollowersList, SearchParameters, MessageToAdmin, ContactUS, SearchWords, SavedItem
from modeltranslation.admin import TranslationAdmin

# Register your models here.

class AccountAdmin(UserAdmin):
  list_display = ("email", "first_name", "last_name", "last_login", "date_joined", "is_active")
  list_display_links = ("email", "first_name", "last_name")
  readonly_fields=["last_login", "date_joined"]
  ordering =('-date_joined',)

  # these 3 parameters must be set and it will make password hideen
  filter_horizontal = ()
  list_filter = ()
  fieldsets = ()

class StateAdmin(TranslationAdmin):
  model = State

class NotificationAdmin(TranslationAdmin):
  model = Notification
  list_display = ["notifier", "type", "user", "is_seen"]
  list_filter = ["notifier", "notified"]

admin.site.register(Account, AccountAdmin)
admin.site.register(Profile)
admin.site.register(FriendList)
admin.site.register(FollowersList)
admin.site.register(LastMessage)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(SearchParameters)
admin.site.register(MessageToAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(ContactUS)
admin.site.register(SearchWords)
admin.site.register(SavedItem)
