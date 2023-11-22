from django.http import HttpResponse
from reportlab.lib.pagesizes import letter,legal
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from django.contrib import admin, messages
from configuracion.models import miEmpresa
import os
import locale
from django.core.files.storage import default_storage

from cocina.models import gastosAdicionalesReceta,productoReceta,subRecetaReceta

@admin.action(description="Descargar Receta")
def generar_presupuesto(modeladmin, request, queryset):

    #Validacion para que seleccione solo 1 queryset
    if len(queryset) != 1:
        messages.error(request, "Seleccione solo un pedido para generar el informe.")
        return
      
    #Capturo la ruta actual para la ruta del logo
    current_directory = os.getcwd()

    logo_path = os.path.join(current_directory, 'static/logo.png')

    # Obtener el primer pedido seleccionado
    pedido = queryset[0]
    
    config = miEmpresa.objects.first()


    nombre_empresa = config.Empresa
    direccion_empresa = config.Direccion
    telefono_empresa = config.Telefono
    email_empresa = config.Horarios
    
    # Establecer el idioma en español
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    # Obtener el primer pedido seleccionado
    pedido = queryset[0]  
    #Crear el objeto
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="presupuesto_{pedido.Nombre}.pdf"'
    # Crear el lienzo PDF
    p = canvas.Canvas(response, pagesize=legal)

    # Agregar contenido al lienzo
    y = 950  # Posición vertical inicial
    x = 50
    
    # Verificar si el archivo de imagen del logo existe
    if logo_path:
        # Tamaño y posición del logo
        logo_width = 150  # Ancho del logo
        logo_height = 150 # Alto del logo
        logo_x = 410  # Posición horizontal del logo
        logo_y = 820  # Posición vertical del logo

        # Agregar el logo al lienzo PDF
        logo_image = ImageReader(logo_path)
        p.drawImage(logo_image, logo_x, logo_y, width=logo_width, height=logo_height)
    
 
    # Titulo del reporte
    p.setFont("Helvetica-Bold", 18)  
    p.drawString(x, y, nombre_empresa)
    y -= 20

    p.setFont("Helvetica", 12)  # Fuente normal
    p.drawString(x, y, direccion_empresa)
    y -= 15

    p.drawString(x, y, telefono_empresa)
    y -= 15

    p.drawString(x, y, email_empresa)
    y -= 15

    # Seccion de cliente - Titulo
    p.setFont("Helvetica-Bold", 12)  # Fuente en negrita y tamaño 14
    p.drawString(x, y, f"")
    y -= 20

    # Bloque entrega
    p.setFillColorRGB(0, 0, 0)  # Color de texto negro
    p.setFont("Helvetica-Bold", 12)  # Fuente en negrita y tamaño 14
    p.drawString(x, y, f"DATOS DE LA RECETA")
    y -= 20

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Receta #: ")
    p.setFont("Helvetica", 10)  # Fuente normal
    codigo_str = str(pedido.id)
    p.drawString(100, y, codigo_str.zfill(4))
    y -= 15

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Costos totales: $ ")
    p.setFont("Helvetica", 10)  # Fuente normal
    Calculo = pedido.costo_receta()
    codigo_str = str("{:,.2f}".format(Calculo))
    p.drawString(140, y, codigo_str)
    y -= 15

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Rentabilidad: %")
    p.setFont("Helvetica", 10)  # Fuente normal
    Calculo = pedido.Rentabilidad
    codigo_str = str("{:,.2f}".format(Calculo))
    p.drawString(140, y, codigo_str)
    y -= 15

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Precio venta: $ ")
    p.setFont("Helvetica", 10)  # Fuente normal
    codigo_str = str("{:,.2f}".format(pedido.precio_unitario()))
    p.drawString(140, y, codigo_str)
    y -= 25


    # Obtener los gastos adicionales de la receta
    gastos_adicionales = gastosAdicionalesReceta.objects.filter(Receta=pedido)
    
    cant_gastos = gastosAdicionalesReceta.objects.filter(Receta=pedido).count()

    if gastos_adicionales:
        p.setFont("Helvetica-Bold", 10)  # Fuente en negrita y tamaño 14
        p.drawString(x, y, f"COSTOS ADICIONALES:")
        y -= 20
        for gasto in gastos_adicionales:
            p.setFont("Helvetica", 10)  # Fuente en negrita
            p.drawString(x, y, f"{gasto.Adicional}: $ {gasto.Importe:,.2f}")
            y -= 20


    if cant_gastos <= 1:
        y = 725
    elif cant_gastos <= 3:
        y = 700
    else:
        y = 680

    insumos = productoReceta.objects.filter(Receta=pedido)
    if insumos:
        p.setFont("Helvetica-Bold", 10)  # Fuente en negrita y tamaño 14
        p.drawString(x, y, f"ARTICULOS INCLUIDOS:")
        y -= 20
        for insumo in insumos:
            p.setFont("Helvetica", 10)  # Fuente en negrita
            p.drawString(x, y, f"{insumo.Producto.Nombre} {insumo.Producto.Descripcion}")
            y -= 15
            p.drawString(x, y, f"Cant: {insumo.Cantidad} {insumo.MedidaUso} Subtotal : $ {round(insumo.subtotal(),2):,.2f}")
            y -= 20

    y = 725

    subrecetas = subRecetaReceta.objects.filter(Receta=pedido)
    if subrecetas:
        p.setFont("Helvetica-Bold", 10)  # Fuente en negrita y tamaño 14
        p.drawString(340, y, f"SUBRECETAS INCLUIDAS:")
        y -= 20
        for insumo in subrecetas:
            p.setFont("Helvetica", 10)  # Fuente en negrita
            p.drawString(340, y, f"{insumo.SubReceta.Nombre}")
            y -= 15
            total_subreceta = float(insumo.SubReceta.costo_porcion()) * float(insumo.Cantidad)

            p.drawString(340, y, f"Porciones: {insumo.Cantidad}  Subtotal : $ {round(total_subreceta,2):,.2f}")
            y -= 20

    y = 60
    p.setFont("Helvetica-Bold", 14)
    p.drawString(280, y, "Precio total Presupuestado: ")
    p.setFont("Helvetica", 13)  # Fuente normal
    p.drawString(480, y,  f'$ {pedido.precio_unitario():,.2f}')
    y -= 40

    p.save()

    return response
