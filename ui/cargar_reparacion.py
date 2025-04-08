from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QComboBox, QCheckBox,
    QPushButton, QVBoxLayout, QMessageBox, QGroupBox, QStackedLayout
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
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre completo")
        self.main_layout.addWidget(QLabel("Nombre completo:"))
        self.main_layout.addWidget(self.nombre_input)

        self.telefono_input = QLineEdit()
        self.telefono_input.setPlaceholderText("Teléfono")
        self.main_layout.addWidget(QLabel("Teléfono:"))
        self.main_layout.addWidget(self.telefono_input)

        self.producto_combo = QComboBox()
        self.producto_combo.addItems(["PC Escritorio", "Notebook", "Impresora", "Calculadora", "Celular"])
        self.producto_combo.currentTextChanged.connect(self.mostrar_opciones_por_producto)
        self.main_layout.addWidget(QLabel("Producto a reparar:"))
        self.main_layout.addWidget(self.producto_combo)

        self.marca_label = QLabel("Marca / Modelo:")
        self.marca_combo = QComboBox()
        self.main_layout.addWidget(self.marca_label)
        self.main_layout.addWidget(self.marca_combo)

        self.opciones_stack = QStackedLayout()

        # Grupo Notebook / PC
        self.notebook_group = QGroupBox("Opciones de Reparación")
        notebook_layout = QVBoxLayout()
        self.check_n_pantalla = QCheckBox("Pantalla")
        self.check_n_pin = QCheckBox("Pin de carga")
        self.check_n_placa = QCheckBox("Placa")
        self.check_n_ssd = QCheckBox("Cambio SSD")
        self.check_n_ram = QCheckBox("Aumento Memoria RAM")
        self.check_n_act = QCheckBox("Actualización Software")
        self.check_n_activ = QCheckBox("Activación Software")
        for chk in [self.check_n_pantalla, self.check_n_pin, self.check_n_placa,
                    self.check_n_ssd, self.check_n_ram, self.check_n_act, self.check_n_activ]:
            notebook_layout.addWidget(chk)
        self.notebook_group.setLayout(notebook_layout)
        self.opciones_stack.addWidget(self.notebook_group)

        # Impresora
        self.impresora_group = QGroupBox("Opciones de Impresora")
        impresora_layout = QVBoxLayout()
        self.check_i_atasco = QCheckBox("Atasco de papel")
        self.check_i_limpieza = QCheckBox("Limpieza general")
        self.check_i_cabezales = QCheckBox("Cabezales")
        self.check_i_cartuchos = QCheckBox("Cartuchos")
        for chk in [self.check_i_atasco, self.check_i_limpieza,
                    self.check_i_cabezales, self.check_i_cartuchos]:
            impresora_layout.addWidget(chk)
        self.impresora_group.setLayout(impresora_layout)
        self.opciones_stack.addWidget(self.impresora_group)

        # Calculadora
        self.calculadora_group = QGroupBox("Opciones de Calculadora")
        calculadora_layout = QVBoxLayout()
        self.check_c_placa = QCheckBox("Placa")
        self.check_c_mantenimiento = QCheckBox("Mantenimiento general")
        self.check_c_papel = QCheckBox("Agarre de papel")
        for chk in [self.check_c_placa, self.check_c_mantenimiento, self.check_c_papel]:
            calculadora_layout.addWidget(chk)
        self.calculadora_group.setLayout(calculadora_layout)
        self.opciones_stack.addWidget(self.calculadora_group)

        # Celular
        self.celular_group = QGroupBox("Opciones de Celular")
        celular_layout = QVBoxLayout()
        self.check_cel_modulo = QCheckBox("Módulo")
        self.check_cel_pin = QCheckBox("Pin de carga")
        self.check_cel_placa = QCheckBox("Placa de carga")
        self.check_cel_bateria = QCheckBox("Batería")
        for chk in [self.check_cel_modulo, self.check_cel_pin, self.check_cel_placa, self.check_cel_bateria]:
            celular_layout.addWidget(chk)
        self.celular_group.setLayout(celular_layout)
        self.opciones_stack.addWidget(self.celular_group)

        self.main_layout.addLayout(self.opciones_stack)
        self.opciones_stack.setCurrentIndex(0)

        self.btn_guardar = QPushButton("Guardar y Generar Boleta")
        self.btn_guardar.clicked.connect(self.guardar_reparacion)
        self.main_layout.addWidget(self.btn_guardar)

        self.setLayout(self.main_layout)
        self.mostrar_opciones_por_producto("PC Escritorio")

    def resource_path(self, relative_path):
        """Obtiene la ruta absoluta del recurso, compatible con PyInstaller"""
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

    def mostrar_opciones_por_producto(self, producto):
        self.marca_combo.clear()
        self.marca_label.setVisible(True)
        self.marca_combo.setVisible(True)

        if producto == "PC Escritorio":
            self.opciones_stack.setCurrentIndex(0)
            self.marca_label.setVisible(False)
            self.marca_combo.setVisible(False)
        elif producto == "Notebook":
            self.opciones_stack.setCurrentIndex(0)
            self.marca_combo.addItems(["HP", "Lenovo", "Asus", "Dell", "Acer", "Bangho", "Toshiba", "CX"])
        elif producto == "Impresora":
            self.opciones_stack.setCurrentIndex(1)
            self.marca_combo.addItems(["HP", "Epson", "Brother", "Canon", "Samsung"])
        elif producto == "Calculadora":
            self.opciones_stack.setCurrentIndex(2)
            self.marca_combo.addItems(["Cifra PR-1200", "Cifra PR-26", "Cifra PR-226", "Cifra PR-235", "Cifra PR-255"])
        elif producto == "Celular":
            self.opciones_stack.setCurrentIndex(3)
            self.marca_combo.addItems(["Samsung", "Motorola", "Xiaomi", "iPhone", "Huawei", "Nokia", "LG", "Realme"])

    def guardar_reparacion(self):
        nombre = self.nombre_input.text().strip()
        telefono = self.telefono_input.text().strip()
        producto = self.producto_combo.currentText()
        marca = self.marca_combo.currentText() if self.marca_combo.isVisible() else "No aplica"

        if not nombre or not telefono:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        tareas = []
        if producto in ["PC Escritorio", "Notebook"]:
            if self.check_n_pantalla.isChecked(): tareas.append("Pantalla")
            if self.check_n_pin.isChecked(): tareas.append("Pin de carga")
            if self.check_n_placa.isChecked(): tareas.append("Placa")
            if self.check_n_ssd.isChecked(): tareas.append("Cambio SSD")
            if self.check_n_ram.isChecked(): tareas.append("Aumento RAM")
            if self.check_n_act.isChecked(): tareas.append("Actualización Software")
            if self.check_n_activ.isChecked(): tareas.append("Activación Software")
        elif producto == "Impresora":
            if self.check_i_atasco.isChecked(): tareas.append("Atasco de papel")
            if self.check_i_limpieza.isChecked(): tareas.append("Limpieza general")
            if self.check_i_cabezales.isChecked(): tareas.append("Cabezales")
            if self.check_i_cartuchos.isChecked(): tareas.append("Cartuchos")
        elif producto == "Calculadora":
            if self.check_c_placa.isChecked(): tareas.append("Placa")
            if self.check_c_mantenimiento.isChecked(): tareas.append("Mantenimiento general")
            if self.check_c_papel.isChecked(): tareas.append("Agarre de papel")
        elif producto == "Celular":
            if self.check_cel_modulo.isChecked(): tareas.append("Módulo")
            if self.check_cel_pin.isChecked(): tareas.append("Pin de carga")
            if self.check_cel_placa.isChecked(): tareas.append("Placa de carga")
            if self.check_cel_bateria.isChecked(): tareas.append("Batería")

        if not tareas:
            QMessageBox.warning(self, "Error", "Debe seleccionar al menos una tarea.")
            return

        descripcion = (
            f"{producto} - "
            f"{marca}\n"
            f"Tareas a realizar: \n - " + "\n- ".join(tareas)
        )

        presupuesto_id = guardar_reparacion(nombre, telefono, descripcion)
        generar_boleta_pdf(presupuesto_id, nombre, telefono, descripcion)

        QMessageBox.information(self, "Éxito", f"Presupuesto generado N° {presupuesto_id}")
        self.close()
