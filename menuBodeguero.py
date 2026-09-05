import os
import connector
import bdd
import validaciones



def menu_bodeguero():
	while True:
		os.system("cls")
		os.system("color 0E")
		print("█▀▄▀█ █▀▀ █▄░█ █░█   █▄▄ █▀█ █▀▄ █▀▀ █▀▀ █░█ █▀▀ █▀█ █▀█")
		print("█░▀░█ ██▄ █░▀█ █▄█   █▄█ █▄█ █▄▀ ██▄ █▄█ █▄█ ██▄ █▀▄ █▄█")
		print("")
		print("1. Bandeja de entrada (Stock bajo)")
		print("2. Control de stock")
		print("3. Cerrar sesión")
		try:
			opcion = int(input("Ingrese el número de la opción deseada: "))
			if opcion == 1:
				ver_bandeja_entrada()
			elif opcion == 2:
				control_stock()
			elif opcion == 3:
				break
			else:
				print("Opción no válida.")
				os.system("pause")
		except ValueError:
			print("!/ERROR: Por favor, ingrese un número válido.")
			os.system("pause")


def control_stock():
	while True:
		os.system("cls")
		print("=== CONTROL DE STOCK (CRUD productos) ===")
		print("1. Ver productos")
		print("2. Insertar producto")
		print("3. Actualizar producto")
		print("4. Desactivar/Activar producto")
		print("5. Volver")
		try:
			opcion = int(input("Ingrese el número de la opción deseada: "))
			if opcion == 1:
				os.system("cls")
				connector.ver_productos()
				os.system("pause")
			elif opcion == 2:
				insertar_producto()
			elif opcion == 3:
				actualizar_producto()
			elif opcion == 4:
				desactivar_activar_producto()
			elif opcion == 5:
				break
			else:
				print("Opción no válida.")
				os.system("pause")
		except ValueError:
			print("!/ERROR: Por favor, ingrese un valor válido.")
			os.system("pause")

def insertar_producto():
	os.system("cls")
	print("=== INSERTAR PRODUCTO ===")
	print("(Escribe 'volver' en cualquier campo para cancelar)\n")
	print("Ejemplo de productos ya registrados, como referencia:")
	connector.ver_muestra_productos(5)
	print("")

	while True:
		codigo = input("Código de producto (máximo 6 caracteres, ej. P00007): ").strip().upper()

		if codigo.lower() == "volver":
			return

		if not codigo:
			respuesta = input("No se ha ingresado ningún código. ¿Desea continuar? (s/n): ").strip().lower()
			if respuesta == "n":
				return
			else:
				os.system("cls")
				print("=== INSERTAR PRODUCTO ===")
				print("(Escribe 'volver' en cualquier campo para cancelar)\n")
				print("Ejemplo de productos ya registrados, como referencia:")
				connector.ver_muestra_productos(5)
				print("")
				continue

		if len(codigo) > 6:
			print("El código no puede ser mayor a 6 caracteres. Por favor, ingrese un código válido.")
			os.system("pause")
			os.system("cls")
			print("=== INSERTAR PRODUCTO ===")
			print("(Escribe 'volver' en cualquier campo para cancelar)\n")
			print("Ejemplo de productos ya registrados, como referencia:")
			connector.ver_muestra_productos(5)
			print("")
			continue

		if connector.producto_existe(codigo):
			print("Este producto ya existe en el sistema.")
			os.system("pause")
			os.system("cls")
			print("=== INSERTAR PRODUCTO ===")
			print("(Escribe 'volver' en cualquier campo para cancelar)\n")
			print("Ejemplo de productos ya registrados, como referencia:")
			connector.ver_muestra_productos(5)
			print("")
		else:
			break

	while True:
		nombre = input("Nombre del producto: ").strip()
		if nombre.lower() == "volver":
			return
		if nombre:
			break
		else:
			print("Nombre inválido. Por favor, ingrese un nombre válido.")

	while True:
		try:
			cantidad_input = input("Cantidad inicial: ").strip()
			if cantidad_input.lower() == "volver":
				return
			cantidad = int(cantidad_input)
			if cantidad >= 0:
				break
			else:
				print("La cantidad debe ser mayor o igual a 0.")
		except ValueError:
			print("Cantidad inválida.")

	descripcion = input("Descripción del producto (opcional): ").strip()
	if descripcion.lower() == "volver":
		return

	while True:
		try:
			costo_input = input("Costo: ").strip()
			if costo_input.lower() == "volver":
				return
			costo = float(costo_input)
			if costo > 0:
				break
			else:
				print("El costo debe ser mayor a 0.")
		except ValueError:
			print("Costo inválido.")

	connector.insertar_producto(codigo, nombre, cantidad, descripcion, costo)
	print("=" * 50)
	print("✓ Producto insertado correctamente.")
	print("=" * 50)
	os.system("pause")

