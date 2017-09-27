from django.conf.urls import url
from . import views

urlpatterns = [
    
    url(r'^$', views.home, name = 'home'),    
    url(r'^home', views.home, name='Home'),
    
    url(r'^listarVentas', views.listarVentas, name = 'listarVentas'),
    
    url(r'^informe_x', views.informe_x, name = 'Informe X'),
    
    url(r'^informe_z', views.informe_z, name = 'Informe Z'),

    url(r'^reporte_ventas_producto', views.reporte_ventas_producto, name = 'Reporte Ventas por Productos'),

    url(r'^logout', views.logout),
    
#    url(r'^login', views.login),
    


]
