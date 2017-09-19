from django import forms
from django.template.defaultfilters import default

class Producto(forms.Form):
    #cada atributo corresponde con el atributo name en el html
    precio = forms.CharField(label='precio', max_length=100)
    nombre = forms.CharField(label='nombre', max_length=100)
    observaciones = forms.CharField(label='observaciones', max_length=100,required=False)
    foto = forms.FileField(label = 'foto')
   