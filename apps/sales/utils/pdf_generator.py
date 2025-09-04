"""
Generador de PDFs para facturas.
"""
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from apps.sales.models import Factura

def generar_factura_pdf(factura: Factura) -> HttpResponse:
   """
   Genera un PDF para una factura específica.
   
   Args:
       factura (Factura): La factura para generar PDF
       
   Returns:
       HttpResponse: Respuesta HTTP con el PDF
   """
   response = HttpResponse(content_type='application/pdf')
   response['Content-Disposition'] = f'attachment; filename="Factura_{factura.id}.pdf"'

   p = canvas.Canvas(response, pagesize=letter)
   width, height = letter
   y = height - 40

   # Cabecera
   p.setFont("Helvetica-Bold", 16)
   prefijo = factura.configuracion.prefijo if factura.configuracion else ""
   p.drawCentredString(width / 2, y, f"Factura {prefijo}{factura.id}")
   y -= 30

   # Datos básicos
   p.setFont("Helvetica", 12)
   p.drawString(50, y, f"Fecha: {factura.fecha_emision} {factura.hora_emision.strftime('%H:%M')}")
   y -= 20
   p.drawString(50, y, f"Cliente: {factura.cliente}")
   y -= 20
   p.drawString(50, y, f"Empleado: {factura.empleado}")
   y -= 20
   p.drawString(50, y, f"Método de Pago: {factura.tipo_pago}")
   y -= 40

   # Encabezados de tabla
   p.setFont("Helvetica-Bold", 11)
   p.drawString(50, y, "Producto")
   p.drawString(250, y, "Cantidad")
   p.drawString(350, y, "Precio Unit.")
   p.drawString(450, y, "Total")
   y -= 20

   p.setFont("Helvetica", 10)
   for item in factura.detalles.all():
       if y < 100:  # Salto de página si estamos muy abajo
           p.showPage()
           y = height - 40
       total_item = item.precio_unitario * item.cantidad
       p.drawString(50, y, str(item.producto.nombre))
       p.drawString(250, y, str(item.cantidad))
       p.drawString(350, y, f"${item.precio_unitario:.2f}")
       p.drawString(450, y, f"${total_item:.2f}")
       y -= 18

   # Totales
   y -= 30
   p.setFont("Helvetica-Bold", 11)
   p.drawString(50, y, f"Subtotal: ${factura.subtotal:.2f}")
   y -= 18
   p.drawString(50, y, f"Base Gravable: ${factura.base_gravable:.2f}")
   y -= 18
   impuesto = factura.impuesto_calculado
   p.drawString(50, y, f"Impuesto ({factura.tipo_impuesto.nombre}): ${impuesto:.2f}")
   y -= 18
   p.drawString(50, y, f"Propina: ${factura.propina:.2f}")
   y -= 18
   p.drawString(50, y, f"Total: ${factura.total:.2f}")
   y -= 18
   p.drawString(50, y, f"Recibido: ${factura.recibido:.2f}")
   y -= 18
   cambio = factura.cambio
   p.drawString(50, y, f"Cambio: ${cambio:.2f}")

   p.showPage()
   p.save()
   return response
