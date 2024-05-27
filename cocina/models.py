# -----------------------------------------------------------------------------
# Project Adema
# Desarrolladores : Zoe Sacks / Kevin Turkienich
#
#
# -----------------------------------------------------------------------------
# Importacion de modulos

from decimal import Decimal
from django.db import models
from .Conversion import calculadora_unitario
from django.core.exceptions import ValidationError
from configuracion.models import cliente,categoria,gastosAdicionales
from configuracion.listas import UnidadDeMedida
from inventario.models import producto
from configuracion.listas import Estado


BIOTIPOPIEL = [
    ("Piel eudérmica", "Piel eudérmica"),
    ("Piel seborreica", "Piel seborreica"),
    ("Piel alipídica", "Piel alipídica"),
    ("Piel sensible", "Piel sensible"),
    ("Piel sensibilizada", "Piel sensibilizada"),
]

BIOTIPOESTADO = [
    ("Hidratado", "Hidratado"),
    ("Deshidratado", "Deshidratado"),
    ("Asfíctico", "Asfíctico"),
]

# -----------------------------------------------------------------------------
# Modelado de datos
# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
#  cliente.total_costo()    ---> Devuelve la cantidad de pedidos engregados
#  cliente.precio_venta()   ---> Devuelve el monto de la suma de los pagos a proveedores en c.c. menos los pagos en c.c.
class orden(models.Model): # Comanda
    Estado= models.CharField(choices=Estado,max_length=20,default="Pendiente",blank=False,null=False)
    Cliente = models.ForeignKey(cliente, on_delete=models.SET_NULL,blank=True,null=True)
    FechaOrden = models.DateTimeField(auto_now_add=True,null=True, blank=False)
    FechaEntrega = models.DateField(null=True, blank=True)
    Comentarios=models.TextField(verbose_name="Comentarios",null=True,blank=True) 
    TotalOrden = models.DecimalField(max_digits=25, decimal_places=2, default=0, blank=False, null=False)
    UltimaModificacion = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    Usuario = models.CharField(max_length=120, null=True, blank=True)   
    costoFinal = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    detalle_final = models.TextField(default="No terminado")
    diagnostico_final = models.TextField(default="No terminado")
        
    def __str__(self):
        return f'#{self.pk} | Cliente: {self.Cliente}'

    class Meta:
        verbose_name = 'sesion'
        verbose_name_plural ='Sesiones' 

    def clean(self):

        if self.pk:
            if self.Estado == "Entregado":
                raise ValidationError("No es posible modificar una tratamiento finalizado.")
            
            
        super().clean()

    def save(self, *args, **kwargs):
        self.TotalOrden = self.total_costo()
        super().save(*args, **kwargs)

    def total_costo(self):
        if self.Estado == "Entregado":
            valor = self.TotalOrden
        
        else:
            detalles = productoOrden.objects.filter(Orden=self)
            suma_detalles = sum(float(detalle.Cantidad) * float(detalle.Producto.precio_unitario()) for detalle in detalles)
            valor = round(suma_detalles,2)

        return valor

# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica


class AreasCara(models.Model):
    area = models.CharField(max_length=255)
    def __str__(self): 
        return self.area

