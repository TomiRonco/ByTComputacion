import sqlite3
import os
from datetime import datetime
import sys

# Ruta al directorio de la base de datos (considera si estamos ejecutando desde el empaquetado o desde código fuente)
if getattr(sys, 'frozen', False):  # Si el código está empaquetado
    BASE_DIR = os.path.dirname(os.path.abspath(sys.executable))  # Ruta al directorio del ejecutable
else:  # Si estamos ejecutando desde el código fuente
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)  # Aseguramos que el directorio exista

DB_PATH = os.path.join(DATA_DIR, "reparaciones.db")

# Función para conectar con la base de datos
def conectar():
    return sqlite3.connect(DB_PATH)

# Crear la tabla 'reparaciones' si no existe
def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reparaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_completo TEXT NOT NULL,
        telefono TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        estado TEXT,
        costo REAL,
        fecha_creacion TEXT NOT NULL,
        fecha_aceptado TEXT,
        fecha_proceso TEXT,
        fecha_finalizado TEXT
    )
    """)
    conn.commit()
    conn.close()

# Función para guardar una nueva reparación
def guardar_reparacion(nombre_completo, telefono, descripcion):
    conn = conectar()
    cursor = conn.cursor()
    fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO reparaciones (nombre_completo, telefono, descripcion, fecha_creacion)
        VALUES (?, ?, ?, ?)
    """, (nombre_completo, telefono, descripcion, fecha_creacion))
    conn.commit()
    presupuesto_id = cursor.lastrowid
    conn.close()
    return presupuesto_id

# Función para buscar una reparación por su ID
def buscar_reparacion(presupuesto_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nombre_completo, telefono, descripcion, estado, costo,
               fecha_creacion, fecha_aceptado, fecha_proceso, fecha_finalizado
        FROM reparaciones WHERE id = ?
    """, (presupuesto_id,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

# Función para actualizar el presupuesto de una reparación
def actualizar_presupuesto(id_presupuesto, descripcion, estado, costo, fecha_aceptado, fecha_proceso, fecha_finalizado):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE reparaciones
        SET descripcion = ?, estado = ?, costo = ?,
            fecha_aceptado = COALESCE(fecha_aceptado, ?),
            fecha_proceso = COALESCE(fecha_proceso, ?),
            fecha_finalizado = COALESCE(fecha_finalizado, ?)
        WHERE id = ?
    """, (descripcion, estado, costo, fecha_aceptado, fecha_proceso, fecha_finalizado, id_presupuesto))
    conn.commit()
    conn.close()

# Función para eliminar y reiniciar la base de datos
def resetear_base_de_datos():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Base de datos eliminada.")
    crear_tabla()
    print("Base de datos reiniciada.")

# Función para obtener el total de reparaciones
def total_reparaciones():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM reparaciones")
    total = cursor.fetchone()[0]
    conn.close()
    return total

# Función para obtener el costo promedio de las reparaciones
def costo_promedio():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(costo) FROM reparaciones WHERE costo IS NOT NULL")
    promedio = cursor.fetchone()[0]
    conn.close()
    return promedio if promedio else 0.0

# Función para obtener el número de reparaciones recientes (en el mes actual)
def reparaciones_recientes(fecha_inicio, fecha_fin):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM reparaciones
        WHERE fecha_creacion BETWEEN ? AND ?
    """, (fecha_inicio, fecha_fin))
    total_recientes = cursor.fetchone()[0]
    conn.close()
    return total_recientes

# Función para obtener las reparaciones agrupadas por estado (por ejemplo, "finalizado", "pendiente")
def reparaciones_por_estado():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT estado, COUNT(*) FROM reparaciones GROUP BY estado")
    estados = cursor.fetchall()
    conn.close()
    return {estado: count for estado, count in estados}
