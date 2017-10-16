from django.db import models

'''
class Dia(models.Model):
    fecha_apertura = models.DateTimeField(auto_now_add=True, blank=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    Observaciones = models.CharField(max_length =250)
    def __str__(self):
        return self.fecha_apertura.strftime("%d-%m-%Y %H:%M:%S")
'''
   
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
    fecha_cierre_Caja = models.DateTimeField(auto_now_add=False, blank=True)
#    Dia = models.ForeignKey(Dia, on_delete = models.CASCADE)

class Producto(models.Model):
    nombre = models.CharField(max_length =250)
    observaciones = models.CharField(max_length =250)
    foto = models.FileField()
    aplica_impuesto = models.BooleanField()

    def __str__(self):
        return self.nombre
        
class PreciosProductoFecha(models.Model):
    Producto = models.ForeignKey(Producto, on_delete = models.CASCADE,related_name='prod')
    #fecha_inicio = models.DateTimeField(auto_now_add=True, blank=True)
    #fecha_fin = models.DateTimeField(auto_now_add=True, blank=True)
    fecha_inicio = models.DateTimeField(auto_now=False, auto_now_add=False)
    fecha_fin = models.DateTimeField(auto_now=False, auto_now_add=False)    
    precio_sin_iva = models.DecimalField(max_digits=15, decimal_places=2) 
    
    def __str__(self):
        return "(%s, %s, %s, %s)" % (self.Producto.nombre,self.fecha_inicio, self.fecha_fin, self.precio_sin_iva)
    
class ImpuestosProductoFecha(models.Model):
    Producto = models.ForeignKey(Producto, on_delete = models.CASCADE)
    fecha_inicio = models.DateTimeField(auto_now=False, auto_now_add=False)
    fecha_fin = models.DateTimeField(auto_now=False, auto_now_add=False)
    porcentaje_impuesto = models.DecimalField(max_digits=15, decimal_places=2) 
    
    def __str__(self):
        return "(%s, %s, %s, %s)" % (self.Producto.nombre,self.fecha_inicio, self.fecha_fin, self.porcentaje_impuesto)
    
# Create your models here.
class Venta(models.Model):
    AperturaCaja = models.ForeignKey(AperturaCaja, on_delete = models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    total_sin_iva = models.DecimalField(max_digits=15, decimal_places=2)
    monto_iva = models.DecimalField(max_digits=15, decimal_places=2)
    total = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.fecha,self.precio
    
class Linea_Venta(models.Model):
    PreciosProductoFecha = models.ForeignKey(PreciosProductoFecha, on_delete = models.CASCADE)
    ImpuestosProductoFecha = models.ForeignKey(ImpuestosProductoFecha, on_delete = models.CASCADE)
    Venta = models.ForeignKey(Venta, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.Venta, self.PreciosProductoFecha

class Cierres(models.Model):
    AperturaCaja = models.ForeignKey(AperturaCaja, on_delete = models.CASCADE)  #Con AperturaCaja llego a todas las ventas y productos vendidos.
    fechaCierre = models.DateTimeField(auto_now_add=True, blank=True)
    total_sin_iva = models.DecimalField(max_digits=15, decimal_places=2)
    monto_iva = models.DecimalField(max_digits=15, decimal_places=2)
    total = models.DecimalField(max_digits=15, decimal_places=2)