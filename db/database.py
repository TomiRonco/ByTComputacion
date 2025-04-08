import sqlite3
import os
import sys
from datetime import datetime

# Detectar si el script está congelado (ejecutándose desde un .exe/.app con PyInstaller)
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta persistente segura para la base de datos (en el home del usuario)
DATA_DIR = os.path.join(os.path.expanduser("~"), ".reparaciones_app")
os.makedirs(DATA_DIR, exist_ok=True)

# Ruta completa a la base de datos
DB_PATH = os.path.join(DATA_DIR, "reparaciones.db")

def conectar():
    return sqlite3.connect(DB_PATH)

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
            fecha_aceptado TEXT,
            fecha_proceso TEXT,
            fecha_finalizado TEXT
        )
    """)
    conn.commit()
    conn.close()

def guardar_reparacion(nombre_completo, telefono, descripcion):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reparaciones (nombre_completo, telefono, descripcion)
        VALUES (?, ?, ?)
    """, (nombre_completo, telefono, descripcion))
    conn.commit()
    presupuesto_id = cursor.lastrowid
    conn.close()
    return presupuesto_id

def buscar_reparacion(presupuesto_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nombre_completo, telefono, descripcion, estado, costo
        FROM reparaciones WHERE id = ?
    """, (presupuesto_id,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

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
