from PyQt5.QtWidgets import QApplication
from ui.ventana_principal import VentanaPrincipal
from db.database import crear_tabla

if __name__ == "__main__":
    crear_tabla()

    app = QApplication([])
    ventana = VentanaPrincipal()
    ventana.show()
    app.exec_()
