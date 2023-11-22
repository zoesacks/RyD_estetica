from django.contrib import admin, messages

@admin.action(description="Confirmar sesion")
def confirmar_orden(modeladmin, request, queryset): 

    #Validacion para que seleccione solo 1 queryset
    if len(queryset) != 1:
        messages.error(request, "Solo se puede aceptar 1 orden a la vez.")
        return
    
    orden = queryset[0]

    if orden.Estado != "Pendiente":
        messages.error(request, "El pedido ya se encuentra confirmado.")
        return
    else:
        orden.Estado = "Aceptado"
        orden.TotalOrden = orden.total_costo()
        orden.save()
        return
    
@admin.action(description="Terminar sesion")
def terminar_orden(modeladmin, request, queryset): 

    #Validacion para que seleccione solo 1 queryset
    if len(queryset) != 1:
        messages.error(request, "Solo se puede terminar 1 orden a la vez.")
        return
    
    orden = queryset[0]

    if orden.Estado == "Aceptado":
        orden.Estado = "Entregado"
        orden.save()
        messages.error(request, "Pedido finalizado correctamente.")
        return
    else:
        messages.error(request, "El pedido no se encuentra en curso.")
        return