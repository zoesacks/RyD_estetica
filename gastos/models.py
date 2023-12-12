from django.db import models

class CategoriaGasto(models.Model):
    descripcion = models.CharField(max_length=255)
    
    def __str__(self):
        return f'{self.descripcion}'
    
    class Meta:
        verbose_name = 'categoria de gasto'
        verbose_name_plural ='Categorias de gastos'    

class gasto(models.Model):

    descripcion = models.CharField(max_length=255,unique=True)
    categoria = models.ForeignKey(CategoriaGasto, on_delete=models.PROTECT)
    total = models.DecimalField(max_digits=20, decimal_places=2)
    periodo = models.DateField()

    def __str__(self):
        return f'Motivo: {self.descripcion}. Monto: ${self.total}, por {self.periodo}'
    
    class Meta:
        verbose_name = 'gasto'
        verbose_name_plural ='Gastos' 


