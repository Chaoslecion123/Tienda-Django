
from django import template

register = template.Library()

@register.filter()
def price_format(value):
    return '${0:.2f}'.format(value)

@register.filter()
def set_day_string(value):
    days = {
        '1' : 'Lunes',
        '2' : 'Martes',
        '3' : 'Miercoles',
        '4' : 'Jueves',
        '5' : 'Viernes',
        '6' : 'Sabado',
        '7' : 'Domingo',
    }

    for indice,day in days.items():
        if int(indice) == value:
            print('*** *** ***')
            print(value)
            print('*** *** ***')
            return '{}'.format(day)
