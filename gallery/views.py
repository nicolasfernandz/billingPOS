from django.shortcuts import render
from django.conf.urls import url
from django.views.generic import TemplateView
from django.conf import settings
from gallery.models import Producto
from .forms import *
import os
from gallery import models
from _overlapped import NULL
import json
import time
from django.db.models import Max
from Bar7a.settings import BASE_DIR
import csv
from django.http import HttpResponse

class Index(TemplateView):
    template_name='gallery/index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
       # print('static root')
        #print (settings.STATIC_ROOT)
        try:
            # Lista todos los archivos contenidos en <STATIC_ROOT>/gallery/img
            # <images> es una variable que se usara en el template <template_name>
             
            images = os.listdir(os.path.join(settings.STATIC_ROOT, 'gallery\img'))
            #print (settings.STATIC_ROOT)
            all_products = models.Producto.objects.values_list("foto", "precio")
            #all_objects = models.Producto.objects.all()
            context ={
                   'all_products':all_products,
            }
            #context['images'] = os.listdir(os.path.join(settings.STATIC_ROOT, 'gallery\img'))
           # print("Content ")
           # print (all_products)
            #print(context)
        except Exception as e:
            # Si no hay ninguna imagen retornar un arreglo vacio
            print (e)
            context['images'] = []
        return context

def cargaVenta(request):
    
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    content = body["param"]
    #print(content)
    
    producto = models.Producto.objects.get(foto=content)
    #print(producto.nombre)
    venta = models.Venta.objects.create(precio = producto.precio, fecha = time.strftime("%H:%M:%S"),Observaciones = "", cantidad_unidades = 1, caja = 1)
     
    #Revisar 
    models.Linea_Venta.objects.create(Producto = producto, Venta = venta)
    return render(request,'gallery/index.html', {})


def some_view(request):
    
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = "attachment; filename='C:\\Users\\Jorge\\Desktop\\somefilename.csv'"

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response
