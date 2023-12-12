from django.contrib import admin
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin
from .models import gasto

# Register your models here.
@admin.register(gasto)
class gastoAdmin(ImportExportModelAdmin):
    list_display = ('categoria', 'descripcion', 'periodo',  'Total',)
    list_filter=('descripcion',)

    def Total(self, obj):
        return str(" ${:,.2f}".format(obj.total))
    

