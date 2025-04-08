import os
import sys
from datetime import datetime

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox, QComboBox
)
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt

from db.database import buscar_reparacion, actualizar_presupuesto
from utils.pdf_generator import generar_boleta_pdf


def get_asset_path(filename):
    """
    Devuelve la ruta absoluta al archivo dentro de assets.
    Compatible con ejecución directa y PyInstaller.
    """
    try:
        base_path = sys._MEIPASS  # PyInstaller
    except AttributeError:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    return os.path.join(base_path, 'assets', filename)


class VentanaBuscarReparacion(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Buscar Presupuesto")
        self.setFixedSize(800, 600)

        self.set_background_image()

        layout = QVBoxLayout()

        # Grilla búsqueda
        buscar_grid = QGridLayout()
        label = QLabel("Ingrese el número de presupuesto:")
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Número de presupuesto")
        self.id_input.setFixedHeight(35)

        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.setStyleSheet("background-color: rgba(100, 100, 100, 200); color: white; border-radius: 5px;")
        self.btn_buscar.setMinimumHeight(70)
        self.btn_buscar.setMinimumWidth(150)
        self.btn_buscar.clicked.connect(self.buscar)

        buscar_grid.addWidget(label,        0, 0)
        buscar_grid.addWidget(self.id_input,1, 0)
        buscar_grid.addWidget(self.btn_buscar,0, 1, 2, 1)
        buscar_grid.setColumnStretch(0, 3)
        buscar_grid.setColumnStretch(1, 2)

        layout.addLayout(buscar_grid)

        # Info del cliente
        self.nombre_label = QLabel("Nombre: -")
        self.telefono_label = QLabel("Teléfono: -")
        layout.addWidget(self.nombre_label)
        layout.addWidget(self.telefono_label)

        # Descripción
        layout.addWidget(QLabel("Descripción:"))
        self.resultado = QTextEdit()
        layout.addWidget(self.resultado)

        # Costo
        layout.addWidget(QLabel("Costo (ARS):"))
        self.costo_input = QLineEdit()
        self.costo_input.setPlaceholderText("Costo de la reparación")
        layout.addWidget(self.costo_input)

        # Estado
        layout.addWidget(QLabel("Estado:"))
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["Aceptado", "En proceso", "Finalizado", "No aceptado"])
        layout.addWidget(self.estado_combo)

        # Botones
        botones_layout = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar Cambios")
        self.btn_guardar.setFixedHeight(40)
        self.btn_guardar.setStyleSheet("background-color: rgba(80, 80, 150, 200); color: white; border-radius: 5px;")
        self.btn_guardar.clicked.connect(self.guardar)

        self.btn_reimprimir = QPushButton("Reimprimir Boleta")
        self.btn_reimprimir.setFixedHeight(40)
        self.btn_reimprimir.setStyleSheet("background-color: rgba(150, 80, 80, 200); color: white; border-radius: 5px;")
        self.btn_reimprimir.clicked.connect(self.reimprimir)

        botones_layout.addWidget(self.btn_guardar)
        botones_layout.addWidget(self.btn_reimprimir)
        layout.addLayout(botones_layout)

        self.setLayout(layout)

    def set_background_image(self):
        image_path = get_asset_path("fondo.jpg")
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            palette = QPalette()
            palette.setBrush(QPalette.Window, QBrush(pixmap.scaled(
                self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
            self.setPalette(palette)
            self.setAutoFillBackground(True)
        else:
            print("⚠️ Imagen de fondo no encontrada:", image_path)

    def resizeEvent(self, event):
        self.set_background_image()
        super().resizeEvent(event)

    def buscar(self):
        try:
            id_presupuesto = int(self.id_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Número de presupuesto inválido.")
            return

        resultado = buscar_reparacion(id_presupuesto)
        if resultado:
            self.presupuesto_id = resultado[0]
            self.nombre = resultado[1]
            self.telefono = resultado[2]
            descripcion = resultado[3]
            estado = resultado[4] or "Aceptado"
            costo = resultado[5] or ""

            self.resultado.setText(descripcion)
            self.estado_combo.setCurrentText(estado)
            self.costo_input.setText(str(costo))

            self.nombre_label.setText(f"Nombre: {self.nombre}")
            self.telefono_label.setText(f"Teléfono: {self.telefono}")
        else:
            QMessageBox.information(self, "No encontrado", "No se encontró el presupuesto.")
            self.limpiar_campos()

    def limpiar_campos(self):
        self.resultado.clear()
        self.costo_input.clear()
        self.nombre_label.setText("Nombre: -")
        self.telefono_label.setText("Teléfono: -")

    def obtener_fechas_estado(self, estado):
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fechas = {"fecha_aceptado": None, "fecha_proceso": None, "fecha_finalizado": None}

        if estado in ["Aceptado", "No aceptado"]:
            fechas["fecha_aceptado"] = fecha_actual
        elif estado == "En proceso":
            fechas["fecha_proceso"] = fecha_actual
        elif estado == "Finalizado":
            fechas["fecha_finalizado"] = fecha_actual

        return fechas

    def guardar(self):
        if not hasattr(self, "presupuesto_id"):
            QMessageBox.warning(self, "Error", "Debe buscar un presupuesto primero.")
            return

        descripcion = self.resultado.toPlainText()
        estado = self.estado_combo.currentText()
        try:
            costo = float(self.costo_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Costo inválido.")
            return

        fechas = self.obtener_fechas_estado(estado)

        actualizar_presupuesto(
            self.presupuesto_id,
            descripcion,
            estado,
            costo,
            fechas["fecha_aceptado"],
            fechas["fecha_proceso"],
            fechas["fecha_finalizado"]
        )

        QMessageBox.information(self, "Éxito", "Presupuesto actualizado correctamente.")

    def reimprimir(self):
        if not hasattr(self, "presupuesto_id"):
            QMessageBox.warning(self, "Error", "Debe buscar un presupuesto primero.")
            return

        descripcion = self.resultado.toPlainText()
        estado = self.estado_combo.currentText()
        try:
            costo = float(self.costo_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Costo inválido.")
            return

        fechas = self.obtener_fechas_estado(estado)

        generar_boleta_pdf(
            self.presupuesto_id,
            self.nombre,
            self.telefono,
            descripcion,
            costo,
            estado,
            fechas
        )

        QMessageBox.information(self, "Boleta Generada", "Boleta reimpresa exitosamente.")
