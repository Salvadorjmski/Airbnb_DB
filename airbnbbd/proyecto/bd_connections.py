
import mysql.connector
from mysql.connector import Error

def get_conn():
    try:
        conn=mysql.connector.connect(
        user="airbnbadmin",
        password="Cerati!123mouse",
        host="airbnbdb.mysql.database.azure.com",
        port=3306,
        database="airbnbbd")
        return conn
    except Error as e:
        print(f"X Error de conexión: {e}")
        return None
