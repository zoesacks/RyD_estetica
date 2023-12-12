from django.shortcuts import render
from django.views import View
from .models import orden

class PedidoDetailView(View):
    template_name = 'pedido_detalle.html'  # Crea un template HTML para mostrar los detalles del pedido

    def get(self, request, pedido_id):
        pedido = orden.objects.get(pk=pedido_id)  # Obtén el pedido según su ID

        context = {
            'pedido': pedido,  # Pasa el pedido al contexto para mostrar en el template
        }

        return render(request, self.template_name, context)
    



