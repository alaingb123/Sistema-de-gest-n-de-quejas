from django import template

register = template.Library()


@register.filter(name='eliminar_queja')
def eliminar_queja(user):
    if user.groups.filter(name__in=['Funcionario', 'ViceDirectora']):
        return True
    return False