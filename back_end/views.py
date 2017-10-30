from django.shortcuts import render
from gallery.models import *
from gallery.forms import *
from gallery.views import *
from gallery.urls import *
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator
# Create your views here.

from django.contrib.auth import logout as auth_logout

from back_end.models import Utilities
from back_end.forms import *
from django.shortcuts import *
from datetime import datetime
from _overlapped import NULL
from test.test_dis import simple

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
        #all_ventas = Linea_Venta.objects.all().order_by('-id')
        context = {
            #'all_ventas': all_ventas,
        } 
        #return render(request, 'pages/home.html', context)
        return redirect("/back_end/home", context)

@login_required    
def home(request):
    all_lineaVentas = Linea_Venta.objects.all().order_by('-id')
    context = {
        'all_lineaVentas': all_lineaVentas,
    } 
    return render(request, 'pages/home.html', context)


@login_required 
@has_role_decorator('encargado')
def listarVentas(request):
    all_ventas = Linea_Venta.objects.all().order_by('-id')
    context = {
        'all_ventas': all_ventas,
    } 
    return render(request, 'pages/ventas.html', context)

from django.core.exceptions import MultipleObjectsReturned

@login_required 
@has_role_decorator('encargado')
def informe_x(request):
    all_cajas = Caja.objects.all().order_by('id')
    for caja in all_cajas:
        try:
            aperturaCajaAbierta = AperturaCaja.objects.filter(Caja=caja, fecha_cierre_Caja__isnull=True)
        except MultipleObjectsReturned:
            print("Error, se obtuvieron mas de 1 caja abierta.")
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
    #  all_cierres = Linea_Venta.objects.all().order_by('-id')
    all_cierres = Cierres.objects.all().order_by('-id')
    context = {
        'all_cierres': all_cierres,
    } 
    return render(request, 'pages/informe_z.html', context)


@login_required 
@has_role_decorator('contador')
def reporte_ventas_producto(request):
#    all_ventas = Linea_Venta.objects.all().order_by('-id')
    context = {
 #       'all_ventas': all_ventas,
    } 
    return render(request, 'pages/reporte_ventas_producto.html', context)

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
    
    row=execQuery.getSalesProductsCountsByOpeningBoxNumber(cierre.AperturaCaja.id)
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

@login_required  
@has_role_decorator('contador')
def verCierreX(request, caja_id):
    aperturaCaja = AperturaCaja.objects.filter(Caja_id = caja_id).last()
    
    rows=execQuery.getTotalsToCloseBox(aperturaCaja.id)
    
    rows.
    
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
        x = SimpleClass()
        x.nombre = rows[0]
        x.cantidad = rows[1]
        simpleList.append(x)
        print (rows)
    
    print(simpleList)
    
    for rows in execQuery.getZETAReportDetailsByOpeningBoxNumber(aperturaCaja.id):
        print (rows)
            
    context = {
        'informe': x,
        'productosVendidos': simpleList,
    } 
    
    return render(request, 'pages/informexz.html', context)

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
