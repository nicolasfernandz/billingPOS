from django.conf.urls import url
from . import views
from .views import Index

urlpatterns = [
    #url(r'^$', Index.as_view(), name='index'),
   # url(r'^$', views.get_context_data, name='index'),
    url(r'(?P<caja_id>[0-9]{1})', views.get_context_data, name='index'),
    
    url(r'ventas/cargaVenta/', views.cargaVenta, name = 'cargaVenta'),
    url(r'^ventas/some/', views.some_view, name = 'pruebas'),
    url(r'ventas/aperturaCaja/', views.aperturaCaja, name = 'aperturaCaja'),
    url(r'ventas/cierreCaja/', views.cierreCaja, name = 'cierreCaja'),
    url(r'ventas/checkCaja/', views.checkCaja, name = 'checksCaja'),
    
    url(r'^logout', views.logout),
]