def actualizar_producto():
	os.system("cls")
	print("=== ACTUALIZAR PRODUCTO ===")

	while True:
		connector.ver_productos()
		print("")
		codigo = input("Ingrese el código del producto a actualizar: ").strip().upper()

		if not codigo:
			print("El código no puede estar vacío. Por favor, ingrese un código válido.")
			os.system("pause")
			os.system("cls")
			continue

		if not connector.producto_existe(codigo):
			print("El producto no existe en el sistema.")
			os.system("pause")
			os.system("cls")
			continue

		break

	print("")
	print("Campos disponibles:")
	print("1) nombre_producto")
	print("2) cantidad")
	print("3) descripcion")
	print("4) costo")
	campos = {1: "nombre_producto", 2: "cantidad", 3: "descripcion", 4: "costo"}
	try:
		opcion_campo = int(input("Seleccione el campo a actualizar: "))
	except ValueError:
		print("!/ERROR: Por favor, ingrese un número válido.")
		os.system("pause")
		return

	campo = campos.get(opcion_campo)
	if campo is None:
		print("Opción no válida.")
		os.system("pause")
		return

	valor = input("Ingrese el nuevo valor: ")
	connector.actualizar_producto(codigo, campo, valor)
	os.system("pause")

def desactivar_activar_producto():
	os.system("cls")
	print("=== DESACTIVAR/ACTIVAR PRODUCTO ===")
	print("1. Desactivar producto")
	print("2. Activar producto")
	print("3. Volver")
	try:
		opcion = int(input("Ingrese el número de la opción deseada: "))
		if opcion == 1:
			os.system("cls")
			print("=== PRODUCTOS ACTIVOS ===")
			connector.ver_productos()
			print("")
			codigo = input("Ingrese el código del producto a desactivar: ").strip().upper()
			if connector.producto_existe(codigo):
				connector.desactivar_producto(codigo)
				print("Producto desactivado correctamente.")
				os.system("pause")
			else:
				print("Código inválido o producto no existe.")
				os.system("pause")
		elif opcion == 2:
			os.system("cls")
			print("=== PRODUCTOS INACTIVOS ===")
			connector.ver_productos_inactivos()
			print("")
			codigo = input("Ingrese el código del producto a activar: ").strip().upper()
			if connector.producto_existe(codigo):
				connector.activar_producto(codigo)
				print("Producto activado correctamente.")
				os.system("pause")
			else:
				print("Código inválido o producto no existe.")
				os.system("pause")
		elif opcion == 3:
			pass
		else:
			print("Opción no válida.")
			os.system("pause")
	except ValueError:
		print("!/ERROR: Por favor, ingrese un número válido.")
		os.system("pause")

def ver_bandeja_entrada():
	os.system("cls")
	print("=== BANDEJA DE ENTRADA - STOCK BAJO ===")
	connector.mostrar_alertas_stock()
	os.system("pause")
