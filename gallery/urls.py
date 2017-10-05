from django.conf.urls import url
from . import views
from .views import Index

urlpatterns = [
    #url(r'^$', Index.as_view(), name='index'),
    url(r'^$', views.get_context_data, name='index'),
    
    url(r'ventas/cargaVenta/', views.cargaVenta, name = 'cargaVenta'),
    url(r'^ventas/some/', views.some_view, name = 'pruebas'),
    url(r'ventas/aperturaCaja/', views.aperturaCaja, name = 'aperturaCaja'),
    
    url(r'^logout', views.logout),
]
