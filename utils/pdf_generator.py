from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os
import datetime
import sys

def ruta_recurso(rel_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, rel_path)
    return os.path.join(os.path.abspath("."), rel_path)

def generar_boleta_pdf(id_presupuesto, nombre, telefono, descripcion, cotizacion=None, estado="Pendiente", fecha_estado=None):
    file_name = f"presupuesto_{id_presupuesto}.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)
    width, height = A4
    mitad = height / 2

    def dibujar_boleta(y_offset, copia):
        # Logo
        logo_path = ruta_recurso("assets/BYT.png")
        logo_width = 80
        logo_height = 80
        logo_x = 50
        logo_y = y_offset - 80

        try:
            logo = ImageReader(logo_path)
            c.drawImage(logo, logo_x, logo_y, width=logo_width, height=logo_height, mask='auto')
        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")

        # Datos del local
        text_x = logo_x + logo_width + 10
        text_y = logo_y + logo_height - 5

        c.setFont("Helvetica", 10)
        c.drawString(text_x, text_y - 15, "Dirección: Entre Ríos 640")
        c.drawString(text_x, text_y - 29, "Teléfono: 341-4459665")
        c.drawString(text_x, text_y - 43, "Celular:  341-5071726")
        c.drawString(text_x, text_y - 57, "Email: info@bytcomputacion.com.ar")

        # Fecha de creación del presupuesto
        fecha_presupuesto = None
        if fecha_estado and isinstance(fecha_estado, dict):
            fecha_creacion = fecha_estado.get("fecha_creacion")
            if fecha_creacion:
                try:
                    fecha_presupuesto = datetime.datetime.strptime(fecha_creacion, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
                except Exception as e:
                    print(f"Error al parsear fecha_creacion: {e}")

        if not fecha_presupuesto:
            fecha_presupuesto = datetime.date.today().strftime("%d/%m/%Y")

        # Presupuesto, Fecha, Copia
        info_x = width - 50
        c.setFont("Helvetica-Bold", 10)
        c.drawRightString(info_x, y_offset - 20, f"Presupuesto N°: {id_presupuesto}")
        c.setFont("Helvetica", 10)
        c.drawRightString(info_x, y_offset - 35, f"Fecha: {fecha_presupuesto}")
        c.setFont("Helvetica-Bold", 10)
        c.drawRightString(info_x, y_offset - 50, copia)

        # Línea divisoria
        c.setStrokeColorRGB(0.6, 0.6, 0.6)
        c.setLineWidth(1)
        c.line(40, y_offset - 90, width - 40, y_offset - 90)

        # Datos del cliente
        x_left = 50
        y_datos = y_offset - 110

        c.setFont("Helvetica", 11)
        c.drawString(x_left, y_datos, f"Cliente: {nombre}")
        c.drawString(x_left, y_datos - 15, f"Celular: {telefono}")

        # Estado y su fecha
        estado_str = f"Estado: {estado}"
        fecha_estado_str = ""

        if fecha_estado and isinstance(fecha_estado, dict):
            fecha = None
            if estado == "En proceso":
                fecha = fecha_estado.get("fecha_proceso")
            elif estado == "No aceptado":
                fecha = fecha_estado.get("fecha_aceptado")
            elif estado == "Terminado":
                fecha = fecha_estado.get("fecha_finalizado")

            if fecha:
                try:
                    fecha_estado_str = datetime.datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
                    estado_str += f" - {fecha_estado_str}"
                except:
                    pass

        c.drawRightString(width - 50, y_datos, estado_str)

        # Cotización
        if cotizacion is not None:
            cotizacion_str = f"Presupuesto: ${float(cotizacion):,.2f}"
            c.drawRightString(width - 50, y_datos - 15, cotizacion_str)

        c.line(40, y_datos - 30, width - 40, y_datos - 30)

        # Descripción
        text = c.beginText(x_left, y_offset - 155)
        text.setFont("Helvetica", 10)
        for linea in descripcion.splitlines():
            text.textLine(linea)
        c.drawText(text)

        # Cuadro de información
        mensaje_titulo = "INFORMACIÓN IMPORTANTE"
        mensaje_texto = (
            "Se informará al cliente el presupuesto de reparación una vez realizada la revisión.\n"
            "En caso de no aceptar el mismo, se cobrará un cargo de $10.000 por diagnóstico."
        )

        espacio_inferior = 30
        msg_box_height = 65
        msg_box_width = width - 100
        msg_box_x = 50
        msg_box_y = y_offset - (height / 2) + espacio_inferior

        c.setStrokeColorRGB(0.2, 0.2, 0.2)
        c.setFillColorRGB(0.95, 0.95, 0.95)
        c.rect(msg_box_x, msg_box_y, msg_box_width, msg_box_height, fill=1)

        c.setFont("Helvetica-Bold", 10)
        c.setFillColorRGB(1, 0, 0)
        c.drawCentredString(width / 2, msg_box_y + msg_box_height - 15, mensaje_titulo)

        c.setFont("Helvetica-Bold", 9)
        c.setFillColorRGB(0, 0, 0)
        for i, linea in enumerate(mensaje_texto.splitlines()):
            y_line = msg_box_y + msg_box_height - 30 - (i * 12)
            c.drawCentredString(width / 2, y_line, linea)

        # Línea de corte
        if copia == "ORIGINAL":
            c.setStrokeColorRGB(0.6, 0.6, 0.6)
            c.setDash(1, 3)
            c.line(30, mitad, width - 30, mitad)
            c.setFont("Helvetica-Oblique", 9)
            c.setFillColorRGB(0, 0, 0)
            c.drawCentredString(width / 2, mitad + 5, "--- cortar por aquí ---")
            c.setDash()

    # Dibujar ambas copias
    dibujar_boleta(height, "ORIGINAL")
    dibujar_boleta(mitad, "DUPLICADO")

    c.save()
    os.startfile(file_name)
