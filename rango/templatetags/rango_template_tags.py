from django import template
from rango.models import Category

register = template.Library()

@register.inclusion_tag('rango/cats.html')
def get_category_list(cat=None):
    return {'cats': Category.objects.all(),
        'act_cat': cat}

@register.inclusion_tag('rango/album-list2.html')
def get_album_list(album=None):
    return {'albums': Category.objects.all(),
        'act_alb': album}