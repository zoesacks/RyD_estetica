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
from .models import orden, productoOrden, receta,productoReceta, gastosAdicionalesReceta
from configuracion.models import miEmpresa
from .Reporte import generar_presupuesto
from .Autorizaciones import confirmar_orden,terminar_orden


# -----------------------------------------------------------------------------
#   Administradores de vistas inlines
#
class productoOrdenInline(admin.StackedInline):
    model = productoOrden
    extra = 1
    fields = ('Producto',)
    search_fields = ('Producto',)

class productoRecetaInline(admin.StackedInline):
    model = productoReceta
    extra = 1
    fields = ('Producto', 'Cantidad',)
    autocomplete_fields = ('Producto',)

'''
class productoSubRecetaInline(admin.TabularInline):
    model = productoSubReceta
    extra = 1
    fields = ('Producto', 'Cantidad','MedidaUso',)
    autocomplete_fields = ('Producto',)
'''

class gastosAdicionalesRecetaInline(admin.StackedInline):
    model = gastosAdicionalesReceta
    extra = 1
    fields = ('Adicional', 'Importe',)

'''
class subRecetaRecetaInline(admin.TabularInline):
    model = subRecetaReceta
    extra = 1
    fields = ('SubReceta', 'Cantidad',)
'''

# -----------------------------------------------------------------------------
#   Administradores de vistas
#
@admin.register(orden)
class ordenAdmin(admin.ModelAdmin):

    list_display = ('orden','estado', 'Cliente','Fecha_de_la_sesion','Costo', 'precio_final', 'ganancia',)
    list_display_links = ('orden',)
    readonly_fields = ('Costo', 'detalle_final')
    list_filter = ('Cliente','FechaOrden',)
    exclude = ('Usuario','Estado','TotalOrden')
    list_per_page = 25

    actions=[terminar_orden,]
 
    inlines = [
        productoOrdenInline,
    ]

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return [productoOrdenInline(self.model, self.admin_site)]
        
        elif obj.Estado == "Pendiente":
            return [productoOrdenInline(self.model, self.admin_site)]
        
        return []
    
    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return ['Costo', 'detalle_final']
        
        elif obj.Estado != "Pendiente":
            return ['Cliente', 'FechaOrden', 'FechaEntrega', 'Comentarios', 'TotalOrden', 'costoFinal', 'detalle_final'] # Ajusta estos nombres según tus campos
        
        else:
            return ['Costo', 'detalle_final']

    def Fecha_de_la_sesion(self, obj):
        return obj.FechaEntrega
        
    def Costo(self,obj):
        return str(" ${:,.2f}".format(obj.total_costo()))

    def ganancia(self,obj):
        return str(" ${:,.2f}".format(float(obj.costoFinal) - float(obj.total_costo())))
    
    def precio_final(self, obj):
        return str(" ${:,.2f}".format(obj.costoFinal))

    def orden(self,obj):
        presup = obj.pk
        return f'# {presup}'
    
    def total(self, obj):
        return str(" {:,.2f}".format(obj.total_costo()))

    def estado(self,obj):

        if obj.Estado=="Pendiente":
            return "🔴 Pendiente"
        elif obj.Estado == "Aceptado":
            return "🟠 En curso"
        else:
            return "🟢 Terminado"

        
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
@admin.register(receta)
class recetaAdmin(admin.ModelAdmin):

    list_display = ('Nombre','Categoria','costo_del_tratamiento',)
    list_display_links = ('Nombre',)
    list_filter = ('Nombre','Estado',)
    readonly_fields = ('Comentarios', )
    exclude = ('Categoria', 'costo_del_tratamiento','Usuario','Estado','GeneraComanda', 'MedidaUso','Rentabilidad', 'precio_final', 'ganancia', 'costo_final')
    list_per_page = 25
    actions = [terminar_orden]
    
    inlines = [
        productoRecetaInline,
        gastosAdicionalesRecetaInline,
        #subRecetaRecetaInline,
    ]

    def ganancia(self,obj):
        return str(" ${:,.2f}".format(float(obj.costo_final) - obj.costo_receta()))

    def costo_del_tratamiento(self,obj):
        return str(" ${:,.2f}".format(obj.costo_receta()))
    
    def receta(self,obj):
        texto = obj.pk
        return f'# {texto}'
    
    def precio_final(self, obj):
        return str(" ${:,.2f}".format(obj.costo_final))
    
    def ultima_actualizacion(self, obj): 
        hora_buenos_aires = pytz.timezone('America/Argentina/Buenos_aires')
        fecha_hora = obj.UltimaModificacion.astimezone(hora_buenos_aires)
        formateo = fecha_hora.strftime("%H:%M %d/%m/%Y")

        formateo = "📆 " +formateo
        return formateo


'''
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
'''