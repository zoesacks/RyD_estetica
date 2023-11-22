from django.contrib import admin
from configuracion.models import categoria,proveedor,cliente
from inventario.models import producto
from django.contrib.auth.models import User

@admin.action(description="Crear datos de ejemplo")
def CrearDataEjemplo(modeladmin, request, queryset):

    #------ CREACION DE DATOS DE EJEMPLO
    # CREACION DE CATEGORIAS

    COCINA = categoria.objects.create(Descripcion='ALMACEN',)
    BEBIDAS_SIN_ALCOHOL = categoria.objects.create(Descripcion='BEBIDAS SIN ALCOHOL',)
    BEBIDAS_CON_ALCOHOL = categoria.objects.create(Descripcion='BEBIDAS CON ALCOHOL',)
    LIMPIEZA = categoria.objects.create(Descripcion='LIMPIEZA',)
    CARNICERIA = categoria.objects.create(Descripcion='CARNICERIA',)
    PANADERIA = categoria.objects.create(Descripcion='PANADERIA',)

    # Creacion de clientes
    CLIENTE_1 = cliente.objects.create(NombreApellido='Juan Perez', Direccion='Trunvirato 123, buenos aires',Telefono='+54 11 1234 5678')
    CLIENTE_2 = cliente.objects.create(NombreApellido='Jeremias Jera' ,Direccion='Zumbique 123, buenos aires',Telefono='+54 11 1234 5678')
    CLIENTE_3 = cliente.objects.create(NombreApellido='Andrea Palmito',Direccion='Esmeraldas 123, buenos aires',Telefono='+54 11 1234 5678')

    # Creacion de proveedores
    PROVEEDOR_1 = proveedor.objects.create(Empresa='VyA Concentrados', NombreApellido='David',Direccion='Trunvirato 123, buenos aires',Telefono='+54 11 1234 5678')
    PROVEEDOR_2 = proveedor.objects.create(Empresa='Tienda el Imbatible', NombreApellido='Kevin',Direccion='Zumbique 123, buenos aires',Telefono='+54 11 1234 5678')
    PROVEEDOR_3 = proveedor.objects.create(Empresa='Bella Maga', NombreApellido='Lucia',Direccion='Esmeraldas 123, buenos aires',Telefono='+54 11 1234 5678')

    # Crecion de productos
    producto.objects.create(
        Codigo='001', 
        Nombre='Harina para pan', 
        Descripcion='Bolsa',
        Proveedor=PROVEEDOR_1,
        Categoria=COCINA,
        Cantidad=5,
        UnidadMedida="Kilos",
        PrecioCosto=600,
        Rentabilidad=20,
        Stock=25,
    )

    producto.objects.create(
        Codigo='002', 
        Nombre='Fernet', 
        Descripcion='Branca',
        Proveedor=PROVEEDOR_2,
        Categoria=BEBIDAS_CON_ALCOHOL,
        Cantidad=710,
        UnidadMedida="Mililitros",
        PrecioCosto=0,
        Rentabilidad=0,
        Stock=25,
    )

    producto.objects.create(
        Codigo='003', 
        Nombre='Gaseosa Cola', 
        Descripcion='Coca-cola',
        Proveedor=PROVEEDOR_3,
        Categoria=BEBIDAS_SIN_ALCOHOL,
        Cantidad=2.25,
        UnidadMedida="Litros",
        PrecioCosto=300,
        Rentabilidad=30,
        Stock=250,
    )

    producto.objects.create(
        Codigo='005', 
        Nombre='Gaseosa Naranja', 
        Descripcion='Fanta',
        Proveedor=PROVEEDOR_3,
        Categoria=BEBIDAS_SIN_ALCOHOL,
        Cantidad=2.25,
        UnidadMedida="Litros",
        PrecioCosto=300,
        Rentabilidad=30,
        Stock=250,
    )

    producto.objects.create(
        Codigo='006', 
        Nombre='Vino tinto', 
        Descripcion='Almamora',
        Proveedor=PROVEEDOR_1,
        Categoria=BEBIDAS_CON_ALCOHOL,
        Cantidad=1.25,
        UnidadMedida="Litros",
        PrecioCosto=1125,
        Rentabilidad=40,
        Stock=62,
    )

    producto.objects.create(
        Codigo='007', 
        Nombre='Manteca', 
        Descripcion='La serenisima',
        Proveedor=PROVEEDOR_1,
        Categoria=COCINA,
        Cantidad=500,
        UnidadMedida="Gramos",
        PrecioCosto=35,
        Rentabilidad=15,
        Stock=2,
    )

    producto.objects.create(
        Codigo='008', 
        Nombre='Huevos', 
        Descripcion='Supermercado',
        Proveedor=PROVEEDOR_1,
        Categoria=COCINA,
        Cantidad=6,
        UnidadMedida="Unidades",
        PrecioCosto=205,
        Rentabilidad=15,
        Stock=200,
    )

    producto.objects.create(
        Codigo='009', 
        Nombre='Aceite', 
        Descripcion='Cañuelas',
        Proveedor=PROVEEDOR_1,
        Categoria=COCINA,
        Cantidad=2,
        UnidadMedida="Litros",
        PrecioCosto=350,
        Rentabilidad=15,
        Stock=25,
    )

    producto.objects.create(
        Codigo='010', 
        Nombre='Carne Picada', 
        Descripcion='Carniceria',
        Proveedor=PROVEEDOR_1,
        Categoria=CARNICERIA,
        Cantidad=2,
        UnidadMedida="Litros",
        PrecioCosto=350,
        Rentabilidad=15,
        Stock=25,
    )
