from django.db import models

# Create your models here.
class Venta(models.Model):
    precio = models.DecimalField(max_digits=15, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    Observaciones = models.CharField(max_length =250)
    cantidad_unidades = models.IntegerField(null = True)
    caja = models.IntegerField(null = True)
    def _str_(self):
        return self.fecha,self.precio
    
class Producto(models.Model):
    precio = models.DecimalField(max_digits=15, decimal_places=2)
    nombre = models.CharField(max_length =250)
    observaciones = models.CharField(max_length =250)
    foto = models.FileField()
    def _str_(self):
        return self.nombre,self.precio
        
class Linea_Venta(models.Model):
    Producto = models.ForeignKey(Producto, on_delete = models.CASCADE)
    Venta = models.ForeignKey(Venta, on_delete = models.CASCADE)
    def _str_(self):
        return self.Venta, self.Producto
