#si quieren conectarse a la base de datos deben importar este archivo de python
import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",        #el user debe ser el mismo
    password="root",    #la contraseña varia, si alguien que no soy yo ejecuta el codigo debe cambiar la contraseña
    database="rajtir"   #la db, si le pusiste el mismo nombre es el mismo
)

def init_conn():
    cursor = conexion.cursor()

    return cursor


