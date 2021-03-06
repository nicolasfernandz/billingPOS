from django.shortcuts import render
from gallery.models import *
from gallery.forms import *
from gallery.views import *
from gallery.urls import *
from django.http import HttpResponse, HttpResponseRedirect, response

#imports para Roles y Permisos
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator
from django.contrib.auth import logout as auth_logout

from back_end.models import Utilities
from back_end.forms import *
from django.shortcuts import *
from datetime import datetime
from _overlapped import NULL
from test.test_dis import simple
from lib2to3.fixes.fix_input import context
from fileinput import filename
from pip import download
import logging


#Print to PDF
#https://www.codingforentrepreneurs.com/blog/html-template-to-pdf-in-django/
#pip install --pre xhtml2pdf

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/login/")

def login(request):
    #return render(request, 'pages/login.html', {})
    return HttpResponseRedirect("/login/")


from django.shortcuts import redirect

@login_required
def login_success(request):
    # Redirects users based on whether they are in the admins group
    if request.user.groups.filter(name="barman").exists():
        print (request.user.username)
        # user is an admin
        caja = request.user.username
        if (caja == 'caja1'):
            return redirect("/billingPOS/1")
        else:
            if (caja == 'caja2'):
                return redirect("/billingPOS/2")
            else:
                if (caja == 'caja3'):
                    return redirect("/billingPOS/3")
    else:
        context = {
            #'all_ventas': all_ventas,
        } 
        #return render(request, 'pages/home.html', context)
        return redirect("/back_end/home", context)


@login_required    
def home(request):
                           
    today = datetime.today()
    first_day = today.replace(day=1)        
    
    all_lineaVentas = Linea_Venta.objects.filter(Venta__fecha__gte=first_day).order_by('-id')
    
    context = {
        'month': first_day.strftime('%B'),
        'all_lineaVentas': all_lineaVentas,
    } 
    
    return render(request, 'pages/home.html', context)

'''
@login_required 
@has_role_decorator('encargado')
def listarVentas(request):
    all_ventas = Linea_Venta.objects.all().order_by('-id')
    context = {
        'all_ventas': all_ventas,
    } 
    return render(request, 'pages/ventas.html', context)
'''
from django.core.exceptions import MultipleObjectsReturned

@login_required 
@has_role_decorator('encargado')
def informe_x(request):
    #Se hace una busqueda ALL porque las cajas en este sistema, siempre seran relativamente pocas.
    all_cajas = Caja.objects.all().order_by('id')
    for caja in all_cajas:
        try:
            aperturaCajaAbierta = AperturaCaja.objects.filter(Caja=caja, fecha_cierre_Caja__isnull=True)
        except MultipleObjectsReturned:
            print("Error, se obtuvieron mas de 1 caja abierta.")
        except:
            logger = logging.getLogger(__name__)
            logger.debug('Something went wrong!')
            print("")
        else:
            if aperturaCajaAbierta is not NULL and aperturaCajaAbierta.count() > 0:
                caja.estado = 'ABIERTA' 
                print("Caja " + str(caja.id) + " abierta.")
            else:
                caja.estado = 'CERRADA' 
                print("Caja " + str(caja.id) + " abierta.")
                        
    context = {
        'all_cajas': all_cajas,
    } 
    return render(request, 'pages/informe_x.html', context)


@login_required 
@has_role_decorator('encargado')
def informe_z(request):
                               
    today = datetime.today()
    #all_cierres = Cierres.objects.filter().order_by('-id')
    #all_cierres = Cierres.objects.filter(fechaCierre__gte=today).order_by('-id')
    all_cierres = Cierres.objects.filter(fechaCierre__year=today.year, fechaCierre__month=today.month, fechaCierre__day=today.day).order_by('-id')
    
    context = {
        'all_cierres': all_cierres,
    } 
    return render(request, 'pages/informe_z.html', context)

