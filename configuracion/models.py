# -----------------------------------------------------------------------------
# Project Adema
# Desarrolladores : Zoe Sacks / Kevin Turkienich
#
#
# Importacion de modulos
from django.db import models
from configuracion.listas import Monedas
from django.contrib.auth.models import User
# -----------------------------------------------------------------------------
# Modelado de datos
# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
# cliente.pedidos()    ---> Devuelve la cantidad de pedidos engregados
# cliente.cuenta_corriente()   ---> Devuelve el monto de la suma de los pagos a proveedores en c.c. menos los pagos en c.c.
class cliente(models.Model):
    NumeroCliente= models.AutoField(primary_key=True)
    NombreApellido=models.CharField(max_length=120,null=False,blank=False)
    Direccion=models.CharField(max_length=255,null=True,blank=True)
    Email=models.CharField(max_length=120,null=True,blank=True)
    Telefono =models.CharField(max_length=15,null=True,blank=True)
    UltimaModificacion = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    Usuario = models.CharField(max_length=120, null=True, blank=True)   

    def __str__(self): # Como se muestra el objeto en una relacion foranea
        return self.NombreApellido

    class Meta:
        verbose_name = 'cliente'  # Como se va a nombrar el objeto de la instancia
        verbose_name_plural ='Clientes'  # Como se nombra el modelo

    def pedidos():
        # Funcion para obtener la cantidad de pedidos engregados
        # Falta armar funcion
        pass

    def cuenta_corriente():
        # Funcion que Devuelve el monto de la suma de los pagos a proveedores en c.c. menos los pagos en c.c
        # Falta armar funcion
        pass
# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
# proveedor.pedidos()    ---> Devuelve la cantidad de compras confirmadas
# proveedor.cuenta_corriente()   ---> Devuelve el monto de la suma de los pagos a proveedores en c.c. menos los pagos en c.c.
class proveedor(models.Model):
    Empresa=models.CharField(max_length=120,null=False,blank=False) 
    NombreApellido=models.CharField(max_length=120,null=False,blank=False) 
    Direccion=models.CharField(max_length=120,null=True,blank=True)
    Email=models.EmailField(null=True,blank=True)
    Telefono=models.CharField(max_length=120,null=False,blank=False)
    UltimaModificacion = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    Usuario = models.CharField(max_length=120, null=True, blank=True)   

    def __str__(self):
        return self.Empresa
    
    class Meta:
        verbose_name = 'proveedor' # Como se va a nombrar el objeto de la instancia
        verbose_name_plural ='Proveedores' # Como se nombra el modelo

    def pedidos():
        # Falta armar funcion
        pass

    def cuenta_corriente():
        # Falta armar funcion
        pass
# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
# proveedor.pedidos()    ---> Devuelve la cantidad de compras confirmadas
# proveedor.cuenta_corriente()   ---> Devuelve el monto de la suma de los pagos a proveedores en c.c. menos los pagos en c.c.
class categoria(models.Model):
    Descripcion = models.CharField(max_length=120, null=False, blank=False,unique=True)
    UltimaModificacion = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    Usuario = models.CharField(max_length=120, null=True, blank=True)   

    def __str__(self):
        return self.Descripcion
    
    class Meta:
        verbose_name = 'categoria'  # Como se va a nombrar el objeto de la instancia
        verbose_name_plural ='Categorias' # Como se nombra el modelo
# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
#   configuracion.moneda()   ---> devuelve la moneda en la que se trabaja
#
class miEmpresa(models.Model):
    Empresa = models.CharField(max_length=100,unique=True)
    Moneda = models.CharField(max_length=20,choices=Monedas,default="ARS",blank=False,null=False)
    Direccion = models.CharField(max_length=255,blank=True, null=True)
    Telefono = models.CharField(max_length=255,blank=True, null=True)
    Horarios = models.CharField(max_length=255,blank=True, null=True)
    
    def clean(self): # Metodo para verificar algun  campo antes de guardar.
        super().clean()
        
    def __str__(self): # Como se muestra el objeto en una relacion foranea
        return f'{self.Empresa} ({self.Moneda})'

    class Meta: # Metodo para nombrar el modelo
        verbose_name = 'empresa'  # Como se va a nombrar el objeto de la instancia
        verbose_name_plural ='Mi empresa'  # Como se nombra el modelo 

# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
#   configuracion.moneda()   ---> devuelve la moneda en la que se trabaja
#
class deposito(models.Model):
    Nombre = models.CharField(max_length=100,unique=True,blank=False,null=False)

    def clean(self): # Metodo para verificar algun  campo antes de guardar.
        super().clean()

    def __str__(self): # Como se muestra el objeto en una relacion foranea
        return self.Nombre
    
    class Meta: # Metodo para nombrar el modelo
        verbose_name = 'deposito'  # Como se va a nombrar el objeto de la instancia
        verbose_name_plural ='Deposito' # Como se nombra el modelo

# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
#   configuracion.moneda()   ---> devuelve la moneda en la que se trabaja
#
class gastosAdicionales(models.Model):
    Descripcion = models.CharField(max_length=100,unique=True,blank=False,null=False)

    def __str__(self):
        return self.Descripcion
    
    class Meta:
        verbose_name = 'gasto'  # Como se va a nombrar el objeto de la instancia
        verbose_name_plural ='gastos adicionales' # Como se nombra el modelo



# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
#   configuracion.moneda()   ---> devuelve la moneda en la que se trabaja
#
class medioDeCompra(models.Model):
    Nombre = models.CharField(max_length=200, null=True, blank=True)


    def clean(self): # Metodo para verificar algun  campo antes de guardar.
        super().clean()

    def __str__(self): # Como se muestra el objeto en una relacion foranea
        return self.Nombre
    
    class Meta: # Metodo para nombrar el modelo
        verbose_name = 'medio de compra'  # Como se va a nombrar el objeto de la instancia
        verbose_name_plural ='Medios de compra' # Como se nombra el modelo
  
# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
#   configuracion.moneda()   ---> devuelve la moneda en la que se trabaja
#
class medioDePago(models.Model):
    Nombre = models.CharField(max_length=200, null=True, blank=True)

    def clean(self): # Metodo para verificar algun  campo antes de guardar.
        super().clean()

    def __str__(self): # Como se muestra el objeto en una relacion foranea
        return self.Nombre
    
    class Meta: # Metodo para nombrar el modelo
        verbose_name = 'medio de pago'  # Como se va a nombrar el objeto de la instancia
        verbose_name_plural ='Medios de pago' # Como se nombra el modelo


# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
#   configuracion.moneda()   ---> devuelve la moneda en la que se trabaja
#
class rol(models.Model):
    Nombre = models.CharField(max_length=200, null=True, blank=True)

    def clean(self): # Metodo para verificar algun  campo antes de guardar.
        super().clean()

    def __str__(self): # Como se muestra el objeto en una relacion foranea
        return self.Nombre
    
    class Meta: # Metodo para nombrar el modelo
        verbose_name = 'rol'  # Como se va a nombrar el objeto de la instancia
        verbose_name_plural ='Roles de usuario' # Como se nombra el modelo

# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
#   configuracion.moneda()   ---> devuelve la moneda en la que se trabaja
#

class usuarioCustom(models.Model):
    Usuario = models.OneToOneField(User, on_delete=models.CASCADE,unique=True,blank=False,null=False)
    Rol = models.ForeignKey(rol,models.CASCADE,default=1,blank=False,null=False)
    Deposito = models.ForeignKey(deposito,on_delete=models.SET_NULL,null=True,blank=True)

    def clean(self): # Metodo para verificar algun  campo antes de guardar.
        super().clean()

    def __str__(self): # Como se muestra el objeto en una relacion foranea
        return f'{self.Usuario} (Rol: {self.Rol} Deposito asignado: {self.Deposito})'
    
    class Meta: # Metodo para nombrar el modelo
        verbose_name = 'asignacion'  # Como se va a nombrar el objeto de la instancia
        verbose_name_plural ='Asignacion Deposito' # Como se nombra el modelo
