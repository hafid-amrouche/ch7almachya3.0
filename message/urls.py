from django.urls import path
from . import views

urlpatterns = [
    path("", views.messages_list, name="messages-list" ),
    path("ajax-messages-list", views.ajax_messages_list, name="ajax-messages-list" ),
    path("<int:reciever_id>/", views.messages_box, name="messages-box" ),
    path("<int:reciever_id>/save", views.ajax_save_message, name="ajax-save" ),
    path("<int:reciever_id>/load", views.ajax_load_messages, name="ajax-load" )
]
