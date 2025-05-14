#si quieren conectarse a la base de datos deben importar este archivo de python
import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",        #el user debe ser el mismo
<<<<<<< HEAD
    password="2383",    #la contraseña varia, si alguien que no soy yo ejecuta el codigo debe cambiar la contraseña
=======
    password="root",    #la contraseña varia, si alguien que no soy yo ejecuta el codigo debe cambiar la contraseña
>>>>>>> 65b5f9d22918852a5af0c603461d3b8d6bb7fe50
    database="rajtir"   #la db, si le pusiste el mismo nombre es el mismo
)

def init_conn():
    cursor = conexion.cursor()

    return cursor


