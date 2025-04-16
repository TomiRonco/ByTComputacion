from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QCheckBox, QTextEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox,
    QGroupBox, QFormLayout, QSizePolicy
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os
import sys

from db.database import guardar_reparacion
from utils.pdf_generator import generar_boleta_pdf


class VentanaCargarReparacion(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cargar Reparación")
        self.setFixedSize(800, 600)

        self.fondo = QLabel(self)
        self.fondo.setGeometry(0, 0, 800, 600)
        self.set_background_image("assets/fondo.jpg")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        # Sección: Datos del Cliente
        self.seccion_cliente = self.crear_seccion_cliente()
        self.main_layout.addWidget(self.seccion_cliente)

        # Sección: Producto a reparar
        self.seccion_producto = self.crear_seccion_producto()
        self.main_layout.addWidget(self.seccion_producto)

        # Sección: Descripción
        self.seccion_descripcion = self.crear_seccion_descripcion()
        self.main_layout.addWidget(self.seccion_descripcion)

        # Botón
        self.btn_guardar = QPushButton("Guardar y Generar Boleta")
        self.btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #222;
                color: white;
                padding: 10px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #444;
            }
        """)
        self.btn_guardar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.btn_guardar.clicked.connect(self.guardar_reparacion)
        self.main_layout.addWidget(self.btn_guardar)

        self.setLayout(self.main_layout)

    from PyQt5.QtCore import Qt

    def crear_seccion_cliente(self):
        grupo = QGroupBox("Datos del Cliente")
        grupo.setStyleSheet(self.estilo_grupo())

        layout = QVBoxLayout()

        # Fila Nombre
        fila_nombre = QHBoxLayout()
        label_nombre = QLabel("Nombre completo:")
        label_nombre.setFixedWidth(120)  # Ajustá según necesites
        label_nombre.setStyleSheet("color: white;")
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre completo")
        self.nombre_input.setStyleSheet(self.estilo_input())
        self.nombre_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        fila_nombre.addWidget(label_nombre)
        fila_nombre.addWidget(self.nombre_input)
        layout.addLayout(fila_nombre)

        # Fila Teléfono
        fila_telefono = QHBoxLayout()
        label_telefono = QLabel("Teléfono:")
        label_telefono.setFixedWidth(120)
        label_telefono.setStyleSheet("color: white;")
        self.telefono_input = QLineEdit()
        self.telefono_input.setPlaceholderText("Teléfono")
        self.telefono_input.setStyleSheet(self.estilo_input())
        self.telefono_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        fila_telefono.addWidget(label_telefono)
        fila_telefono.addWidget(self.telefono_input)
        layout.addLayout(fila_telefono)

        grupo.setLayout(layout)
        return grupo

    def crear_seccion_producto(self):
        grupo = QGroupBox("Producto a Reparar")
        layout = QVBoxLayout()

        self.checkboxes_layout = QHBoxLayout()
        self.productos_checkboxes = []
        productos = ["PC Escritorio", "Notebook", "Impresora", "Calculadora", "Celular"]
        for producto in productos:
            checkbox = QCheckBox(producto)
            checkbox.setStyleSheet("color: white;")
            self.checkboxes_layout.addWidget(checkbox)
            self.productos_checkboxes.append(checkbox)
        layout.addLayout(self.checkboxes_layout)

        self.marca_input = QLineEdit()
        self.marca_input.setPlaceholderText("Marca / Modelo")
        self.marca_input.setStyleSheet(self.estilo_input())
        label = QLabel("Marca / Modelo:")
        label.setStyleSheet("color: white;")
        layout.addWidget(label)
        layout.addWidget(self.marca_input)

        grupo.setLayout(layout)
        grupo.setStyleSheet(self.estilo_grupo())
        return grupo

    def crear_seccion_descripcion(self):
        grupo = QGroupBox("Descripción del Problema")
        layout = QVBoxLayout()

        self.descripcion_input = QTextEdit()
        self.descripcion_input.setPlaceholderText("Describa el problema o tareas a realizar...")
        self.descripcion_input.setStyleSheet(self.estilo_input())
        layout.addWidget(self.descripcion_input)

        grupo.setLayout(layout)
        grupo.setStyleSheet(self.estilo_grupo())
        return grupo

    def estilo_grupo(self):
        return """
        QGroupBox {
            background-color: rgba(0, 0, 0, 150); /* Fondo negro con transparencia */
            color: white;
            border: 1px solid #444;
            border-radius: 10px;
            padding: 10px;
            font-weight: bold;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 5px;
        }
        """

    def estilo_input(self):
        return """
        QLineEdit, QTextEdit {
            background-color: rgba(0, 0, 0, 100);
            color: white;
            border: 1px solid #666;
            border-radius: 5px;
            padding: 5px;
        }
        """

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def set_background_image(self, image_path):
        path = self.resource_path(image_path)
        if not os.path.exists(path):
            print(f"[Advertencia] Imagen no encontrada: {path}")
            return
        pixmap = QPixmap(path).scaled(800, 600, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.fondo.setPixmap(pixmap)
        self.fondo.lower()

    def guardar_reparacion(self):
        nombre = self.nombre_input.text().strip()
        telefono = self.telefono_input.text().strip()
        descripcion = self.descripcion_input.toPlainText().strip()

        productos_seleccionados = [cb.text() for cb in self.productos_checkboxes if cb.isChecked()]
        if not productos_seleccionados:
            QMessageBox.warning(self, "Error", "Debe seleccionar al menos un producto.")
            return

        marca = self.marca_input.text().strip()

        if not nombre or not telefono or not descripcion:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        lineas_descripcion = descripcion.splitlines()
        descripcion_con_iconos = '\n'.join(f"• {linea}" for linea in lineas_descripcion if linea.strip())

        descripcion_completa = (
            f"{', '.join(productos_seleccionados)} {marca}\n"
            f"Descripción:\n{descripcion_con_iconos}"
        )

        presupuesto_id = guardar_reparacion(nombre, telefono, descripcion_completa)
        generar_boleta_pdf(presupuesto_id, nombre, telefono, descripcion_completa)

        QMessageBox.information(self, "Éxito", f"Presupuesto generado N° {presupuesto_id}")
        self.close()
