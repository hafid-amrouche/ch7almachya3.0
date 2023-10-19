from modeltranslation.translator import translator, TranslationOptions
from .models import Category, ParentCategory, Option, Fuel, GearBox, Color, Document



class CategoryTranslationOptions(TranslationOptions):
    fields = {'name',}

class ParentTranslationOptions(TranslationOptions):
    fields = {'name',}

class OptionTranslationOptions(TranslationOptions):
    fields = {'name',}

class FuelTranslationOptions(TranslationOptions):
    fields = {'name',}

class GearBoxTranslationOptions(TranslationOptions):
    fields = {'name',}

class ColorTranslationOptions(TranslationOptions):
    fields = {'name'}

class DocumentTranslationOptions(TranslationOptions):
    fields = {'name', }

translator.register(Category, CategoryTranslationOptions)
translator.register(ParentCategory, ParentTranslationOptions)
translator.register(Option, OptionTranslationOptions)
translator.register(Fuel, FuelTranslationOptions)
translator.register(GearBox, GearBoxTranslationOptions)
translator.register(Color, ColorTranslationOptions)
translator.register(Document, DocumentTranslationOptions)