class Diagnostico(models.Model):
    orden = models.ForeignKey(orden, on_delete=models.CASCADE)

    motivo_de_consulta = models.TextField(blank=True, null=True)

    biotipo_cutaneo = models.CharField(max_length=255, choices=BIOTIPOPIEL, blank=True, null=True)
    biotipo_estado = models.CharField(max_length=255, choices=BIOTIPOESTADO, blank=True, null=True)
    fototipo_cutaneo = models.PositiveIntegerField(blank=True, null=True)


    macula_vascular = models.ManyToManyField(AreasCara, related_name='macula_vascular', blank=True) 
    eritema = models.ManyToManyField(AreasCara, related_name='eritema', blank=True) 
    telangiectasias = models.ManyToManyField(AreasCara, related_name='telangiectasias', blank=True) 
    purpura = models.ManyToManyField(AreasCara, related_name='purpura', blank=True) 
    petequias = models.ManyToManyField(AreasCara, related_name='petequias', blank=True) 
    hematoma = models.ManyToManyField(AreasCara, related_name='hematoma', blank=True) 
    macula_picmentaria = models.ManyToManyField(AreasCara, related_name='macula_picmentaria', blank=True) 
    hiperpicmentada = models.ManyToManyField(AreasCara, related_name='hiperpicmentada', blank=True) 
    hipopicmentaria = models.ManyToManyField(AreasCara, related_name='hipopicmentaria', blank=True) 
    acromica = models.ManyToManyField(AreasCara, related_name='acromica', blank=True) 
    papula = models.ManyToManyField(AreasCara, related_name='papula', blank=True) 
    placa = models.ManyToManyField(AreasCara, related_name='placa', blank=True) 
    tuberculo = models.ManyToManyField(AreasCara, related_name='tuberculo', blank=True) 
    nodulo = models.ManyToManyField(AreasCara, related_name='nodulo', blank=True) 
    comedon_abierto = models.ManyToManyField(AreasCara, related_name='comedon_abierto', blank=True) 
    comedon_cerrado = models.ManyToManyField(AreasCara, related_name='comedon_cerrado', blank=True) 
    pustula = models.ManyToManyField(AreasCara, related_name='pustula', blank=True) 
    quiste_de_millium = models.ManyToManyField(AreasCara, related_name='quiste_de_millium', blank=True) 
    cicatrices = models.ManyToManyField(AreasCara, related_name='cicatrices', blank=True)


    def concatenar_campos(self):
        campos = [
            ('Motivo de consulta', self.motivo_de_consulta),
            ('Biotipo cutáneo', self.biotipo_cutaneo),
            ('Biotipo estado', self.biotipo_estado),
            ('Fototipo cutáneo', self.fototipo_cutaneo)
        ]
        
        # ManyToMany fields should be handled separately
        many_to_many_fields = [
            ('Mácula vascular', self.macula_vascular),
            ('Eritema', self.eritema),
            ('Telangiectasias', self.telangiectasias),
            ('Púrpura', self.purpura),
            ('Petequias', self.petequias),
            ('Hematoma', self.hematoma),
            ('Mácula pigmentaria', self.macula_picmentaria),
            ('Hiperpigmentada', self.hiperpicmentada),
            ('Hipopigmentaria', self.hipopicmentaria),
            ('Acromica', self.acromica),
            ('Pápula', self.papula),
            ('Placa', self.placa),
            ('Túberculo', self.tuberculo),
            ('Nódulo', self.nodulo),
            ('Comedón abierto', self.comedon_abierto),
            ('Comedón cerrado', self.comedon_cerrado),
            ('Pústula', self.pustula),
            ('Quiste de millium', self.quiste_de_millium),
            ('Cicatrices', self.cicatrices)
        ]
        
        result = []
        for nombre, valor in campos:
            if valor:
                result.append(f"{nombre}: {valor}")
        
        for nombre, campo in many_to_many_fields:
            valores = campo.all()
            if valores.exists():
                nombres_areas = ', '.join([str(area) for area in valores])
                result.append(f"{nombre}: {nombres_areas}")

        return '\n'.join(result)




class receta(models.Model):
    Nombre=models.CharField(max_length=150,blank=False,null=False,unique=True)
    Categoria = models.ForeignKey(categoria,on_delete=models.DO_NOTHING,null=True, blank=True)
    Rentabilidad = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    Comentarios=models.TextField(null=True,blank=True) 
    UltimaModificacion = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    Usuario = models.CharField(max_length=120, null=True, blank=True)
    GeneraComanda = models.BooleanField(default=False) 
    Estado = models.BooleanField(default=False)   
    costo_final = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True, null=True)

    def __str__(self):
        return f'{self.Nombre}'
    
    def clean(self):
        self.costo_final = 0
        super().clean()

    class Meta:
        verbose_name = 'tratamiento'
        verbose_name_plural ='Tratamiento' 

    def costo_receta(self):

        adicionales = gastosAdicionalesReceta.objects.filter(Receta=self)
        suma_adicionales = sum(float(adicional.Importe) if adicional.Importe is not None else 0 for adicional in adicionales)

        productos = productoReceta.objects.filter(Receta=self)
        suma_productos = sum(float(producto.subtotal()) if producto.subtotal() is not None else 0 for producto in productos)

        #subrecetas = subRecetaReceta.objects.filter(Receta=self)
        #subreceta = sum(float(subreceta.SubReceta.costo_porcion()) * float(subreceta.Cantidad) if subreceta.SubReceta.costo_porcion() is not None else 0 for subreceta in subrecetas)

        total = round(float(Decimal(suma_productos)) + float(suma_adicionales), 2)

        return total


    def precio_unitario(self):
        return self.costo_receta()
