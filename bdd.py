<<<<<<< HEAD
import mysql.connector, os
from tabulate import tabulate

def conectar():
	return mysql.connector.connect(
		host="localhost",
		user="root",
		password="root",
		database="importadorajj",
		auth_plugin='mysql_native_password'
	)

def executar(query, mostrar_mensaje=True):
	try:
		conexion = conectar()
		cursor = conexion.cursor()
		cursor.execute(query)
		conexion.commit()
		if mostrar_mensaje:
			print("Operación realizada con éxito.")
			os.system("pause")
	except Exception as e:
		print(f"Error al realizar operación: {e}")
		os.system("pause")
	finally:
		if conexion.is_connected():
			cursor.close()
			conexion.close()
=======
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


>>>>>>> 5a72e7ec9126216e70b7ab3b8a7123ad42060b0c

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

<<<<<<< HEAD
def consulta(query):
	try:
		conexion = conectar()
		cursor = conexion.cursor()
		cursor.execute(query)
		resultados = cursor.fetchall()
		return resultados
	except Exception as e:
		print(f"Error al consultar datos: {e}")
	finally:
		if conexion.is_connected():
			cursor.close()
			conexion.close()
=======
#select("select * from users;")
>>>>>>> 5a72e7ec9126216e70b7ab3b8a7123ad42060b0c


