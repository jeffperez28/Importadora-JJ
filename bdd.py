import mysql.connector
import os
from tabulate import tabulate

def conectar():
		return mysql.connector.connect(
			host="localhost",
			user="root",
			password="root",
			database="importadorajj",
			auth_plugin='mysql_native_password'
		)

def inicioSesion(usuario, password):
    miConexion = conectar()
    cursor = miConexion.cursor()
    cursor.execute(f"select * from users where name_user like '{usuario}' and password like'{password}';")
    resultado = cursor.fetchone()
    if resultado:
        print("Acceso concedido")
        os.system("pause")
        return True
    else:
        print("Usuario o contraseña incorrectos")
        os.system("pause")
        return False

#inicioSesion("admin", "1234") #-- Estoy invocando la funcion para probarla si esta funcionando 



def select(query):
	try:
		conexion = conectar()
		cursor = conexion.cursor()
		cursor.execute(query)
		resultados = cursor.fetchall()
		columnas = cursor.column_names
		print(tabulate(resultados, headers=columnas, tablefmt='grid'))
		return resultados
	except Exception as e:
		print(f"Error al consultar datos: {e}")
	finally:
		if conexion.is_connected():
			cursor.close()
			conexion.close()

#select("select * from users;")