#
# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
#
class productoReceta(models.Model):
    Producto  = models.ForeignKey(producto, on_delete=models.CASCADE)
    Receta = models.ForeignKey(receta, on_delete=models.CASCADE)
    Cantidad = models.DecimalField(max_digits=20, decimal_places=2, default=1, blank=False, null=False)
    MedidaUso =  models.CharField(max_length=10, choices=UnidadDeMedida, default="Unidades", null=False, blank=False)
    UltimaModificacion = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    Usuario = models.CharField(max_length=120, null=True, blank=True)   

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural ='Productos incluidos en tratamiento' 

    def __str__(self):
        return str(self.Producto.Nombre)
    
    def clean(self):

        # Validacion de cantidad
        if self.Cantidad <= 0:
            raise ValidationError("Por favor ingrese una cantidad superior a 0.")
        
        self.MedidaUso = self.Producto.UnidadMedida

        super().clean()

    def subtotal(self):

        calculo = calculadora_unitario(medida_compra=self.Producto.UnidadMedida,medida_uso=self.MedidaUso,costo=(self.Producto.PrecioCosto / self.Producto.Cantidad),cantidad=self.Cantidad)
        # print(f' costo mililitro: {(self.Producto.PrecioCosto / self.Producto.Cantidad)}')
        # print(f' cantidad : {self.Producto.Cantidad}')

        return calculo
     
    def save(self, *args, **kwargs):
        # self.costo_unitario = self.producto.COSTO_UNITARIO
        # self.medida_uso = self.producto.UNIDAD_MEDIDA_USO
        # self.subtotal = self.producto.PRECIO_VENTA * self.cantidad
        super().save(*args, **kwargs)
#
# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
# 
class productoOrden(models.Model):
    Orden  = models.ForeignKey(orden, on_delete=models.CASCADE)
    Producto = models.ForeignKey(receta, on_delete=models.CASCADE)
    Cantidad = models.DecimalField(max_digits=20, decimal_places=2, default=1, blank=False, null=False)
    MedidaUso = models.CharField(max_length=20,choices=UnidadDeMedida,default='Unidades',blank=False,null=False)  
    CostoUnitario = models.DecimalField(max_digits=20, decimal_places=2,blank=True,null=True)
    UltimaModificacion = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    Usuario = models.CharField(max_length=120, null=True, blank=True)   

    def subtotal(self,obj):
        total = 0
        return total



# 
# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
#
class gastosAdicionalesReceta(models.Model):
    Receta = models.ForeignKey(receta, on_delete=models.CASCADE)
    Adicional  = models.ForeignKey(gastosAdicionales, on_delete=models.CASCADE)
    Importe = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    Usuario = models.CharField(max_length=120, null=True, blank=True)   

    class Meta:
        verbose_name = 'gasto'
        verbose_name_plural ='Adicionales incluidos en la tratamiento' 

    def __str__(self):
        return str(self.Receta.Nombre)
    
    def clean(self):
        if self.Importe <= 0:
            raise ValidationError("El importe del gasto adicional no puede ser inferior o igual a $ 0.")
        super().clean()


