from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QFrame
from PyQt5.QtCore import Qt
from db.database import total_reparaciones, costo_promedio, reparaciones_recientes, reparaciones_por_estado
from datetime import datetime

class VentanaEstadisticas(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Estadísticas de Reparaciones")
        self.setMinimumSize(600, 400)

        # Ya no llamamos a set_ui_style, ya que no necesitamos la imagen de fondo.
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Título de la ventana
        titulo = QLabel("📈 Estadísticas Generales")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #000000;  # Puedes cambiar el color del texto si lo deseas
        """)
        layout.addWidget(titulo)

        # Crear un marco para la tabla con bordes redondeados y fondo semitransparente
        frame = QFrame(self)
        frame.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 0.7);  # Fondo negro semitransparente
                border-radius: 15px;
                border: 2px solid #333;
            }
        """)
        frame.setLayout(QVBoxLayout())  # Crear un layout dentro del frame

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(2)
        self.tabla.setHorizontalHeaderLabels(["Métrica", "Valor"])
        self.tabla.setStyleSheet("""
            QTableWidget {
                border: none;
                font-size: 16px;
                color: #000;  # Texto en negro para contrastar
            }
            QHeaderView::section {
                background-color: rgba(255, 255, 255, 0.2);  # Fondo semitransparente para los encabezados
                font-weight: bold;
                color: #000000;
            }
            QTableWidgetItem {
                padding: 8px;
                color: #000;
                border: 1px solid #444;  # Borde más oscuro para los elementos de la tabla
            }
        """)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        frame.layout().addWidget(self.tabla)

        layout.addWidget(frame)
        self.setLayout(layout)
        self.cargar_datos_estadisticos()

    def cargar_datos_estadisticos(self):
        # Obtener estadísticas reales de la base de datos
        total_reparaciones_value = total_reparaciones()
        costo_promedio_value = costo_promedio()
        
        # Obtener reparaciones por estado
        reparaciones_estado = reparaciones_por_estado()

        # Aquí puedes agregar una lógica para contar las reparaciones recientes de este mes (o el período que prefieras)
        fecha_inicio = datetime(datetime.now().year, datetime.now().month, 1).strftime("%Y-%m-%d 00:00:00")
        fecha_fin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        reparaciones_mes = reparaciones_recientes(fecha_inicio, fecha_fin)

        # Calcular el porcentaje de reparaciones completadas
        reparaciones_completadas = reparaciones_estado.get("finalizado", 0)
        porcentaje_completadas = (reparaciones_completadas / total_reparaciones_value) * 100 if total_reparaciones_value else 0

        # Agregar estadísticas a la tabla
        estadisticas = {
            "Total de reparaciones": total_reparaciones_value,
            "Promedio de costo": f"${costo_promedio_value:,.2f}",
            "Reparaciones del mes": reparaciones_mes,
            "Porcentaje completadas": f"{porcentaje_completadas:.2f}%",
        }

        # Actualizar la tabla con los valores
        self.tabla.setRowCount(len(estadisticas))
        for fila, (clave, valor) in enumerate(estadisticas.items()):
            self.tabla.setItem(fila, 0, QTableWidgetItem(clave))
            self.tabla.setItem(fila, 1, QTableWidgetItem(str(valor)))
