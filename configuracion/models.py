# -----------------------------------------------------------------------------
# Project Adema
# Desarrolladores : Zoe Sacks / Kevin Turkienich
#
#
# Importacion de modulos
from django.db import models
from configuracion.listas import Monedas
from django.contrib.auth.models import User

REGIRREGU = [
    ("Regular", "Regular"),
    ("Irregular", "Irregular"),
]

ALIMENTACION = [
    ("Saludable", "Saludable"),
    ("No saludable", "No saludable"),
    ("Variado", "Variado"),
]

HIDRATACION = [
    ("Nada", "Nada"),
    ("Menos de 2lt", "Menos de 2lt"),
    ("Más de 2lt", "Más de 2lt"),
]

SINOOCA = [
    ("Sí", "Sí"),
    ("No", "No"),
    ("Ocasionalmente", "Ocasionalmente"),
]

TIEMPOS = [
    ("No", "No"),
    ("Una vez por semana", "Una vez por semana"),
    ("Cada 15 días", "Cada 15 días"),
    ("Una vez al mes", "Una vez al mes"),
]



LESIONES = [
    ("Mejilla derecha", "Mejilla derecha"),
    ("Mejilla izquierda", "Mejilla izquierda"),
    ("Menton", "Menton"),
    ("Nariz", "Nariz"),
    ("Frente", "Frente"),
]



# -----------------------------------------------------------------------------
# Modelado de datos
# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
# cliente.pedidos()    ---> Devuelve la cantidad de pedidos engregados
# cliente.cuenta_corriente()   ---> Devuelve el monto de la suma de los pagos a proveedores en c.c. menos los pagos en c.c.
class cliente(models.Model):
    NumeroCliente= models.AutoField(primary_key=True)
    NombreApellido=models.CharField(max_length=120,null=False,blank=False)
    Telefono =models.CharField(max_length=15,null=True,blank=True)
    ocupacion = models.CharField(max_length=15,null=True,blank=True)

    def __str__(self): # Como se muestra el objeto en una relacion foranea
        return self.NombreApellido

    class Meta:
        verbose_name = 'cliente'  # Como se va a nombrar el objeto de la instancia
        verbose_name_plural ='Clientes'  # Como se nombra el modelo


class DatosClinicos(models.Model):
    cliente = models.ForeignKey(cliente, on_delete=models.CASCADE)
    alergias = models.BooleanField(default=False)
    cuales_alergias = models.CharField(max_length=255, blank=True, null=True)
    medicaciones = models.CharField(max_length=255, blank=True, null=True)

    marcapasos = models.BooleanField(default=False)
    presion_arterial = models.BooleanField(default=False)
    presion_arterial_medicacion = models.CharField(max_length=255, blank=True, null=True)
    diabetes = models.BooleanField(default=False)
    diabetes_medicacion = models.CharField(max_length=255, blank=True, null=True)
    colesterol = models.BooleanField(default=False)
    colesterol_medicacion = models.CharField(max_length=255, blank=True, null=True)
    estres = models.BooleanField(default=False)
    estres_medicacion = models.CharField(max_length=255, blank=True, null=True)
    depresion = models.BooleanField(default=False)
    depresion_medicacion = models.CharField(max_length=255, blank=True, null=True)
    ansiedad = models.BooleanField(default=False)
    ansiedad_medicacion = models.CharField(max_length=255, blank=True, null=True)
    insomnio = models.BooleanField(default=False)
    insomnio_medicacion = models.CharField(max_length=255, blank=True, null=True)
    hiper_hipo_tiroidismo = models.BooleanField(default=False)
    hiper_hipo_tiroidismo_medicacion = models.CharField(max_length=255, blank=True, null=True)
    
    horas_descanso = models.CharField(max_length=255, blank=True, null=True)
    ciclo_menstrual = models.CharField(max_length=255, choices=REGIRREGU, blank=True, null=True)

    infecciones_infectocontagiosas = models.BooleanField(default=False)
    infecciones_infectocontagiosas_cual = models.CharField(max_length=255, blank=True, null=True)

    celiaquia = models.BooleanField(default=False)
    colon_irritable = models.BooleanField(default=False)
    intolerancia_gastrica = models.BooleanField(default=False)
    gastritis = models.BooleanField(default=False)
    intolerancia_lactosa = models.BooleanField(default=False)
    asma = models.BooleanField(default=False)
    broncoespasmo = models.BooleanField(default=False)
    epoc = models.BooleanField(default=False)

    anticonceptivos = models.BooleanField(default=False)
    hormonas = models.BooleanField(default=False)
    anticoagulantes = models.BooleanField(default=False)
    analgesicos = models.BooleanField(default=False)
    corticoides = models.BooleanField(default=False)
    complejo_vitaminico = models.BooleanField(default=False)

    def __str__(self): # Como se muestra el objeto en una relacion foranea
        return self.cliente.NombreApellido

    class Meta:
        verbose_name = 'datos clinicos'  # Como se va a nombrar el objeto de la instancia
        verbose_name_plural ='datos clinicos' 

class HabitosDiarios(models.Model):
    cliente = models.ForeignKey(cliente, on_delete=models.CASCADE)    

    alimentacion = models.CharField(max_length=255, choices=ALIMENTACION, blank=True, null=True)
    hidratacion = models.CharField(max_length=255, choices=HIDRATACION, blank=True, null=True)
    alcohol = models.CharField(max_length=255, choices=SINOOCA, blank=True, null=True)
    fuma = models.CharField(max_length=255, choices=SINOOCA, blank=True, null=True)
    cuantos_cigarrillos = models.PositiveIntegerField(blank=True, null=True)
    actividad_fisica = models.BooleanField(default=False)
    cuantos_dias_actividad_fisica = models.PositiveIntegerField(blank=True, null=True)


class CuidadosDeLaPiel(models.Model):
    cliente = models.ForeignKey(cliente, on_delete=models.CASCADE)  
    se_higieniza_habitualmente = models.BooleanField(default=False)
    se_exfolia = models.CharField(max_length=255, choices=TIEMPOS, blank=True, null=True)
    usa_maquillaje = models.BooleanField(max_length=255, choices=SINOOCA, blank=True, null=True)
    utiliza_cremas = models.BooleanField(default=False)
    cuales_cremas = models.CharField(max_length=255, blank=True, null=True)
    protector_solar = models.BooleanField(default=False)




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
