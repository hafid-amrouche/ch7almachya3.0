from django import template

register = template.Library()

def sort_by(model, field):
    return model.order_by(field)

register.filter('sort_by', sort_by)