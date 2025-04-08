import os
import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtCore import Qt, QTimer, QDateTime
from ui.cargar_reparacion import VentanaCargarReparacion
from ui.buscar_reparacion import VentanaBuscarReparacion

def resource_path(relative_path):
    """Obtiene el path absoluto del recurso, compatible con PyInstaller."""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Reparaciones")
        self.setFixedSize(600, 400)

        # Fondo
        ruta_fondo = resource_path("assets/fondo.jpg")
        try:
            fondo = QPixmap(ruta_fondo)
            if not fondo.isNull():
                palette = QPalette()
                palette.setBrush(QPalette.Window, QBrush(fondo.scaled(
                    self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
                self.setPalette(palette)
        except Exception as e:
            print(f"Error cargando fondo: {e}")

        # Layout principal
        layout_principal = QVBoxLayout()
        layout_principal.setAlignment(Qt.AlignTop)

        # Estilo botones
        estilo_boton = """
            QPushButton {
                background-color: rgba(50, 50, 50, 180);
                color: white;
                font-size: 16px;
                padding: 12px;
                border-radius: 10px;
                border: 2px solid white;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: rgba(70, 70, 70, 220);
            }
        """

        # Botones en dos columnas
        layout_grid = QGridLayout()
        layout_grid.setSpacing(20)
        layout_grid.setContentsMargins(60, 20, 60, 10)

        btn_agregar = QPushButton("Cargar reparación")
        btn_agregar.setStyleSheet(estilo_boton)
        btn_agregar.clicked.connect(self.abrir_cargar_reparacion)

        btn_buscar = QPushButton("Buscar presupuesto")
        btn_buscar.setStyleSheet(estilo_boton)
        btn_buscar.clicked.connect(self.abrir_buscar_reparacion)

        layout_grid.addWidget(btn_agregar, 0, 0)
        layout_grid.addWidget(btn_buscar, 0, 1)

        layout_principal.addLayout(layout_grid)

        # Fecha
        self.label_fecha = QLabel()
        self.label_fecha.setAlignment(Qt.AlignCenter)
        self.label_fecha.setStyleSheet("color: black; font-size: 16px;")
        layout_principal.addWidget(self.label_fecha)

        # Hora
        self.label_hora = QLabel()
        self.label_hora.setAlignment(Qt.AlignCenter)
        self.label_hora.setStyleSheet("color: black; font-size: 28px; font-weight: bold;")
        layout_principal.addWidget(self.label_hora)

        # Timer para actualizar fecha y hora
        timer = QTimer(self)
        timer.timeout.connect(self.actualizar_fecha_hora)
        timer.start(1000)
        self.actualizar_fecha_hora()

        # Spacer
        layout_principal.addStretch()

        # Botón salir abajo a la derecha
        boton_salir = QPushButton("Salir")
        boton_salir.setStyleSheet(estilo_boton)
        boton_salir.setFixedWidth(100)
        boton_salir.clicked.connect(self.salir_aplicacion)

        layout_salir = QHBoxLayout()
        layout_salir.addStretch()
        layout_salir.addWidget(boton_salir)

        layout_principal.addLayout(layout_salir)

        self.setLayout(layout_principal)

    def actualizar_fecha_hora(self):
        ahora = QDateTime.currentDateTime()
        self.label_fecha.setText(ahora.toString("dd/MM/yyyy"))
        self.label_hora.setText(ahora.toString("HH:mm:ss"))

    def abrir_cargar_reparacion(self):
        self.ventana = VentanaCargarReparacion()
        self.ventana.show()

    def abrir_buscar_reparacion(self):
        self.ventana = VentanaBuscarReparacion()
        self.ventana.show()

    def salir_aplicacion(self):
        self.close()
