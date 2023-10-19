from modeltranslation.translator import translator, TranslationOptions
from .models import State, Notification



class StateTranslationOptions(TranslationOptions):
    fields = {'name',}


class NotificationTranslationOptions(TranslationOptions):
    fields = {'text',}

translator.register(State, StateTranslationOptions)
translator.register(Notification, NotificationTranslationOptions)

