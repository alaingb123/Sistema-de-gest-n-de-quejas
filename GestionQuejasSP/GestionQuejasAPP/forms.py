from django.forms import ModelForm,forms,DateTimeInput
from datetime import datetime

from django import forms
from multiupload.fields import MultiFileField

from .models import Queja, Respuesta, EntidadAfectada, CasoPrensa, Conclusion, Clasificacion, Satisfaccion, Procedencia, \
    Via, Modalidad, DocumentoQF, AnalisisQueja


class QuejaForm(forms.ModelForm):
    entidadAfectada = forms.ModelChoiceField(queryset=EntidadAfectada.objects.all())
    casoPrensa = forms.ModelChoiceField(queryset=CasoPrensa.objects.all())
    modalidad = forms.ModelChoiceField(queryset=Modalidad.objects.all())
    via = forms.ModelChoiceField(queryset=Via.objects.all())
    procedencia = forms.ModelChoiceField(queryset=Procedencia.objects.all())
    clasificacion = forms.ModelChoiceField(queryset=Clasificacion.objects.all())

    class Meta:
        model = Queja
        fields = ['nombre_apellidos', 'entidadAfectada', 'modalidad', 'via', 'procedencia', 'clasificacion',
                  'casoPrensa', 'fechaR', 'argumento','asunto','telefono','direccion','queja_u']



class RespuestaForm(forms.ModelForm):
    satisfaccion = forms.ModelChoiceField(queryset=Satisfaccion.objects.all(),required=False)
    conclusion = forms.ModelChoiceField(queryset=Conclusion.objects.all())

    class Meta:
        model = Respuesta
        fields = ['numero', 'responsable', 'descripcion', 'entrega', 'satisfaccion', 'conclusion', 'fechaE']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['numero'].queryset = Queja.objects.all()
        self.fields['numero'].label = 'Selecciona una queja'
        self.fields['numero'].empty_label = None
        self.fields['fechaE'].required = False




class FiltroQuejasForm(forms.Form):
    years = forms.ChoiceField(choices=[], label='Año')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        anos = Queja.objects.dates('fechaR', 'year').distinct()
        choices = [(ano.year, str(ano.year)) for ano in anos]
        self.fields['years'].choices = choices


class ReporteQuejasForm(forms.Form):
    MONTH_CHOICES = [
        (1, 'Enero'),
        (2, 'Febrero'),
        (3, 'Marzo'),
        (4, 'Abril'),
        (5, 'Mayo'),
        (6, 'Junio'),
        (7, 'Julio'),
        (8, 'Agosto'),
        (9, 'Septiembre'),
        (10, 'Octubre'),
        (11, 'Noviembre'),
        (12, 'Diciembre'),
    ]
    years = forms.ChoiceField(choices=[], label='Año')
    month = forms.ChoiceField(choices=MONTH_CHOICES, label='Mes')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        anos = Queja.objects.dates('fechaR', 'year').distinct()
        choices = [(ano.year, str(ano.year)) for ano in anos]
        self.fields['years'].choices = choices



class ModificarRespuestaForm(forms.ModelForm):
    satisfaccion = forms.ModelChoiceField(queryset=Satisfaccion.objects.all(),required=False)
    conclusion = forms.ModelChoiceField(queryset=Conclusion.objects.all())

    class Meta:
        model = Respuesta
        fields = ['responsable', 'descripcion', 'entrega', 'satisfaccion', 'conclusion', 'fechaE']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fechaE'].required = False


class FormMeses(forms.Form):
    MESES_CHOICES = (
         ('', 'Elige'),
        ('01', 'Enero'),
        ('02', 'Febrero'),
        ('03', 'Marzo'),
        ('04', 'Abril'),
        ('05', 'Mayo'),
        ('06', 'Junio'),
        ('07', 'Julio'),
        ('08', 'Agosto'),
        ('09', 'Septiembre'),
        ('10', 'Octubre'),
        ('11', 'Noviembre'),
        ('12', 'Diciembre'),
    )
    DIAS_CHOICES = (
        ('', 'Todos los días'),
        ('01', '1'),
        ('02', '2'),
        ('03', '3'),
        ('04', '4'),
        ('05', '5'),
        ('06', '6'),
        ('07', '7'),
        ('08', '8'),
        ('09', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('16', '16'),
        ('17', '17'),
        ('18', '18'),
        ('19', '19'),
        ('20', '20'),
        ('21', '21'),
        ('22', '22'),
        ('23', '23'),
        ('24', '24'),
        ('25', '25'),
        ('26', '26'),
        ('27', '27'),
        ('28', '28'),
        ('29', '29'),
        ('30', '30'),
        ('31', '31'),
    )

    dias = forms.ChoiceField(choices=DIAS_CHOICES, required=False)
    mes = forms.ChoiceField(choices=MESES_CHOICES,required=False)


class AnalisisQuejaForm(forms.ModelForm):
    class Meta:
        model = AnalisisQueja
        fields = ['analisis']

        widgets = {
            'analisis': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'cols': 80})
        }
