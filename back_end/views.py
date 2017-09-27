from django.shortcuts import render
from gallery.models import Venta, Linea_Venta
from gallery.forms import *
from gallery.views import *
from gallery.urls import *
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator
# Create your views here.

from django.contrib.auth import logout as auth_logout


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/login/")

def login(request):
    return render(request, 'pages/login.html', {})


from django.shortcuts import redirect

@login_required
def login_success(request):
   # Redirects users based on whether they are in the admins group
    if request.user.groups.filter(name="barman").exists():
        # user is an admin
        return redirect("/billingPOS")
    else:
        all_ventas = Linea_Venta.objects.all().order_by('-id')
        context = {
            'all_ventas': all_ventas,
        } 
        #return render(request, 'pages/home.html', context)
        return redirect("/back_end/home.html", context)

@login_required    
def home(request):
    all_ventas = Linea_Venta.objects.all().order_by('-id')
    context = {
        'all_ventas': all_ventas,
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


@login_required 
@has_role_decorator('encargado')
def informe_x(request):
    all_ventas = Linea_Venta.objects.all().order_by('-id')
    context = {
        'all_ventas': all_ventas,
    } 
    return render(request, 'pages/informe_x.html', context)


@login_required 
@has_role_decorator('encargado')
def informe_z(request):
    all_ventas = Linea_Venta.objects.all().order_by('-id')
    context = {
        'all_ventas': all_ventas,
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