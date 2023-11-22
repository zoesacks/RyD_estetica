# -----------------------------------------------------------------------------
# Project Adema
# Desarrolladores : Zoe Sacks / Kevin Turkienich
#
# -----------------------------------------------------------------------------
# Modelado de vistas del administrador
# -----------------------------------------------------------------------------
# Importacion de modelos
from django.contrib import admin
import pytz
from .models import orden, productoOrden, receta,productoReceta,subReceta,productoSubReceta,gastosAdicionalesReceta,subRecetaReceta
from configuracion.models import miEmpresa
from .Reporte import generar_presupuesto
from .Autorizaciones import confirmar_orden,terminar_orden
# -----------------------------------------------------------------------------
#   Administradores de vistas inlines
#
class productoOrdenInline(admin.TabularInline):
    model = productoOrden
    extra = 1
    fields = ('Producto', 'Cantidad')
    search_fields = ('Producto',)

class productoRecetaInline(admin.TabularInline):
    model = productoReceta
    extra = 1
    fields = ('Producto', 'Cantidad','MedidaUso')
    autocomplete_fields = ('Producto',)

class productoSubRecetaInline(admin.TabularInline):
    model = productoSubReceta
    extra = 1
    fields = ('Producto', 'Cantidad','MedidaUso',)
    autocomplete_fields = ('Producto',)


class gastosAdicionalesRecetaInline(admin.TabularInline):
    model = gastosAdicionalesReceta
    extra = 1
    fields = ('Adicional', 'Importe',)


class subRecetaRecetaInline(admin.TabularInline):
    model = subRecetaReceta
    extra = 1
    fields = ('SubReceta', 'Cantidad',)


# -----------------------------------------------------------------------------
#   Administradores de vistas
#
@admin.register(orden)
class ordenAdmin(admin.ModelAdmin):

    list_display = ('orden','estado','Cliente','FechaEntrega','total')
    list_display_links = ('estado','Cliente',)
    #readonly_fields = ('Stock',)
    list_filter = ('Estado','Cliente','FechaOrden',)
    exclude = ('Usuario','Estado','TotalOrden')
    list_per_page = 25
    actions = [confirmar_orden,terminar_orden]
 
    inlines = [
        productoOrdenInline,
        #IngredienteRecetaInline,
    ]

    def orden(self,obj):
        presup = obj.pk
        return f'# {presup}'
    
    def total(self, obj):
        moneda = miEmpresa.objects.first()

        if obj.Estado == "Pendiente":
            print(obj.Estado)
            return str(moneda.Moneda) + str(" {:,.2f}".format(obj.total_costo()))

        else:
            print(obj.Estado)
            return str(moneda.Moneda) + str(" {:,.2f}".format(obj.TotalOrden))

    def estado(self,obj):

        if obj.Estado=="Pendiente":
            return "🔴 Pendiente"
        elif obj.Estado == "Aceptado":
            return "🟠 En curso"
        else:
            return "🟢 Entregado"
        
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if 'Pendiente' in request.GET:
            return queryset  # No aplicar ningún filtro si el filtro 'entregado' está activo
        else:
            return queryset
            r#eturn queryset.exclude(Estado='Entregado')


# -----------------------------------------------------------------------------
#   Administradores de vistas
#
@admin.register(subReceta)
class subRecetaAdmin(admin.ModelAdmin):

    list_display = ('subreceta','costo_porcion','costo_receta','ultima_actualizacion',)
    list_display_links = ('subreceta',)
    list_filter = ('Nombre','Estado',)
    exclude = ('Usuario','Estado',)
    list_per_page = 25


    inlines = [
        productoSubRecetaInline,
    ]

    def subreceta(self,obj):
        texto = f'{obj.Nombre}'
        return f'# {texto}'

    def costo_receta(self, obj):
        moneda = miEmpresa.objects.first()
        return str(moneda.Moneda) + str(" {:,.2f}".format(obj.costo_total()))
    
    def costo_porcion(self, obj):
        moneda = miEmpresa.objects.first()
        cadena = str(moneda.Moneda) + str(" {:,.2f}".format(obj.costo_porcion()))
        return cadena
    
    def ultima_actualizacion(self, obj): 
        hora_buenos_aires = pytz.timezone('America/Argentina/Buenos_aires')
        fecha_hora = obj.UltimaModificacion.astimezone(hora_buenos_aires)
        formateo = fecha_hora.strftime("%H:%M %d/%m/%Y")

        formateo = "📆 " +formateo
        return formateo

# -----------------------------------------------------------------------------
#   Administradores de vistas
#
@admin.register(receta)
class recetaAdmin(admin.ModelAdmin):

    list_display = ('Nombre','Categoria','costo_receta','rentabilidad','precio_unitario','ultima_actualizacion',)
    list_display_links = ('Nombre',)
    list_filter = ('Nombre','Estado',)
    exclude = ('Usuario','Estado','GeneraComanda')
    readonly_fields=('precio_unitario',)
    list_per_page = 25
    actions = [generar_presupuesto,]
    
    inlines = [
        gastosAdicionalesRecetaInline,
        productoRecetaInline,
        subRecetaRecetaInline,
    ]

    def rentabilidad(self,obj):
        return str("% {:,.2f}".format(obj.Rentabilidad))
    
    def receta(self,obj):
        texto = obj.pk
        return f'# {texto}'
    
    def costo_receta(self, obj):
        moneda = miEmpresa.objects.first()
        return str(moneda.Moneda) + str(" {:,.2f}".format(obj.costo_receta()))
    
    def precio_unitario(self, obj):
        moneda = miEmpresa.objects.first()
        return str(moneda.Moneda) + str(" {:,.2f}".format(obj.precio_unitario()))
    
    def ultima_actualizacion(self, obj): 
        hora_buenos_aires = pytz.timezone('America/Argentina/Buenos_aires')
        fecha_hora = obj.UltimaModificacion.astimezone(hora_buenos_aires)
        formateo = fecha_hora.strftime("%H:%M %d/%m/%Y")

        formateo = "📆 " +formateo
        return formateo


