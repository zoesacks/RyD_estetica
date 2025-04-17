from django.shortcuts import render
from .models import Servicio
def home(request):
    return render(request, 'home.html')

def servicios(request):
    servicios = Servicio.objects.all()
    context = {
        'servicios': servicios,
    }
    return render(request, 'servicios.html', context)

def sobre_nosotros(request):
    return render(request, 'sobre-nosotros.html')