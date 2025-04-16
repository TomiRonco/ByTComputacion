import os
import sys
from datetime import datetime

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QGroupBox, QMessageBox, QComboBox
)
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt

from db.database import buscar_reparacion, actualizar_presupuesto
from utils.pdf_generator import generar_boleta_pdf


def get_asset_path(filename):
    try:
        base_path = sys._MEIPASS
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
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        layout.addWidget(self.create_busqueda_group())
        layout.addWidget(self.create_info_group())
        layout.addWidget(self.create_detalle_group())
        layout.addLayout(self.create_botones_layout())

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

    def create_busqueda_group(self):
        group = QGroupBox("Buscar Presupuesto")
        group.setStyleSheet("""
            QGroupBox {
                background-color: rgba(0, 0, 0, 150);
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
            }
        """)
        layout = QVBoxLayout()
        form_layout = QHBoxLayout()

        label = QLabel("Número de presupuesto:")
        label.setFixedWidth(150)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Ej: 123")
        self.id_input.setFixedHeight(35)
        self.id_input.setFixedWidth(200)
        self.id_input.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border-radius: 5px;
                background-color: rgba(0, 0, 0, 100);
                color: white;
                border: 1px solid #888;
            }
        """)

        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.setFixedHeight(35)
        self.btn_buscar.setFixedWidth(100)
        self.btn_buscar.setStyleSheet(self.get_button_style())
        self.btn_buscar.clicked.connect(self.buscar)

        form_layout.addWidget(label)
        form_layout.addWidget(self.id_input)
        form_layout.addStretch()
        form_layout.addWidget(self.btn_buscar)

        layout.addLayout(form_layout)
        group.setLayout(layout)
        return group

    def create_info_group(self):
        group = QGroupBox("Información del cliente y estado")
        group.setStyleSheet("""
            QGroupBox {
                background-color: rgba(0, 0, 0, 150);
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
            }
        """)
        layout = QHBoxLayout()

        cliente_info = QVBoxLayout()
        self.nombre_label = QLabel("Nombre: -")
        self.telefono_label = QLabel("Teléfono: -")
        cliente_info.addWidget(self.nombre_label)
        cliente_info.addWidget(self.telefono_label)

        estado_info = QVBoxLayout()
        self.estado_label = QLabel("Estado actual: -")
        self.costo_label = QLabel("Presupuesto actual: -")
        estado_info.addWidget(self.estado_label)
        estado_info.addWidget(self.costo_label)

        layout.addLayout(cliente_info)
        layout.addStretch()
        layout.addLayout(estado_info)

        group.setLayout(layout)
        return group

    def create_detalle_group(self):
        group = QGroupBox("Detalle de Reparación")
        group.setStyleSheet("""
            QGroupBox {
                background-color: rgba(0, 0, 0, 150);
                color: white;
                border-radius: 10px;
                padding: 5px;
                font-weight: bold;
            }
        """)
        layout = QVBoxLayout()

        self.resultado = QTextEdit()
        self.resultado.setPlaceholderText("Descripción detallada...")
        self.resultado.setMinimumHeight(100)
        self.resultado.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0, 0, 0, 100);
                color: white;
                border-radius: 5px;
                padding: 5px;
                border: 1px solid #888;
            }
        """)

        self.costo_input = QLineEdit()
        self.costo_input.setPlaceholderText("Costo en ARS")
        self.costo_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(0, 0, 0, 100);
                color: white;
                border-radius: 5px;
                padding: 5px;
                border: 1px solid #888;
            }
        """)

        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["Pendiente", "Aceptado", "En proceso", "Finalizado", "No aceptado"])
        self.estado_combo.setStyleSheet("""
            QComboBox {
                background-color: rgba(0, 0, 0, 100);
                color: white;
                border-radius: 5px;
                padding: 5px;
                border: 1px solid #888;
            }
        """)

        layout.addWidget(QLabel("Descripción:"))
        layout.addWidget(self.resultado)
        layout.addWidget(QLabel("Estado:"))
        layout.addWidget(self.estado_combo)
        layout.addWidget(QLabel("Costo (ARS):"))
        layout.addWidget(self.costo_input)


        group.setLayout(layout)
        return group

    def create_botones_layout(self):
        layout = QHBoxLayout()

        self.btn_guardar = QPushButton("Guardar Cambios")
        self.btn_guardar.setFixedHeight(40)
        self.btn_guardar.setStyleSheet(self.get_button_style())
        self.btn_guardar.clicked.connect(self.guardar)

        self.btn_reimprimir = QPushButton("Reimprimir Boleta")
        self.btn_reimprimir.setFixedHeight(40)
        self.btn_reimprimir.setStyleSheet(self.get_button_style())
        self.btn_reimprimir.clicked.connect(self.reimprimir)

        layout.addWidget(self.btn_guardar)
        layout.addWidget(self.btn_reimprimir)

        return layout

    def get_button_style(self):
        return """
            QPushButton {
                background-color: rgba(50, 50, 50, 180);
                color: white;
                border-radius: 6px;
                border: 1px solid #999;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: rgba(90, 90, 90, 220);
            }
        """

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
            self.descripcion_actual = resultado[3]
            estado = resultado[4] if resultado[4] else "Pendiente"
            costo = resultado[5] or "-"

            # Fechas almacenadas desde la base de datos
            self.fecha_creacion = resultado[6]
            self.fecha_aceptado = resultado[7]
            self.fecha_proceso = resultado[8]
            self.fecha_finalizado = resultado[9]

            self.resultado.setText(self.descripcion_actual)
            self.estado_combo.setCurrentText(estado)
            self.costo_input.setText("" if costo == "-" else str(costo))

            self.nombre_label.setText(f"Nombre: {self.nombre}")
            self.telefono_label.setText(f"Teléfono: {self.telefono}")
            self.estado_label.setText(f"Estado actual: {estado}")
            self.costo_label.setText(f"Presupuesto actual: {costo}")
            self.estado_anterior = estado
        else:
            QMessageBox.information(self, "No encontrado", "No se encontró el presupuesto.")
            self.limpiar_campos()

    def limpiar_campos(self):
        self.resultado.clear()
        self.costo_input.clear()
        self.nombre_label.setText("Nombre: -")
        self.telefono_label.setText("Teléfono: -")
        self.estado_label.setText("Estado actual: -")
        self.costo_label.setText("Presupuesto actual: -")

    def obtener_fechas_estado(self, estado):
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fechas = {"fecha_aceptado": None, "fecha_proceso": None, "fecha_finalizado": None}

        if estado == "Aceptado":
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

        descripcion = self.resultado.toPlainText().strip()
        nuevo_estado = self.estado_combo.currentText()

        costo_texto = self.costo_input.text().strip()
        if costo_texto:
            try:
                costo = float(costo_texto)
            except ValueError:
                QMessageBox.warning(self, "Error", "Costo inválido.")
                return
        else:
            costo = None

        fechas = self.obtener_fechas_estado(nuevo_estado)
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        if nuevo_estado != getattr(self, "estado_anterior", None):
            descripcion += f'\n→ Estado cambiado a "{nuevo_estado}" el {fecha_actual}'
            self.estado_anterior = nuevo_estado

        self.resultado.setText(descripcion)

        actualizar_presupuesto(
            self.presupuesto_id,
            descripcion,
            nuevo_estado,
            costo,
            fechas["fecha_aceptado"],
            fechas["fecha_proceso"],
            fechas["fecha_finalizado"]
        )

        self.estado_label.setText(f"Estado actual: {nuevo_estado}")
        self.costo_label.setText(f"Presupuesto actual: {costo if costo is not None else '-'}")

        QMessageBox.information(self, "Éxito", "Presupuesto actualizado correctamente.")

    def reimprimir(self):
        if not hasattr(self, "presupuesto_id"):
            QMessageBox.warning(self, "Error", "Debe buscar un presupuesto primero.")
            return

        descripcion = self.resultado.toPlainText()
        estado = self.estado_combo.currentText()

        costo_texto = self.costo_input.text().strip()
        if costo_texto:
            try:
                costo = float(costo_texto)
            except ValueError:
                QMessageBox.warning(self, "Error", "Costo inválido.")
                return
        else:
            costo = None

        # Usar fechas ya guardadas
        fechas = {
            "fecha_creacion": self.fecha_creacion,
            "fecha_aceptado": self.fecha_aceptado,
            "fecha_proceso": self.fecha_proceso,
            "fecha_finalizado": self.fecha_finalizado
        }

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
