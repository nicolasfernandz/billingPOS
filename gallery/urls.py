from django.conf.urls import url
from . import views
from .views import Index

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    
    url(r'^ventas/cargaVenta/', views.cargaVenta, name = 'pruebas'),
    url(r'^ventas/some/', views.some_view, name = 'pruebas'),
   
]
