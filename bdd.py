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


