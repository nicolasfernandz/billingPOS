from django.db import models

class Dia(models.Model):
    fecha_apertura = models.DateTimeField(auto_now_add=True, blank=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    Observaciones = models.CharField(max_length =250)
    def __str__(self):
        return self.fecha_apertura.strftime("%d-%m-%Y %H:%M:%S")
   
class Caja(models.Model):
    Descripcion = models.CharField(max_length =250)
    ubicacion = models.CharField(max_length =250)
    modelo = models.CharField(max_length =250, null=True)
    numero_serie = models.CharField(max_length =250, null=True)
    def __str__(self):
        return self.Descripcion + " - " + self.ubicacion

class AperturaCaja(models.Model):
    Caja = models.ForeignKey(Caja, on_delete = models.CASCADE)
    fecha_apertura_Caja = models.DateTimeField(auto_now_add=True, blank=True)
    fecha_cierre_Caja = models.DateTimeField(auto_now_add=True, blank=True)
    Dia = models.ForeignKey(Dia, on_delete = models.CASCADE)
    
# Create your models here.
class Venta(models.Model):
    AperturaCaja = models.ForeignKey(AperturaCaja, on_delete = models.CASCADE)
    precio = models.DecimalField(max_digits=15, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    Observaciones = models.CharField(max_length =250)
    cantidad_unidades = models.IntegerField(null = True)
    def __str__(self):
        return self.fecha,self.precio
    
class Producto(models.Model):
    precio = models.DecimalField(max_digits=15, decimal_places=2)
    nombre = models.CharField(max_length =250)
    observaciones = models.CharField(max_length =250)
    foto = models.FileField()
    def __str__(self):
        return self.nombre,self.precio
        
class Linea_Venta(models.Model):
    Producto = models.ForeignKey(Producto, on_delete = models.CASCADE)
    Venta = models.ForeignKey(Venta, on_delete = models.CASCADE)
    def __str__(self):
        return self.Venta, self.Producto
