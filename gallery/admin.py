from django.contrib import admin
from .models import Linea_Venta, Producto, Venta
# Register your models here.
admin.site.register(Linea_Venta)
admin.site.register(Producto)
admin.site.register(Venta)