import django_filters
from .models import Queja,EntidadAfectada,Modalidad,Procedencia,Clasificacion,CasoPrensa,Via

class QuejaFilter(django_filters.FilterSet):

    entidadAfectada = django_filters.ModelChoiceFilter(queryset=EntidadAfectada.objects.all())
    modalidad = django_filters.ModelChoiceFilter(queryset=Modalidad.objects.all())
    via = django_filters.ModelChoiceFilter(queryset=Via.objects.all())
    procedencia = django_filters.ModelChoiceFilter(queryset=Procedencia.objects.all())
    clasificacion = django_filters.ModelChoiceFilter(queryset=Clasificacion.objects.all())
    casoPrensa = django_filters.ModelChoiceFilter(queryset=CasoPrensa.objects.all())


    class Meta:
        model = Queja
        fields = ['entidadAfectada', 'modalidad', 'via', 'procedencia', 'clasificacion', 'casoPrensa']