# -----------------------------------------------------------------------------
# Project Adema
# Desarrolladores : Zoe Sacks / Kevin Turkienich
#
#
# Importacion de modulos
from django.contrib import admin
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin
from configuracion.models import miEmpresa,deposito
from django.core.exceptions import ValidationError
# -----------------------------------------------------------------------------
# Modelado de vistas del administrador
# -----------------------------------------------------------------------------
# Importacion de modelos
from .models import producto, movimientoInventarios, Compra, DetalleCompra, Venta, DetalleVenta
from configuracion.models import proveedor,categoria




# -----------------------------------------------------------------------------
# Configuracion de importacion de productos

class productoResource(resources.ModelResource):
        Codigo = fields.Field(attribute='Codigo',  column_name='Codigo')
        Nombre = fields.Field(attribute='Nombre',  column_name='Nombre')
        Descripcion = fields.Field(attribute='Descripcion',column_name='Descripcion')
        InformacionAdicional = fields.Field(attribute='Descripcion',column_name='Descripcion')
        Proveedor = fields.Field(attribute='Proveedor', column_name='Proveedor', widget=widgets.ForeignKeyWidget(proveedor, 'Empresa')) # Acceso al campo 'codigo' en codigoFinanciero
        Categoria = fields.Field(attribute='Categoria', column_name='Categoria', widget=widgets.ForeignKeyWidget(categoria, 'Descripcion'))
        Cantidad = fields.Field(attribute='Cantidad',  column_name='Cantidad')
        Rentabilidad = fields.Field(attribute='Rentabilidad',  column_name='Rentabilidad')
        PrecioCosto = fields.Field(attribute='PrecioCosto',  column_name='PrecioCosto')

        class Meta:
                model = producto

        def before_import_row(self, row, **kwargs):
                # Realiza la validación antes de importar la fila
                if not row.get('Codigo'):
                        raise ValidationError("La columna 'codigo' no puede estar vacío.")
                if not row.get('Nombre'):
                        raise ValidationError("La columna 'Nombre' no puede estar vacío.")
                if not row.get('Cantidad'):
                        raise ValidationError("La columna 'proveedor' no puede estar vacío.")
                '''
                if not row.get('Rentabilidad'):
                        raise ValidationError("La columna 'Rentabilidad' no puede estar vacío.")
                '''
                if not row.get('PrecioCosto'):
                        raise ValidationError("La columna 'PrecioCosto' no puede estar vacío.")



# Configuraciones de vistas
# -----------------------------------------------------------------------------
# Vista de producto (Inventario de productos)
# 
@admin.register(producto)
class productoAdmin(ImportExportModelAdmin):
    resource_class = productoResource
    list_display = ('Codigo','nombre','Categoria','Proveedor','ultimo_costo','UltimaModificacion')
    list_display_links = ('Codigo','nombre',)
    list_filter=('Categoria',)
    search_fields = ('Codigo','Descripcion',)
    exclude=('Usuario','CostoDolar','HabilitarVenta', 'Rentabilidad', 'Stock',)
    list_per_page = 20  
    
    def ultimo_costo(self,obj):
        moneda = miEmpresa.objects.first()
        total = obj.PrecioCosto
        return str(moneda.Moneda) + str(" {:,.2f}".format(total))
    
    def precio_venta(self, obj):
        moneda = miEmpresa.objects.first()
        total = obj.precio_unitario()
        return str(moneda.Moneda) + str(" {:,.2f}".format(total))

    def nombre(self,obj):
        texto  = f'{obj.Nombre} x{obj.Cantidad} {obj.UnidadMedida}'
        return texto

    nombre.admin_order_field = 'Nombre'

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            # Filtrar productos con stock negativo
            if search_term_as_int == -1:
                queryset = queryset.filter(stock__lt=0)
        except ValueError:
            pass
        return queryset, use_distinct

class DetalleCompraInline(admin.StackedInline):
    model = DetalleCompra
    extra = 1

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ( 'fecha', 'mostrar_detalles', 'Total')
    inlines = [
        DetalleCompraInline,
    ]

    def mostrar_detalles(self, obj):
        detalles_venta = obj.detallecompra_set.all()
        detalles = ", ".join(
            f"{detalle.producto.Nombre} x {detalle.cantidad}"
            for detalle in detalles_venta
        )
        return detalles

    def Total(self, obj):
        detalles_venta = obj.detallecompra_set.all()  # Obtén todos los detalles de la venta
        costo_total = sum(detalle.cantidad * detalle.costo_unidad for detalle in detalles_venta)
        return str("$ {:,.2f}".format(costo_total))


class DetalleVentaInline(admin.StackedInline):
    model = DetalleVenta
    extra = 1

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'fecha', 'mostrar_detalles', 'Total')
    inlines = [
        DetalleVentaInline,
    ]

    def mostrar_detalles(self, obj):
        detalles_venta = obj.detalleventa_set.all()
        detalles = ", ".join(
            f"{detalle.producto.Nombre} x {detalle.cantidad}"
            for detalle in detalles_venta
        )
        return detalles

    def Total(self, obj):
        detalles_venta = obj.detalleventa_set.all()  # Obtén todos los detalles de la venta
        costo_total = sum(detalle.cantidad * detalle.costo_unidad for detalle in detalles_venta)
        return str("$ {:,.2f}".format(costo_total))


# -----------------------------------------------------------------------------
# Vista de movimientos de inventarios (Inventario de productos)
# 
@admin.register(movimientoInventarios)
class movimientoInventariosAdmin(ImportExportModelAdmin):
    list_display = ('fecha','Producto','DepositoSalida','DepositoEntrada' ,'Cantidad','Usuario',)
    list_display_links = ('Producto',)
    list_filter=('Producto','DepositoSalida','DepositoEntrada','Usuario','Estado',)
    search_fields = ('Producto','DepositoSalida','DepositoEntrada')
    exclude=('Usuario','Estado')
    list_per_page = 20

    def fecha(self,obj):
        return obj.UltimaModificacion

    def save_model(self, request, obj, form, change):
        if not obj.Usuario:
            obj.Usuario = request.user.username
        super().save_model(request, obj, form, change)