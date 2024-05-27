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
from .models import cliente,proveedor,deposito,miEmpresa,gastosAdicionales, DatosClinicos, HabitosDiarios
from .datosEjemplo import CrearDataEjemplo
# Nombre del sitio 
# -----------------------------------------------------------------------------
admin.site.site_header = "ADEMA"
admin.site.site_title = "ADEMA"

class SesionInline(admin.StackedInline):
    from cocina.models import orden
    model = orden
    extra = 0
    readonly_fields = ['Cliente', 'FechaOrden', 'FechaEntrega', 'Comentarios', 'TotalOrden', 'costoFinal', 'detalle_final', 'diagnostico_final'] # Ajusta estos nombres según tus campos
    exclude = ['Usuario','Estado','TotalOrden']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(Estado="Entregado")

        return queryset

class DatosClinicosOrdenInline(admin.StackedInline):
    model = DatosClinicos
    max_num = 1


class HabitosDiariosOrdenInline(admin.StackedInline):
    model = HabitosDiarios
    max_num = 1


    

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
    list_display = ('NumeroCliente','NombreApellido',)
    list_filter = ('NumeroCliente','NombreApellido',)
    search_fields = ('NumeroCliente','NombreApellido',)
    inlines = [DatosClinicosOrdenInline,
               HabitosDiariosOrdenInline,
               SesionInline,]


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

