from django.contrib import admin
from .models import Linea_Venta, Producto, Venta
from gallery.models import AperturaCaja, Caja, Dia
# Register your models here.
admin.site.register(Linea_Venta)
admin.site.register(Producto)
admin.site.register(Venta)
admin.site.register(Dia)
admin.site.register(Caja)
admin.site.register(AperturaCaja)