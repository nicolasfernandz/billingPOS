from django import forms

class OpeningDayForm(forms.Form):
    #cada atributo corresponde con el atributo name en el html
    fecha_creacion = forms.CharField(label='fecha_creacion', max_length=100)
    observaciones = forms.CharField(label='ovserbaciones', max_length=250)    
    codigo = forms.CharField(label='codigo', max_length=100)
    repetirCodigo = forms.CharField(label='repetirCodigo', max_length=100)
    
class ClosingDayForm(forms.Form):
    #cada atributo corresponde con el atributo name en el html
    fecha_creacion = forms.CharField(label='fecha_creacion', max_length=100)
    fecha_cierre = forms.CharField(label='fecha_cierre', max_length=100)
    
class VentasPorFechasForm(forms.Form):
    fecha_desde = forms.CharField(label='fecha_desde', max_length=100)
    fecha_hasta = forms.CharField(label='fecha_hasta', max_length=100)