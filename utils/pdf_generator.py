from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os
import datetime

def generar_boleta_pdf(id_presupuesto, nombre, telefono, descripcion, cotizacion=None, estado="Pendiente", fecha_estado=None):
    file_name = f"presupuesto_{id_presupuesto}.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)
    width, height = A4
    mitad = height / 2

    def dibujar_boleta(y_offset, copia):
        # Encabezado
        rect_x = 40
        rect_y = y_offset - 100
        rect_width = width - 80
        rect_height = 90
        c.setStrokeColorRGB(0, 0, 0)
        c.setFillColorRGB(0.95, 0.95, 0.95)
        c.rect(rect_x, rect_y, rect_width, rect_height, fill=1)

        # Datos del local alineados a la izquierda
        c.setFont("Helvetica-Bold", 14)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(rect_x + 10, rect_y + 60, "ByT Computación")

        c.setFont("Helvetica", 10)
        c.drawString(rect_x + 10, rect_y + 45, "Dirección: Entre Ríos 640")
        c.drawString(rect_x + 10, rect_y + 31, "Teléfono: 341-4459665")
        c.drawString(rect_x + 10, rect_y + 17, "Celular:  341-5071726")
        c.drawString(rect_x + 10, rect_y + 3, "Email: info@bytcomputacion.com.ar")

        # Presupuesto y fecha actual
        c.setFont("Helvetica-Bold", 10)
        c.drawRightString(width - 50, rect_y + 65, f"Presupuesto N°: {id_presupuesto}")

        fecha_actual = datetime.date.today().strftime("%d/%m/%Y")
        c.setFont("Helvetica", 10)
        c.drawRightString(width - 50, rect_y + 50, f"Fecha: {fecha_actual}")

        c.setFont("Helvetica-Bold", 10)
        c.drawRightString(width - 50, rect_y + 35, f"{copia}")

        # Datos del cliente y estado
        x_left = 50
        y_datos = y_offset - 130

        # Cliente
        c.setFont("Helvetica", 11)
        c.drawString(x_left, y_datos, f"Cliente: {nombre}")
        c.drawString(x_left, y_datos - 15, f"Celular: {telefono}")

        # Estado y fecha del estado
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
                fecha_estado_str = datetime.datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
                estado_str += f" - {fecha_estado_str}"

        c.setFont("Helvetica", 11)
        c.drawRightString(width - 50, y_datos, estado_str)

        # Cotización (solo si existe)
        if cotizacion is not None:
            c.setFont("Helvetica", 11)
            cotizacion_str = f"Presupuesto: ${float(cotizacion):,.2f}"
            c.drawRightString(width - 50, y_datos - 15, cotizacion_str)

        # Descripción
        c.drawString(x_left, y_offset - 170, "Descripción:")
        text = c.beginText(x_left, y_offset - 190)
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

        # Línea divisoria
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
    os.system(f"open {file_name}")
