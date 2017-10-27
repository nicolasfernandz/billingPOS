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
    
        #Cierre/[CierreID] 
    url(r'^cierre-(?P<cierre_id>[0-9]+)$', views.verCierre),
    
        #Client/[clientID] 
    url(r'^(?P<venta_id>[0-9]+)$', views.verVenta, name = 'Ver Venta'),
    
#    url(r'^login', views.login),

    
    #url(r'^newOpeningDay', views.newOpeningDay, name = 'New Opening Day'),
    
    #url(r'^newCloseDay', views.newCloseDay, name = 'New Close Day'),
    
    #url(r'^saveOpeningDay/', views.saveOpeningDay, name = 'Save Opening Day'),
    
    #url(r'^saveClosingDay/', views.saveClosingDay, name = 'Save Closing Day'),
    


]
