from django.shortcuts import render
from django.conf.urls import url
from django.views.generic import TemplateView
from django.conf import settings
from gallery.models import *
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
from datetime import date
from _datetime import datetime
import datetime
import time
from django.utils import timezone

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
            #----------------------------------------------------------------------
            all_products = models.Producto.objects.values_list("foto")
            print( all_products)
            
            #----------------------------------------------------------------------
            all_p = models.Producto.objects.values_list("foto", "id")
            
            prod = []
            for item in all_p:
                print(item[0])
                print(item[1])
                
                auxTime =  timezone.now() 
               
                #precio = models.PreciosProductoFecha.objects.filter(fecha_inicio__lte=auxTime, fecha_fin__gt=auxTime, Producto_id = item[1])
                precio = models.PreciosProductoFecha.objects.all().filter(fecha_inicio__lte=auxTime, fecha_fin__gt=auxTime, Producto_id = item[1]).values_list('precio_sin_iva','id')    
                
                for elem in precio:
                    print(elem[0])
                    aux = (item[0], elem[0])
                    prod.append(aux)
                    break
                 
                
                
            #all_ = models.PreciosProductoFecha.objects.all().prefetch_related('prod_set')
     
             
            context ={
                  #'all_products':all_products,
                  'all_products':prod,
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
    contentb = body['a']
    print(contentb)
    
    producto = models.Producto.objects.get(foto=content)
    print(producto.nombre)
    venta = models.Venta.objects.create(precio = producto.precio, fecha = time.strftime("%H:%M:%S"),Observaciones = "", cantidad_unidades = 1, AperturaCaja_id = 1)
     
    #Revisar 
    #models.Linea_Venta.objects.create(Producto = producto, Venta = venta)
    return render(request,'gallery/index.html', {})


def some_view(request):
    
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = "attachment; filename='C:\\Users\\Jorge\\Desktop\\somefilename.csv'"

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response

def aperturaCaja(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    #content = body["param"]
    
    caja = models.Caja.objects.get(id=1)
    print(caja.Descripcion)
    auxTime =  timezone.now() 
    print(auxTime)
    models.AperturaCaja.objects.create(fecha_apertura_Caja = auxTime,fecha_cierre_Caja='9999-12-31 00:00:00.000000+00:00', Caja= caja)
 #   apertura_dia = models.Dia.objects.filter(fecha_apertura__lte=content, fecha_cierre__gt=content)    
  #  print(apertura_dia.first())
   # if apertura_dia.first() is not None:
    #    print('jojojojojo')
    return HttpResponse(json.dumps('permitirAperturaCaja'), content_type="application/json")
    
    #return HttpResponse(json.dumps('denegarAperturaCaja'), content_type="application/json")
    