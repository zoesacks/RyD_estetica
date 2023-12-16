# -----------------------------------------------------------------------------
# Project Adema
# Desarrolladores : Zoe Sacks / Kevin Turkienich
# 
#
# Importacion de modulos nativos
from django.db import models, transaction
from django.core.exceptions import ValidationError

from decimal import Decimal

# Importaciones modulos custom
from configuracion.models import proveedor,categoria,deposito, cliente
from configuracion.listas import UnidadDeMedida

# -----------------------------------------------------------------------------
# Modelado de datos
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Metodos 
# 
# producto.costo_unitario()    ---> Devuelve la cantidad de pedidos engregados
# producto.precio_venta()   ---> Devuelve el monto de la suma de los pagos a proveedores en c.c. menos los pagos en c.c.

class producto(models.Model):
    Codigo = models.CharField(max_length=120, null=False, blank=False,unique=True)
    Nombre = models.CharField(max_length=120, null=False, blank=False)
    Descripcion = models.CharField(max_length=120, null=True, blank=True)
    InformacionAdicional = models.TextField(null=True, blank=True)
    Proveedor = models.ForeignKey(proveedor,on_delete=models.DO_NOTHING,blank=True,null=True)
    Categoria = models.ForeignKey(categoria,on_delete=models.DO_NOTHING,null=True, blank=True)
    Cantidad = models.DecimalField(max_digits=20, decimal_places=2, default=1, blank=False, null=False)
    UnidadMedida = models.CharField(max_length=10, choices=UnidadDeMedida, default="Unidades", null=False, blank=False)
    PrecioCosto = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    CostoDolar = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    Rentabilidad = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    Stock = models.IntegerField(default=0,null=True,blank=True)
    HabilitarVenta = models.BooleanField(default=False)
    UltimaModificacion = models.DateTimeField(auto_now_add=True)
    Usuario = models.CharField(max_length=120, null=True, blank=True)
    precio_final = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False) 

    def __str__(self):
        return f'{self.Nombre} x {self.Cantidad} {self.UnidadMedida[:3]}'
    
    def clean(self):
        if self.PrecioCosto == 0:
            raise ValidationError('El costo no puede ser 0.')

        if self.precio_final < self.PrecioCosto:
            self.precio_final = self.PrecioCosto
            
        super().clean()

    def save(self):
        if self.precio_final < self.PrecioCosto:
            self.precio_final = self.PrecioCosto
        super().save()
        
    class Meta:
        verbose_name = 'producto'
        verbose_name_plural ='Productos' 

    def precio_unitario(self):
        '''
        ganancia = Decimal(self.Rentabilidad)
        costo = Decimal(self.PrecioCosto)
        precio = (costo / (Decimal(100) - ganancia)) *100
        '''
        return self.PrecioCosto

# -----------------------------------------------------------------------------
# Metodos 
# 
# producto.costo_unitario()    ---> Devuelve la cantidad de pedidos engregados
# producto.precio_venta()   ---> Devuelve el monto de la suma de los pagos a proveedores en c.c. menos los pagos en c.c.

class movimientoInventarios(models.Model):
    Producto = models.ForeignKey(producto, on_delete=models.DO_NOTHING, blank=True, null=True)
    DepositoSalida = models.ForeignKey(deposito, on_delete=models.DO_NOTHING, null=False, blank=False,default=1, related_name='movimientos_salida')
    DepositoEntrada = models.ForeignKey(deposito, on_delete=models.DO_NOTHING, null=False, blank=False,default=1, related_name='movimientos_entrada')
    Cantidad = models.DecimalField(max_digits=20, decimal_places=2, default=1, blank=False, null=False)
    InformacionAdicional = models.TextField(null=True, blank=True)
    Estado = models.BooleanField(default=True)
    UltimaModificacion = models.DateTimeField(auto_now_add=True)
    Usuario = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return f'{self.Producto}'
    
    def clean(self):
        super().clean()

    class Meta:
        verbose_name = 'movimiento'
        verbose_name_plural ='Movimientos deposito' 

class Compra(models.Model):
    fecha = models.DateField()


class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto = models.ForeignKey(producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    costo_unidad = models.IntegerField(default=0)
    precio_venta = models.IntegerField(default=0)

    def clean(self):
        if self.precio_venta == 0:
            self.precio_venta = self.costo_unidad

        self.producto.PrecioCosto = self.costo_unidad
        self.producto.precio_final = self.precio_venta
        self.producto.save()
        super().clean()


class Venta(models.Model):
    fecha = models.DateField()
    cliente = models.ForeignKey(cliente, on_delete=models.PROTECT)

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    costo_unidad = models.IntegerField(default=0)

    def clean(self):
        if self.costo_unidad == 0:
            self.costo_unidad = self.producto.precio_final
        super().clean()

    