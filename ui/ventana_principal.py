import os
import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtCore import Qt, QTimer, QDateTime

from ui.cargar_reparacion import VentanaCargarReparacion
from ui.buscar_reparacion import VentanaBuscarReparacion
from ui.estadisticas import VentanaEstadisticas


# --- Configuración de estilos globales ---
BUTTON_STYLE = """
    QPushButton {
        background-color: rgba(30, 30, 30, 190);
        color: white;
        font-size: 16px;
        padding: 12px;
        border-radius: 10px;
        border: 1px solid white;
        min-height: 50px;
    }
    QPushButton:hover {
        background-color: rgba(70, 70, 70, 220);
    }
"""

TITLE_STYLE = """
    color: white;
    font-size: 24px;
    font-weight: bold;
    background-color: rgba(0, 0, 0, 120);
    padding: 10px;
    border-radius: 10px;
"""

LABEL_STYLE = """
    color: white;
    background-color: rgba(0, 0, 0, 100);
    padding: 8px;
    border-radius: 8px;
"""

# --- Función de compatibilidad para acceder a recursos (PyInstaller ready) ---
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)


# --- Clase principal de la aplicación ---
class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Reparaciones")
        self.setFixedSize(600, 450)

        self._init_ui()

    # --- Setup completo de la UI ---
    def _init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Fondo personalizado
        self._set_background()

        # Título
        main_layout.addWidget(self._crear_titulo())

        # Botones principales en una sola fila
        main_layout.addLayout(self._crear_botones())

        # Información de fecha y hora
        main_layout.addLayout(self._crear_reloj())

        # Espacio adicional para flexibilidad de layout
        main_layout.addStretch(1)

        # Pie de página con botón de salir
        main_layout.addLayout(self._crear_footer())

    # --- Fondo personalizado ---
    def _set_background(self):
        ruta_fondo = resource_path("assets/fondo.jpg")
        try:
            fondo = QPixmap(ruta_fondo)
            if not fondo.isNull():
                palette = QPalette()
                palette.setBrush(QPalette.Window, QBrush(fondo.scaled(
                    self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
                self.setPalette(palette)
        except Exception as e:
            print(f"[Error] No se pudo cargar el fondo: {e}")

    # --- Título principal ---
    def _crear_titulo(self):
        titulo = QLabel("🛠️ Sistema de Reparaciones")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet(TITLE_STYLE)
        return titulo

    # --- Botones principales en una fila horizontal ---
    def _crear_botones(self):
        layout = QHBoxLayout()  # Usamos QHBoxLayout para alinear horizontalmente
        layout.setSpacing(20)  # Espacio entre los botones

        # Botones
        btn_cargar = self._crear_boton("➕ Cargar reparación", self.abrir_cargar_reparacion)
        btn_buscar = self._crear_boton("🔎 Buscar presupuesto", self.abrir_buscar_reparacion)
        btn_estadisticas = self._crear_boton("📊 Ver estadísticas", self.abrir_estadisticas)

        # Agregar los botones al layout horizontal
        layout.addWidget(btn_cargar)
        layout.addWidget(btn_buscar)
        layout.addWidget(btn_estadisticas)

        return layout

    # --- Información de fecha y hora en tiempo real ---
    def _crear_reloj(self):
        layout = QVBoxLayout()

        self.label_fecha = QLabel()
        self.label_hora = QLabel()

        self.label_fecha.setAlignment(Qt.AlignCenter)
        self.label_hora.setAlignment(Qt.AlignCenter)

        self.label_fecha.setStyleSheet(LABEL_STYLE + "font-size: 16px;")
        self.label_hora.setStyleSheet(LABEL_STYLE + "font-size: 28px; font-weight: bold;")

        layout.addWidget(self.label_fecha)
        layout.addWidget(self.label_hora)

        # Timer para actualizar cada segundo
        timer = QTimer(self)
        timer.timeout.connect(self._actualizar_fecha_hora)
        timer.start(1000)
        self._actualizar_fecha_hora()

        return layout

    # --- Pie de página con botón de salida ---
    def _crear_footer(self):
        footer_layout = QHBoxLayout()
        footer_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Botón de salir
        btn_salir = self._crear_boton("Salir", self.salir_aplicacion)
        btn_salir.setFixedWidth(100)

        footer_layout.addWidget(btn_salir)
        return footer_layout

    # --- Crear botones con estilo y acción ---
    def _crear_boton(self, texto, funcion):
        boton = QPushButton(texto)
        boton.setStyleSheet(BUTTON_STYLE)
        boton.clicked.connect(funcion)
        return boton

    # --- Actualiza hora y fecha cada segundo ---
    def _actualizar_fecha_hora(self):
        ahora = QDateTime.currentDateTime()
        self.label_fecha.setText(ahora.toString("dddd dd MMMM yyyy"))
        self.label_hora.setText(ahora.toString("HH:mm:ss"))

    # --- Funciones de navegación ---
    def abrir_cargar_reparacion(self):
        self.ventana = VentanaCargarReparacion()
        self.ventana.show()

    def abrir_buscar_reparacion(self):
        self.ventana = VentanaBuscarReparacion()
        self.ventana.show()
    
    def abrir_estadisticas(self):
        self.ventana_estadisticas = VentanaEstadisticas()
        self.ventana_estadisticas.show()

    def salir_aplicacion(self):
        self.close()
