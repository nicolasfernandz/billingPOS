from django.shortcuts import render
from gallery.models import Venta, Linea_Venta
from gallery.forms import Producto
import csv
from django.http import HttpResponse
# Create your views here.

def listarVentas(request):
    
    all_ventas = Linea_Venta.objects.all().order_by('-id')
     

    context = {
        'all_ventas': all_ventas,
    } 
    return render(request, 'pages/ventas.html', context)