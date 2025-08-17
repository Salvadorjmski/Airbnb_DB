import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Carga variables del .env (mismo directorio)
load_dotenv()

def get_conn():
    """Devuelve una conexión a MySQL (Azure-ready)."""
    try:
        ssl_disabled = os.getenv("DB_SSL", "true").lower() in ("false", "0", "no")
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", ""),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", ""),
            ssl_disabled=ssl_disabled
        )
        return conn
    except Error as e:
        print(f"❌ Error de conexión: {e}")
        return None
    