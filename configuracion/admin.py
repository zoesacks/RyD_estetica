# -----------------------------------------------------------------------------
# Project Adema
# Desarrolladores : Zoe Sacks / Kevin Turkienich
#
#
# Importacion de modulos
from django.contrib import admin
from .models import categoria
from import_export.admin import ImportExportModelAdmin
from configuracion.models import medioDeCompra,medioDePago,rol,usuarioCustom
# -----------------------------------------------------------------------------
# Modelado de vistas del administrador
# -----------------------------------------------------------------------------
# Importacion de modelos
from .models import cliente,proveedor,deposito,miEmpresa,gastosAdicionales
from .datosEjemplo import CrearDataEjemplo
# Nombre del sitio 
# -----------------------------------------------------------------------------
admin.site.site_header = "ADEMA"
admin.site.site_title = "ADEMA"


# Configuraciones de vistas
# -----------------------------------------------------------------------------
# Vista Depositos
# 
@admin.register(miEmpresa)
class miEmpresaAdmin(admin.ModelAdmin):
    list_display = ('Empresa','Moneda','Direccion','Telefono','Horarios')
    exclude =('Nombre',)
    actions = [CrearDataEjemplo,]

# -----------------------------------------------------------------------------
# Funciones del admin
# 
@admin.register(cliente)
class clienteAdmin(ImportExportModelAdmin):
    list_display = ('NumeroCliente','NombreApellido','Direccion','Email','Telefono',)
    list_filter = ('NumeroCliente','NombreApellido','Email','Telefono',)
    search_fields = ('NumeroCliente','NombreApellido','Email','Direccion',)


# -----------------------------------------------------------------------------
# Vista proveedor
# 
@admin.register(proveedor)
class proveedorAdmin(ImportExportModelAdmin):
    list_display = ('Empresa', 'NombreApellido','Direccion', 'Email','Telefono',)
    list_filter = ('Empresa', 'NombreApellido','Direccion', 'Email','Telefono',)
    search_fields = ('Empresa', 'NombreApellido','Direccion', 'Email','Telefono',)
    ordering = ('Empresa',)


# -----------------------------------------------------------------------------
# Vista Categoria
# 
@admin.register(categoria)
class categoriaAdmin(admin.ModelAdmin):
    list_display = ('Descripcion',)

# -----------------------------------------------------------------------------
# Vista Depositos
# 
@admin.register(deposito)
class depositoAdmin(admin.ModelAdmin):
    list_display = ('Nombre',)


# -----------------------------------------------------------------------------
# Vista Depositos
# 
@admin.register(gastosAdicionales)
class gastosAdicionalesAdmin(admin.ModelAdmin):
    list_display = ('Descripcion',)

# # -----------------------------------------------------------------------------
# # Vista Depositos
# # 
# @admin.register(medioDeCompra)
# class medioDeCompraAdmin(admin.ModelAdmin):
#     list_display = ('Nombre',)


# # -----------------------------------------------------------------------------
# # Vista Depositos
# # 
# @admin.register(medioDePago)
# class gastosAdicionalesAdmin(admin.ModelAdmin):
#     list_display = ('Nombre',)

# # -----------------------------------------------------------------------------
# # Vista Depositos
# # 
# @admin.register(rol)
# class rolAdmin(admin.ModelAdmin):
#     list_display = ('Nombre',)


# # -----------------------------------------------------------------------------
# # Vista Depositos
# # 
# @admin.register(usuarioCustom)
# class usuarioCustomAdmin(admin.ModelAdmin):
#     list_display = ('Usuario','Rol','Deposito')

