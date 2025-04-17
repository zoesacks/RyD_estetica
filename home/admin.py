from django.contrib import admin
from .models import Servicio
# Register your models here.

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'duracion', 'precio')
    search_fields = ('titulo', 'categoria')
    list_filter = ('categoria',)

