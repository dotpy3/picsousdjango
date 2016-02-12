from django import template

register = template.Library()

@register.filter(name='period')
def period(period_char):
    if period_char == 'S':
        return 'Soir'
    if period_char == 'D':
        return 'Midi'
    if period_char == 'M':
        return 'Matin'
    return None