@login_required 
@has_role_decorator('encargado')
def verInformesZPorFechas(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = VentasPorFechasForm(request.POST)
        print(form)
        
        errors = []
        error = False
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # redirect to a new URL:
            fecha_desde = form.cleaned_data['fecha_desde']
            fecha_hasta = form.cleaned_data['fecha_hasta']
                        
            from datetime import datetime
            
            dtDesde = datetime.strptime(fecha_desde, "%d/%m/%Y")
            dtHasta = datetime.strptime(fecha_hasta, "%d/%m/%Y")

            class SimpleClass(object):
                pass    
            
            x = SimpleClass()
            x.fechaDesde = fecha_desde
            x.fechaHasta = fecha_hasta
            
            if dtDesde == dtHasta:
                all_cierres = Cierres.objects.filter(fechaCierre__year=dtDesde.year, fechaCierre__month=dtDesde.month, fechaCierre__day=dtDesde.day).order_by('-id')
            else:
                all_cierres = Cierres.objects.filter(fechaCierre__range=(dtDesde, dtHasta)).order_by('-id')
            
            if all_cierres.count() <= 0:
                errors.append("No se han encontrado datos para las fechas ingresadas.")
                                                         
            if not error:
                return render(request, 'pages/informe_z.html', {'errors': errors, 'all_cierres': all_cierres,
                                                                              'fechas': x})
                            
        else:
            errors.append("Problemas con el formulario, comuniquese con el administrador.")
            return render(request, 'pages/informe_z.html', {'errors': errors})


@login_required  
@has_role_decorator('contador')
def verVenta (request, venta_id):
    verVenta = Venta.objects.get(id=venta_id)
    lineasVenta = Linea_Venta.objects.filter(Venta=verVenta)
    context = {
        'verLineasVenta': lineasVenta,
        'verVenta': verVenta,
    } 
    return render(request, 'pages/verVenta.html', context)


from django.db.models import Count, Min, Sum, Avg





        
@login_required  
@has_role_decorator('contador')
def verCierre (request, cierre_id):
    cierre = Cierres.objects.get(id=cierre_id)
    row=execQuery.getTicketsByOpeningBoxNumber(cierre.AperturaCaja.id)
    cierre.ticketDesde = row[0][1]
    cierre.ticketHasta = row[0][2]
    cierre.productosVendidos = row[0][3]
    
    class SimpleClass(object):
        pass
    
    simpleList  = []
    for rows in execQuery.getSalesProductsCountsByOpeningBoxNumber(cierre.AperturaCaja.id):
        x = SimpleClass()
        x.nombre = rows[0]
        x.cantidad = rows[1]
        simpleList.append(x)
        print (rows)
                
    context = {
        'informe': cierre,
        'productosVendidos': simpleList,
    } 
    
    return render(request, 'pages/informexz.html', context)

#Comienzo PDF
from django.views.generic import View
from Bar7a.utils import render_to_pdf
from django.template.loader import get_template

@login_required  
@has_role_decorator('contador')
def verCierreToPDF(request, cierre_id, *args, **kwargs):
    #Code para obtener datos del context
    cierre = Cierres.objects.get(id=cierre_id)
    row=execQuery.getTicketsByOpeningBoxNumber(cierre.AperturaCaja.id)
    cierre.ticketDesde = row[0][1]
    cierre.ticketHasta = row[0][2]
    cierre.productosVendidos = row[0][3]
    class SimpleClass(object):
        pass
    simpleList  = []
    for rows in execQuery.getSalesProductsCountsByOpeningBoxNumber(cierre.AperturaCaja.id):
        x = SimpleClass()
        x.nombre = rows[0]
        x.cantidad = rows[1]
        simpleList.append(x)
    context = {
        'informe': cierre,
        'productosVendidos': simpleList,
    } 
    
    template = get_template ('pages/informexz_PDF.html')
    html = template.render(context)
    pdf = render_to_pdf('pages/informexz_PDF.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "InformeX_cierre%s.pdf" %(cierre_id)
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        response['content-Disposition'] = content
        return response
    else:
        return HttpResponse("Not Found")  



import csv

@login_required  
@has_role_decorator('contador')
def verCierreImprimir(request, cierre_id):
    response = HttpResponse(content_type='text/csv')

    filename = "InformeX_cierre%s.csv" %(cierre_id)
    response['Content-Disposition'] = 'attachment; filename="%s"' %(filename)
    
    writer = csv.writer(response)

    #Code para obtener datos del context
    cierre = Cierres.objects.get(id=cierre_id)
    row=execQuery.getTicketsByOpeningBoxNumber(cierre.AperturaCaja.id)
    cierre.ticketDesde = row[0][1]
    cierre.ticketHasta = row[0][2]
    cierre.productosVendidos = row[0][3]
    class SimpleClass(object):
        pass
    simpleList  = []
    for rows in execQuery.getSalesProductsCountsByOpeningBoxNumber(cierre.AperturaCaja.id):
        x = SimpleClass()
        x.nombre = rows[0]
        x.cantidad = rows[1]
        simpleList.append(x)
    
    writer.writerow(['Detalle de Facturacion'])
    writer.writerow(['******************'])
    
    writer.writerow(['Fechas'])
    writer.writerow(['Desde:; %s' %( cierre.AperturaCaja.fecha_apertura_Caja.strftime('%Y-%m-%d %H:%M:%S') )])
    writer.writerow(['Hasta:; %s' %(cierre.AperturaCaja.fecha_cierre_Caja.strftime('%Y-%m-%d %H:%M:%S') )])
    
    writer.writerow([""])
    writer.writerow(['Caja:'])
    writer.writerow(['Nro de Caja:; %s' %(cierre.AperturaCaja.Caja.id)])
    writer.writerow(['Ubicacion:; %s' %(cierre.AperturaCaja.Caja.ubicacion)])
    
    writer.writerow([""])
    writer.writerow(['Totales:'])
    writer.writerow(['IVA:; %s %%' %(cierre.monto_iva)])
    writer.writerow(['Sub Total:; %s' %(cierre.total_sin_iva)])
    writer.writerow(['Total:; %s' %(cierre.total)])
    
    writer.writerow([""])
    writer.writerow(['Tickets:'])
    writer.writerow(['Desde Ticket Nro:; %s' %(cierre.ticketDesde)])
    writer.writerow(['Hasta Ticket Nro:; %s' %(cierre.ticketHasta)])

    writer.writerow([""])    
    writer.writerow(['Productos Vendidos:'])
    writer.writerow(['Cantidad:; %s' %(cierre.productosVendidos)])
    
    writer.writerow([""])
    writer.writerow(['Detalle Productos Vendidos'])
    writer.writerow(['Producto; Cantidad'])
    for productosVendidos in simpleList:
        writer.writerow([ "%s ; %s" %(productosVendidos.nombre, productosVendidos.cantidad) ])
    
    return response




@login_required  
@has_role_decorator('contador')
def verCierreX(request, caja_id):
    aperturaCaja = AperturaCaja.objects.filter(Caja_id = caja_id).last()
    
    rows=execQuery.getTotalsToCloseBox(aperturaCaja.id)
    
    class SimpleClass(object):
        pass
            
    x = SimpleClass()
    x.AperturaCaja = aperturaCaja
    x.total_sin_iva = rows[0][0]
    x.monto_iva = rows[0][1]
    x.total = rows[0][2]
            
    #models.Cierres.objects.create(fechaCierre= time, total_sin_iva=rows[0][0], monto_iva=rows[0][1], total=rows[0][2], AperturaCaja= caja)
    
    row=execQuery.getTicketsByOpeningBoxNumber(aperturaCaja.id)
    x.ticketDesde = row[0][1]
    x.ticketHasta = row[0][2]
    x.productosVendidos = row[0][3]
        
    row=execQuery.getSalesProductsCountsByOpeningBoxNumber(aperturaCaja.id)
    simpleList  = []
    for rows in execQuery.getSalesProductsCountsByOpeningBoxNumber(aperturaCaja.id):
        item = SimpleClass()
        item.nombre = rows[0]
        item.cantidad = rows[1]
        simpleList.append(item)
        print (rows)
    
    print(simpleList)
    
    for rows in execQuery.getZETAReportDetailsByOpeningBoxNumber(aperturaCaja.id):
        print (rows)
            
    context = {
        'informe': x,
        'productosVendidos': simpleList,
    } 
    
    return render(request, 'pages/informexz.html', context)

@login_required  
@has_role_decorator('contador')
def verEstadoCajas (request):
    #Se hace una busqueda ALL porque las cajas en este sistema, siempre seran relativamente pocas.
    all_cajas = Caja.objects.all().order_by('id')
    for caja in all_cajas:
        try:
            aperturaCajaAbierta = AperturaCaja.objects.filter(Caja=caja, fecha_cierre_Caja__isnull=True)
        except MultipleObjectsReturned:
            print("Error, se obtuvieron mas de 1 caja abierta.")
        else:
            if aperturaCajaAbierta is not NULL and aperturaCajaAbierta.count() > 0:
                caja.estado = 'ABIERTA' 
                caja.AperturaCaja = aperturaCajaAbierta.latest('id')
                print("Caja " + str(caja.id) + " abierta.")
            else:
                caja.estado = 'CERRADA'
                aperturaCajaLast = AperturaCaja.objects.filter(Caja=caja).latest('id')
                caja.AperturaCaja = aperturaCajaLast 
                print("Caja " + str(caja.id) + " abierta.")


        try:
            all_last_ventas_por_caja = Venta.objects.filter(AperturaCaja_id=caja.AperturaCaja.id)
            if all_last_ventas_por_caja is not NULL and all_last_ventas_por_caja.count() > 0:
                caja.rollosImpresos = all_last_ventas_por_caja.count()
                caja.subTotal = all_last_ventas_por_caja.aggregate(Sum('total_sin_iva')).get('total_sin_iva__sum')
                caja.iva = all_last_ventas_por_caja.aggregate(Sum('monto_iva')).get('monto_iva__sum')
                caja.total = all_last_ventas_por_caja.aggregate(Sum('total')).get('total__sum')
                
                if caja.rollosImpresos > 400:
                    caja.alertaImpresion = 'Alerta de Rollos!'
                else:
                    caja.alertaImpresion = 'Ninguna.' 
            else:
                caja.rollosImpresos = 0
                caja.subTotal = 0
                caja.iva = 0
                caja.total = 0
                caja.alertaImpresion = 'Ninguna.' 
        except:
            print("Error.")
        
    context = {
        'all_cajas': all_cajas,
    } 

    return render(request, 'pages/estado_de_cajas.html', context)

@login_required 
@has_role_decorator('contador')
def reporte_ventas_producto(request):
    context = {
#        'all_ventas_por_fechas': NULL,
    } 
    return render(request, 'pages/reporte_ventas_producto.html', context)

def ventasPorFechas(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = VentasPorFechasForm(request.POST)
        print(form)
        
        errors = []
        error = False
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # redirect to a new URL:
            fecha_desde = form.cleaned_data['fecha_desde']
            fecha_hasta = form.cleaned_data['fecha_hasta']
                        
            from datetime import datetime
            
            dtDesde = datetime.strptime(fecha_desde, "%d/%m/%Y")
            dtHasta = datetime.strptime(fecha_hasta, "%d/%m/%Y")

            class SimpleClass(object):
                pass    
            
            x = SimpleClass()
            x.fechaDesde = fecha_desde
            x.fechaHasta = fecha_hasta
            
            all_ventas_por_fecjas = Venta.objects.filter(fecha__range=(dtDesde, dtHasta))
            
            if all_ventas_por_fecjas.count() <= 0:
                errors.append("No se han encontrado datos para las fechas ingresadas.")
                                                         
            if not error:
                return render(request, 'pages/reporte_ventas_producto.html', {'errors': errors, 'all_ventas_por_fechas': all_ventas_por_fecjas,
                                                                              'fechas': x})
                            
        else:
            errors.append("Problemas con el formulario, comuniquese con el administrador.")
            return render(request, 'pages/reporte_ventas_producto.html', {'errors': errors})
            
    #return redirect("/back_end/newOpeningDay")

@login_required 
@has_role_decorator('contador')
def reporte_ventas_producto_fecha(request):
    context = {
#        'all_ventas_por_fechas': NULL,
    } 
    return render(request, 'pages/reporte_ventas_producto_fecha.html', context)

def ventasPorProductoPorFechas(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = VentasPorFechasForm(request.POST)
        print(form)
        
        errors = []
        error = False
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # redirect to a new URL:
            fecha_desde = form.cleaned_data['fecha_desde']
            fecha_hasta = form.cleaned_data['fecha_hasta']
                        
            #from datetime import datetime
            #dtDesde = datetime.strptime(fecha_desde, "%d/%m/%Y")
            #dtHasta = datetime.strptime(fecha_hasta, "%d/%m/%Y")
          
            class SimpleClass(object):
                pass    
            
            x = SimpleClass()
            x.fechaDesde = fecha_desde
            x.fechaHasta = fecha_hasta
            
            all_ventas_por_producto_por_fecha = []
            
            for theRow in execQuery.getVentaPorProductoPorFechas(fecha_desde, fecha_hasta):
                print (theRow)
                item = SimpleClass()
                item.nombre = theRow[0]
                if theRow[1] == True:
                    item.impuesto = "SI"
                else:
                    item.impuesto = "NO"
                    
                item.porcentajeImpuesto = theRow[2]  
                item.cantidadVentas = theRow[3]
                item.subTotalVentas = theRow[4]
                item.IVAVentas = theRow[5]
                item.totalVentas = theRow[6]
                all_ventas_por_producto_por_fecha.append(item)
                
            if len(all_ventas_por_producto_por_fecha)<= 0:
                errors.append("No se han encontrado datos para las fechas ingresadas.")
                                                         
            if not error:
                return render(request, 'pages/reporte_ventas_producto_fecha.html', {'errors': errors, 'all_ventas_por_producto_por_fecha': all_ventas_por_producto_por_fecha,
                                                                              'fechas': x})
        else:
            errors.append("Problemas con el formulario, comuniquese con el administrador.")
            return render(request, 'pages/reporte_ventas_producto_fecha.html', {'errors': errors})
            
    #return redirect("/back_end/newOpeningDay")

'''
def newOpeningDay (request):
    util = Utilities()
    util.todayDateTimeNow = Utilities().getTodayDateTimeNow()
    return render(request, 'pages/openingDay.html', {'util': util})


def newCloseDay (request):
    util = Utilities()
    util.todayDateTimeNow = Utilities().getTodayDateTimeNow()
    
    fechaCreacion = util.today
    errors = []
    diaActual = Dia.objects.filter(fecha_apertura__startswith=fechaCreacion)
    if not diaActual.exists():
        errors.append("Error, no existe un dia de apertura creado.")
    else:
        diaActualItem = diaActual.__getitem__(0)
        #util.fechaApertura = diaActualItem.fecha_apertura
        util.fechaApertura = diaActualItem.fecha_apertura  #.strftime('%d/%m/%Y')
           
    #return render(request, 'pages/closeDay.html', {'util': util})
    return render(request, 'pages/closeDay.html', {'errors': errors, 'util': util})

def saveOpeningDay(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = OpeningDayForm(request.POST)
        print(form)
        
        errors = []
        warnings = []
        error = False
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # redirect to a new URL:
            fechaCreacion = form.cleaned_data['fecha_creacion']
            observaciones = form.cleaned_data['observaciones']
            codigo = form.cleaned_data['codigo']
            repetirCodigo = form.cleaned_data['repetirCodigo']
            
            if not codigo == repetirCodigo:
                error = True
                errors.append("Error, los codigos de verificacion ingresados no coinciden.")
                        
            diaActual = Dia.objects.filter(fecha_apertura__startswith=fechaCreacion)
                        
            if diaActual.exists():
                error = True
                errors.append("Error, ya existe un dia de trabajo creado para la fecha ingresada.")
                                           
            if not error:
                fechaNow = Utilities().getTodayDateTimeNow()
                Dia.objects.create(fecha_apertura=fechaNow, fecha_cierre=fechaCreacion, Observaciones=observaciones)
                return redirect("/back_end")
            else:
                util = Utilities()
                util.todayDateTimeNow = Utilities().getTodayDateTimeNow()
                return render(request, 'pages/openingDay.html', {'errors': errors, 'util': util})
            
        else:
            warnings.append("Atencion, debe completar todos los campos.")
            util = Utilities()
            util.todayDateTimeNow = Utilities().getTodayDateTimeNow()
            return render(request, 'pages/openingDay.html', {'errors': errors, 'util': util, 'warnings': warnings})
            
    #return redirect("/back_end/newOpeningDay")

def saveClosingDay(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ClosingDayForm(request.POST)
        print(form)
        
        errors = []
        error = False
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # redirect to a new URL:
            fechaCreacion = form.cleaned_data['fecha_creacion']
            fecha_cierre = form.cleaned_data['fecha_cierre']
                        
            diaActual = Dia.objects.filter(fecha_apertura__startswith=fechaCreacion)
                        
            if not diaActual.exists():
                error = True
                errors.append("No existe un dia de trabajo creado.")
                
            if not error:
                fechaNow = Utilities().getTodayDateTimeNowDBFormat()
                diaActualItem = diaActual.__getitem__(0)
                diaActualItem.fecha_cierre=fechaNow
                diaActualItem.save()
                
                return redirect("/back_end")
            else:
                util = Utilities()
                util.todayDateTimeNow = Utilities().getTodayDateTimeNow()
                return render(request, 'pages/closeDay.html', {'errors': errors, 'util': util})
            
        else:
            errors.append("No existe un dia de trabajo creado.")
            util = Utilities()
            util.todayDateTimeNow = Utilities().getTodayDateTimeNow()
            return render(request, 'pages/closeDay.html', {'errors': errors, 'util': util})
            
    #return redirect("/back_end/newOpeningDay")
'''
