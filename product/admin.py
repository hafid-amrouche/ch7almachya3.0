from django.contrib import admin
from .models import Product, Image, Detail, ParentCategory, Category, Like, Dislike, Comment, Option, Fuel, GearBox, Color, Document
from modeltranslation.admin import TranslationAdmin


# Register your models here.

class CategoryAdmin(TranslationAdmin):
  model = Category
  list_display = ["name", "parent",]
  list_filter = ["parent"]
  prepopulated_fields = {"slug" : ["name",]}

class OptionAdmin(TranslationAdmin):
  model = Option

class FuelAdmin(TranslationAdmin):
  model = Fuel

class GearBoxAdmin(TranslationAdmin):
  model = GearBox


class ParentCategoryAdmin(TranslationAdmin):
  model = ParentCategory
  list_display = ["name"]
  prepopulated_fields = {"slug" : ["name",]}


admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Detail)
admin.site.register(Like)
admin.site.register(Dislike)
admin.site.register(Comment)
admin.site.register(Color)
admin.site.register(Document)
admin.site.register(ParentCategory, ParentCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Fuel, FuelAdmin)
admin.site.register(GearBox, GearBoxAdmin)
