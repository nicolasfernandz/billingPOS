from django.contrib import admin
from .models import Linea_Venta, Producto, Venta
from gallery.models import *
# Register your models here.
admin.site.register(Linea_Venta)
admin.site.register(Producto)
admin.site.register(Venta)
admin.site.register(Caja)

admin.site.register(ImpuestosProductoFecha)

admin.site.register(PreciosProductoFecha)
 

admin.site.register(AperturaCaja)

    
