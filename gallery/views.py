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

from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator
# Create your views here.

from django.contrib.auth import logout as auth_logout
from django.template.context_processors import request

from django.http import HttpResponse, HttpResponseRedirect

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/login/")

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
            #print( all_products)
            
            #----------------------------------------------------------------------
            all_p = models.Producto.objects.values_list("foto", "id")
            
            prod = []
            for item in all_p:
               # print(item[0])
                #print(item[1])
                
                auxTime =  timezone.now() 
               
                #precio = models.PreciosProductoFecha.objects.filter(fecha_inicio__lte=auxTime, fecha_fin__gt=auxTime, Producto_id = item[1])
                precio = models.PreciosProductoFecha.objects.all().filter(fecha_inicio__lte=auxTime, fecha_fin__gt=auxTime, Producto_id = item[1]).values_list('precio_sin_iva','id')    
                impuesto = models.ImpuestosProductoFecha.objects.all().filter(fecha_inicio__lte=auxTime, fecha_fin__gt=auxTime, Producto_id = item[1]).values_list('porcentaje_impuesto','id')    
                
                #print(impuesto)
                for elem in precio:
                    prc = elem[0]
                    for imp in impuesto:
                        
                        total_imp = (prc) * (imp[0]/100)
                        prc =  prc + total_imp
                    aux = (item[0], '{0:.4}'.format(prc), item[1])
                    
                    #prod.append(aux)
                    #print(prod)
                    break
                 
                
                
            #all_ = models.PreciosProductoFecha.objects.all().prefetch_related('prod_set')
     
            #print('+++++++++++++++++++++')
            context ={
                  #'all_products':all_products,
                  #'all_products':prod,
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

@login_required
def get_context_data(request,caja_id ):
       # context = super(Index, self).get_context_data(**kwargs)
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
            all_p = models.Producto.objects.values_list("foto", "id", "observaciones")
            
            prod = []
            for item in all_p:
                #print(item[0])
               # print(item[1])
                
                auxTime =  timezone.now() 
               
                #precio = models.PreciosProductoFecha.objects.filter(fecha_inicio__lte=auxTime, fecha_fin__gt=auxTime, Producto_id = item[1])
                precio = models.PreciosProductoFecha.objects.all().filter(fecha_inicio__lte=auxTime, fecha_fin__gt=auxTime, Producto_id = item[1]).values_list('precio_sin_iva','id')    
                impuesto = models.ImpuestosProductoFecha.objects.all().filter(fecha_inicio__lte=auxTime, fecha_fin__gt=auxTime, Producto_id = item[1]).values_list('porcentaje_impuesto','id')    
                
                #print(impuesto)
                for elem in precio:
                    prc = elem[0]
                    for imp in impuesto:
                        
                        total_imp = (prc) * (imp[0]/100)
                        prc =  prc + total_imp
                    aux = (item[0], '{0:.4}'.format(prc), item[1],item[2])
                    
                    
                    prod.append(aux)
                    break
                 
                
                
            #all_ = models.PreciosProductoFecha.objects.all().prefetch_related('prod_set')
     
            #print('prod: ' + str(prod))
            context ={
                  #'all_products':all_products,
                  'all_products':prod,
                  'caja_id':caja_id,
            }
            #context['images'] = os.listdir(os.path.join(settings.STATIC_ROOT, 'gallery\img'))
           # print("Content ")
           # print (all_products)
            #print(context)
        except Exception as e:
            # Si no hay ninguna imagen retornar un arreglo vacio
            print (e)
            context['images'] = []
        return render(request, 'gallery/index.html', context)

def cargaVenta(request):
    
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
   # aux = json.parse()
    content = body['param']
    
    #print(content)
    
    parametros = content.split(',')
    
    nom_producto = parametros[0].strip()
    precio_param = parametros[1].strip()
    num_caja = parametros[2].strip()
    id = parametros[3].strip()
    observaciones = parametros[4].strip()
    #print('producto: ' +  nom_producto)
    #print('caja: ' + num_caja)
    #print('precio: ' +precio)
    #print('id: ' +id)
    
    #obtengo la caja de la tabla
    caja = models.Caja.objects.get(id = num_caja)
    
    #obtengo el producto de la tabla
    producto = models.Producto.objects.get(id=id)
    #print(producto.nombre)
    
    time =  timezone.now()
    
    print(observaciones)
    precio = models.PreciosProductoFecha.objects.filter(fecha_inicio__lte=time, fecha_fin__gt=time, Producto=producto)    
    if(observaciones == "pago_tarjeta"):
        precio_sin_iva = int(precio_param)
    else:
        precio_sin_iva = 0+precio.first().precio_sin_iva
    prec_prod = precio.first()
    
    #print(precio.first().precio_sin_iva) 
    impuesto = models.ImpuestosProductoFecha.objects.all().filter(fecha_inicio__lte=time, fecha_fin__gt=time, Producto=producto)                
    
    metodoPago = models.Metodo_de_Pago.objects.get(id = 1)           
    
    
    #print(precio)
    montoIVA = 0
    if(impuesto.first() is not None):
        montoIVA = precio_sin_iva*impuesto.first().porcentaje_impuesto/100
    apertura_caja = models.AperturaCaja.objects.filter(fecha_apertura_Caja__lte=time, fecha_cierre_Caja__isnull=True, Caja = caja)    
    #print( apertura_caja.first())
    if apertura_caja.first() is not None:
        #print('entre a realizar una venta')
        venta = models.Venta.objects.create(total_sin_iva =precio_sin_iva, fecha = time,monto_iva =montoIVA, AperturaCaja=apertura_caja.first(),total=montoIVA+precio_sin_iva, MetodoPago = metodoPago )
        #prec_prod = precio.first()
        imp_prod = impuesto.first()
        #if(observaciones != "pago_tarjeta"):
        linea_venta = models.Linea_Venta.objects.create(PreciosProductoFecha=prec_prod, ImpuestosProductoFecha =imp_prod , Venta = venta)
    
    
    
    #Revisar 
    #models.Linea_Venta.objects.create(Producto = producto, Venta = venta)
    return HttpResponse(json.dumps('ventaExitosa'), content_type="application/json")


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
    content = body["param"]
    
    caja = models.Caja.objects.get(id=content)
    #print(caja.Descripcion)
    auxTime =  timezone.now() 
    #print(content)
    #models.AperturaCaja.objects.create(fecha_apertura_Caja = auxTime,fecha_cierre_Caja='9999-12-31 00:00:00.000000+00:00', Caja= caja)
    models.AperturaCaja.objects.create(fecha_apertura_Caja = auxTime, Caja= caja)
 #   apertura_dia = models.Dia.objects.filter(fecha_apertura__lte=content, fecha_cierre__gt=content)    
  #  print(apertura_dia.first())
   # if apertura_dia.first() is not None:
    #    print('jojojojojo')
    return HttpResponse(json.dumps('permitirAperturaCaja'), content_type="application/json")
    
    #return HttpResponse(json.dumps('denegarAperturaCaja'), content_type="application/json")
def checkCaja(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    content = body["param"]
    
    caja = AperturaCaja.objects.filter(Caja_id = content).last()
    time =  timezone.now() 
    
    
    if(caja.fecha_cierre_Caja is None):
        return HttpResponse(json.dumps('existeCajaAbierta'), content_type="application/json")
    else:
        return HttpResponse(json.dumps('cajaCerrada'), content_type="application/json")
    
from gallery import execQuery   
def cierreCaja(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    idCaja = body["param"]
    
    caja = AperturaCaja.objects.filter(Caja_id = idCaja).last()
    time =  timezone.now() 
    caja.fecha_cierre_Caja = time
    caja.save()
    
    rows=execQuery.getTotalsToCloseBox(caja.id)  #caja.id): Aca va el id de Apertura Caja
    
    #for rows in execQuery.getTotalsToCloseBox(1):
    #    print (rows)
        
    models.Cierres.objects.create(fechaCierre= time, total_sin_iva=rows[0][0], monto_iva=rows[0][1], total=rows[0][2], AperturaCaja= caja)
    
    return HttpResponse(json.dumps('permitirAperturaCaja'), content_type="application/json")