'''

#
# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
#
class subReceta(models.Model):
    Nombre=models.CharField(max_length=150,blank=False,null=False,unique=True)
    Detalles=models.TextField(verbose_name="Comentarios",null=True,blank=True) 
    Porciones = models.DecimalField(max_digits=15,decimal_places=2, default=1, blank=False,null=False)
    UltimaModificacion = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    Usuario = models.CharField(max_length=120, null=True, blank=True)   
    Estado = models.BooleanField(default=False)  

    def __str__(self):
        return f'{self.Nombre}'

    class Meta:
        verbose_name = 'tratamiento base'
        verbose_name_plural ='Tratamiento base' 

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def costo_porcion(self):
        detalles = productoSubReceta.objects.filter(SubReceta=self)
        suma_detalles = sum(detalle.total() for detalle in detalles)
        porciones = float(self.Porciones)
        valor = round(float(suma_detalles) / float(porciones),2)
        return valor
    
    def costo_total(self):
        detalles = productoSubReceta.objects.filter(SubReceta=self)
        suma_detalles = sum(detalle.total() for detalle in detalles)
        valor = round(float(suma_detalles),2)
        return valor

        
# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
#
class productoSubReceta(models.Model):
    Producto  = models.ForeignKey(producto, on_delete=models.CASCADE)
    SubReceta = models.ForeignKey(subReceta, on_delete=models.CASCADE)
    Cantidad = models.DecimalField(max_digits=20, decimal_places=2, default=1, blank=False, null=False)
    MedidaUso = models.CharField(max_length=20,choices=UnidadDeMedida,default='Unidades',blank=False,null=False)  

    class Meta:
        verbose_name = 'insumo'
        verbose_name_plural ='Insumos incluidos en el sub-tratamiento' 

    def __str__(self):
        return str(self.SubReceta.Nombre)
    
    def clean(self):
        # Validaciones:
        # No se puede ingresar una cantidad menor o igual a 0.
        if self.Cantidad <= 0:
            raise ValidationError("Por favor ingrese una cantidad superior a 0.")
        
        # Obtener medidas de uso para validacion
        medida_compra = self.Producto.UnidadMedida
        medida_uso = self.MedidaUso

        # Validacion de unidad de medida
        if medida_compra != medida_uso:

            if medida_compra == "Unidades":
                if medida_uso != "Unidades":
                    raise ValidationError("La unica medida de uso aceptada es 'Unidades'.") 
            elif medida_compra == "Kilogramos":
                if medida_uso != "Kilogramos" and medida_uso != "Gramos":
                    raise ValidationError("El producto comprado tiene unidad de medida 'Kilogramos', por lo que sólo puede seleccionar 'Kilogramos' o 'Gramos' como medida de uso.")  
            elif medida_compra == "Litros":
                if medida_uso != "Litros" and medida_uso != "Mililitros":
                    raise ValidationError("El producto comprado tiene unidad de medida 'Litros', por lo que sólo puede seleccionar 'Litros' o 'Mililitros' como medida de uso.")  
            elif medida_compra == "Gramos":
                if medida_uso != "Gramos" and medida_uso != "Kilogramos":
                    raise ValidationError("El producto comprado tiene unidad de medida 'Gramos', por lo que sólo puede seleccionar 'Gramos' o 'Kilogramos' como medida de uso.")  
            elif medida_compra == "Mililitros":
                if medida_uso != "Mililitros" and medida_uso != "Litros":
                    raise ValidationError("El producto comprado tiene unidad de medida 'Mililitros', por lo que sólo puede seleccionar 'Mililitros' o 'Litros' como medida de uso.")  
            elif medida_compra == "Libras":
                if medida_uso != "Libras" and medida_uso != "Onzas":
                    raise ValidationError("El producto comprado tiene unidad de medida 'Libras', por lo que sólo puede seleccionar 'Libras' u 'Onzas' como medida de uso.")  
            elif medida_compra == "Onzas":
                raise ValidationError("El producto comprado tiene unidad de medida 'Onzas', por lo que sólo puede seleccionar 'Onzas' como medida de uso.")  

        super().clean()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def total(self):

        calculo = calculadora_unitario(medida_compra=self.Producto.UnidadMedida,medida_uso=self.MedidaUso,costo=(self.Producto.PrecioCosto / self.Producto.Cantidad),cantidad=self.Cantidad)

        if not calculo:
            calculo = 0
        return calculo  

# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
#
class subRecetaReceta(models.Model):
    Receta = models.ForeignKey(receta, on_delete=models.CASCADE)
    SubReceta  = models.ForeignKey(subReceta, on_delete=models.CASCADE)
    Cantidad = models.DecimalField(max_digits=20, decimal_places=2, default=1, blank=False, null=False)
    Usuario = models.CharField(max_length=120, null=True, blank=True)   

    class Meta:
        verbose_name = 'sub tratamiento'
        verbose_name_plural ='Sub tratamiento incluido en el tratamiento' 

    def __str__(self):
        return str(self.SubReceta.Nombre)
    
    def clean(self):
        if self.Cantidad <= 0:
            raise ValidationError("La cantidad no puede ser inferior o igual a $ 0.")
        super().clean()

    def subtotal(self):
        total = self.SubReceta.costo_porcion() * self.Cantidad
        return total

'''
