import os
import bdd
import connector
import validaciones
import hash
from datetime import datetime



def menu_admin():
	while True:
		os.system("cls")
		os.system("color 09")
		print("█▀▄▀█ █▀▀ █▄░█ █░█   █▀█ █▀▄ █▀▄▀█ █ █▄░█ █ █▀ ▀█▀ █▀█ ▄▀█ █▀▄ █▀█ █▀█")
		print("█░▀░█ ██▄ █░▀█ █▄█   █▀█ █▄▀ █░▀░█ █ █░▀█ █ ▄█ ░█░ █▀▄ █▀█ █▄▀ █▄█ █▀▄")
		print("")
		print("1. Bandeja de entrada")
		print("2. Gestión de usuarios")
		print("3. Gestión de clientes")
		print("4. Ver notas de venta")
		print("5. Cerrar sesión")
		try:
			opcion = int(input("Ingrese el número de la opción deseada: "))
			if opcion == 1:
				ver_bandeja_entrada()
			elif opcion == 2:
				gestion_usuarios()
			elif opcion == 3:
				gestion_clientes()
			elif opcion == 4:
				ver_notas_venta()
			elif opcion == 5:
				break
			else:
				print("Opción no válida.")
				os.system("pause")
		except ValueError:
			print("!/ERROR: Por favor, ingrese un número válido.")
			os.system("pause")

def gestion_usuarios():
	while True:
		os.system("cls")
		print("=== GESTIÓN DE USUARIOS ===")
		print("1. Ver usuarios")
		print("2. Insertar usuario")
		print("3. Actualizar usuario")
		print("4. Cambiar rol de un usuario")
		print("5. Desactivar/Activar usuario")
		print("6. Volver")
		try:
			opcion = int(input("Ingrese el número de la opción deseada: "))
			if opcion == 1:
				os.system("cls")
				connector.ver_usuarios()
				os.system("pause")
			elif opcion == 2:
				os.system("cls")
				insertar_usuario()
			elif opcion == 3:
				os.system("cls")
				print("=== USUARIOS REGISTRADOS ===")
				connector.ver_usuarios()
				print("")
				cedula = input("Ingrese la cédula del usuario a actualizar: ")
				validacion = validaciones.validar_cedula(cedula)
				if validacion:
					actualizar_usuario(cedula)
				else:
					print("Cédula inválida.")
					os.system("pause")
			elif opcion == 4:
				cambiar_rol()
			elif opcion == 5:
				desactivar_activar_usuario()
			elif opcion == 6:
				break
			else:
				print("Opción no válida.")
				os.system("pause")
		except ValueError:
			print("!/ERROR: Por favor, ingrese un número válido.")
			os.system("pause")

def actualizar_usuario(cedula):
	while True:
		os.system("cls")
		print("Seleccione el campo a actualizar:")
		print("1. Nombres")
		print("2. Apellidos")
		print("3. Teléfono")
		print("4. Correo electrónico")
		print("5. Dirección")
		print("6. Contraseña")
		print("7. Salir")
		try:
			opcion = int(input("Ingrese el número de la opción deseada: "))
			if opcion == 1:
				os.system("cls")
				nuevo_nombre = input("Ingrese el nuevo nombre: ")
				validacion = validaciones.validar_nombre(nuevo_nombre)
				if validacion:
					query = f"UPDATE usuario SET nombres = '{nuevo_nombre}' WHERE cedula_usuario = '{cedula}';"
					bdd.executar(query)
				else:
					print("Nombre inválido.")
					os.system("pause")
			elif opcion == 2:
				os.system("cls")
				nuevo_apellido = input("Ingrese el nuevo apellido: ")
				validacion = validaciones.validar_nombre(nuevo_apellido)
				if validacion:
					query = f"UPDATE usuario SET apellidos = '{nuevo_apellido}' WHERE cedula_usuario = '{cedula}';"
					bdd.executar(query)
				else:
					print("Apellido inválido.")
					os.system("pause")
			elif opcion == 3:
				os.system("cls")
				nuevo_telefono = input("Ingrese el nuevo teléfono: ")
				validacion = validaciones.validar_celular(nuevo_telefono)
				if validacion:
					query = f"UPDATE usuario SET telefono = '{nuevo_telefono}' WHERE cedula_usuario = '{cedula}';"
					bdd.executar(query)
				else:
					print("Teléfono inválido.")
					os.system("pause")
			elif opcion == 4:
				os.system("cls")
				nuevo_correo = input("Ingrese el nuevo correo: ")
				validacion = validaciones.validar_email(nuevo_correo)
				if validacion:
					query = f"UPDATE usuario SET correo_electronico = '{nuevo_correo}' WHERE cedula_usuario = '{cedula}';"
					bdd.executar(query)
				else:
					print("Correo inválido.")
					os.system("pause")
			elif opcion == 5:
				os.system("cls")
				nueva_direccion = input("Ingrese la nueva dirección: ")
				if nueva_direccion:
					query = f"UPDATE usuario SET direccion = '{nueva_direccion}' WHERE cedula_usuario = '{cedula}';"
					bdd.executar(query)
				else:
					print("Dirección inválida.")
					os.system("pause")
			elif opcion == 6:
				os.system("cls")
				nueva_contrasena = input("Ingrese la nueva contraseña: ")
				validacion = validaciones.validar_contrasena(nueva_contrasena)
				if validacion:
					hashPass = hash.hash_password(nueva_contrasena)
					query = f"UPDATE usuario SET contrasena = '{hashPass}' WHERE cedula_usuario = '{cedula}';"
					bdd.executar(query)
				else:
					print("Contraseña inválida.")
					os.system("pause")
			elif opcion == 7:
				break
			else:
				print("Opción no válida.")
				os.system("pause")
		except ValueError:
			print("!/ERROR: Por favor, ingrese un número válido.")
			os.system("pause")

def insertar_usuario():
	print("\n(Escribe 'volver' en cualquier campo para cancelar)\n")

	while True:
		cedula_usuario = input("Ingrese la cédula (10 dígitos): ").strip()
		if cedula_usuario.lower() == "volver":
			return
		validacion = validaciones.validar_cedula(cedula_usuario)
		if validacion:
			break
		else:
			print("Cédula inválida. Por favor, ingrese una cédula válida.")

	if connector.usuario_existe(cedula_usuario):
		print("Esta cédula ya se encuentra registrada en nuestro sistema.")
		os.system("pause")
		return

	while True:
		nombres_usuario = input("Ingrese los nombres: ").strip()
		if nombres_usuario.lower() == "volver":
			return
		validar_nombres = validaciones.validar_nombre(nombres_usuario)
		if validar_nombres:
			break
		else:
			print("Nombre inválido. Por favor, ingrese un nombre válido.")

	while True:
		apellidos_usuario = input("Ingrese los apellidos: ").strip()
		if apellidos_usuario.lower() == "volver":
			return
		validar_apellidos = validaciones.validar_nombre(apellidos_usuario)
		if validar_apellidos:
			break
		else:
			print("Apellido inválido. Por favor, ingrese un apellido válido.")

	while True:
		telefono_usuario = input("Ingrese el número de celular: ").strip()
		if telefono_usuario.lower() == "volver":
			return
		validar_telefono = validaciones.validar_celular(telefono_usuario)
		if validar_telefono:
			break
		else:
			print("Celular inválido. Por favor, ingrese un número de celular válido.")

	while True:
		correo_usuario = input("Ingrese el correo electrónico: ").strip()
		if correo_usuario.lower() == "volver":
			return
		validar_correo = validaciones.validar_email(correo_usuario)
		if validar_correo:
			break
		else:
			print("Correo inválido. Por favor, ingrese un correo válido.")

	while True:
		direccion_usuario = input("Ingrese la dirección: ").strip()
		if direccion_usuario.lower() == "volver":
			return
		if direccion_usuario:
			break
		else:
			print("Dirección inválida. Por favor, ingrese una dirección válida.")

	while True:
		fecha_nacimiento = input("Ingrese la fecha de nacimiento (DIA-MES-AÑO): ").strip()
		if fecha_nacimiento.lower() == "volver":
			return
		validar_fecha = validaciones.validar_fecha_nacimiento(fecha_nacimiento)
		if validar_fecha:
			break
		else:
			print("Fecha de nacimiento inválida. Por favor, ingrese la fecha en formato (DIA-MES-AÑO).")

	while True:
		password_usuario = input("Ingrese la contraseña: ").strip()
		if password_usuario.lower() == "volver":
			return
		validar_password = validaciones.validar_contrasena(password_usuario)
		if validar_password:
			break
		else:
			print("Contraseña inválida. Debe tener al menos 8 caracteres, mayúscula, minúscula, número y carácter especial.")

	print("\nRoles disponibles:")
	print("1. ADMINISTRADOR")
	print("2. BODEGUERO")
	print("3. VENDEDOR")
	try:
		opcion_rol = int(input("Seleccione el rol: "))
		roles = {1: "ADMINISTRADOR", 2: "BODEGUERO", 3: "VENDEDOR"}
		if opcion_rol not in roles:
			print("Opción no válida.")
			os.system("pause")
			return
		rol_usuario = roles[opcion_rol]
	except ValueError:
		print("Opción inválida.")
		os.system("pause")
		return

	hashPass = hash.hash_password(password_usuario)
	fecha_mysql = datetime.strptime(fecha_nacimiento, "%d-%m-%Y").strftime("%Y-%m-%d")
	query = f"INSERT INTO usuario (cedula_usuario, nombres, apellidos, telefono, correo_electronico, direccion, fecha_nacimiento, contrasena, rol) VALUES ('{cedula_usuario}', '{nombres_usuario}', '{apellidos_usuario}', '{telefono_usuario}', '{correo_usuario}', '{direccion_usuario}', '{fecha_mysql}', '{hashPass}', '{rol_usuario}');"
	bdd.executar(query, mostrar_mensaje=False)
	print("=" * 50)
	print("✓ Usuario registrado correctamente.")
	print("=" * 50)
	os.system("pause")

def cambiar_rol():
	os.system("cls")
	print("=== CAMBIAR ROL DE USUARIO ===")
	print("=== USUARIOS REGISTRADOS ===")
	connector.ver_usuarios()
	print("")
	cedula = input("Ingrese la cédula del usuario: ")
	print("Roles disponibles:")
	print("1. ADMINISTRADOR")
	print("2. BODEGUERO")
	print("3. VENDEDOR")
	try:
		opcion_rol = int(input("Seleccione el nuevo rol: "))
		roles = {1: "ADMINISTRADOR", 2: "BODEGUERO", 3: "VENDEDOR"}
		if opcion_rol in roles:
			query = f"UPDATE usuario SET rol = '{roles[opcion_rol]}' WHERE cedula_usuario = '{cedula}';"
			bdd.executar(query)
		else:
			print("Opción no válida.")
			os.system("pause")
	except ValueError:
		print("!/ERROR: Por favor, ingrese un número válido.")
		os.system("pause")

def desactivar_activar_usuario():
	os.system("cls")
	print("=== DESACTIVAR/ACTIVAR USUARIO ===")
	print("1. Desactivar usuario")
	print("2. Activar usuario")
	print("3. Volver")
	try:
		opcion = int(input("Ingrese el número de la opción deseada: "))
		if opcion == 1:
			os.system("cls")
			print("=== USUARIOS ACTIVOS ===")
			connector.ver_usuarios()
			print("")
			cedula = input("Ingrese la cédula del usuario a desactivar: ")
			validacion = validaciones.validar_cedula(cedula)
			if validacion:
				connector.desactivar_usuario(cedula)
				print("Usuario desactivado correctamente.")
				os.system("pause")
			else:
				print("Cédula inválida.")
				os.system("pause")
		elif opcion == 2:
			os.system("cls")
			print("=== USUARIOS INACTIVOS ===")
			connector.ver_usuarios_inactivos()
			print("")
			cedula = input("Ingrese la cédula del usuario a activar: ")
			validacion = validaciones.validar_cedula(cedula)
			if validacion:
				connector.activar_usuario(cedula)
				print("Usuario activado correctamente.")
				os.system("pause")
			else:
				print("Cédula inválida.")
				os.system("pause")
		elif opcion == 3:
			pass
		else:
			print("Opción no válida.")
			os.system("pause")
	except ValueError:
		print("!/ERROR: Por favor, ingrese un número válido.")
		os.system("pause")

def gestion_clientes():
	while True:
		os.system("cls")
		print("=== GESTIÓN DE CLIENTES ===")
		print("1. Ver clientes")
		print("2. Registrar cliente")
		print("3. Actualizar cliente")
		print("4. Asignar cliente a vendedor")
		print("5. Gestión de productos")
		print("6. Volver")
		try:
			opcion = int(input("Ingrese el número de la opción deseada: "))
			if opcion == 1:
				os.system("cls")
				connector.ver_clientes()
				os.system("pause")
			elif opcion == 2:
				registrar_cliente()
			elif opcion == 3:
				actualizar_cliente()
			elif opcion == 4:
				asignar_cliente_vendedor()
			elif opcion == 5:
				gestion_productos()
			elif opcion == 6:
				break
			else:
				print("Opción no válida.")
				os.system("pause")
		except ValueError:
			print("!/ERROR: Por favor, ingrese un número válido.")
			os.system("pause")

def asignar_cliente_vendedor():
	os.system("cls")
	print("=== ASIGNAR CLIENTE A VENDEDOR ===")
	print("(Escribe 'volver' en cualquier campo para cancelar)\n")
	print("Vendedores disponibles:")
	connector.ver_vendedores()
	print("")

	while True:
		cedula_vendedor = input("Ingrese la cédula del vendedor: ").strip()
		if cedula_vendedor.lower() == "volver":
			return
		validacion = validaciones.validar_cedula(cedula_vendedor)
		if not validacion:
			print("Cédula inválida.")
		elif connector.obtener_rol(cedula_vendedor) != "VENDEDOR":
			print("El usuario no existe o no es vendedor.")
		else:
			break

	os.system("cls")
	print("=== ASIGNAR CLIENTE A VENDEDOR ===")
	print("(Escribe 'volver' para cancelar)\n")
	print("Clientes registrados y su vendedor actual:")
	connector.ver_clientes()
	print("")

	while True:
		cedula_cliente = input("Ingrese la cédula del cliente a asignar: ").strip()
		if cedula_cliente.lower() == "volver":
			return
		validacion = validaciones.validar_cedula(cedula_cliente)
		if not validacion or not connector.cliente_existe(cedula_cliente):
			print("Cédula inválida o cliente no existe.")
		elif connector.cliente_asignado_vendedor(cedula_vendedor, cedula_cliente):
			print("Este cliente ya pertenece a la cartera de ese vendedor.")
			os.system("pause")
		else:
			connector.asignar_cliente_vendedor(cedula_vendedor, cedula_cliente)
			print("=" * 50)
			print("✓ Cliente asignado correctamente.")
			print("=" * 50)
			os.system("pause")
			break

def registrar_cliente():
	os.system("cls")
	print("=== REGISTRAR CLIENTE ===")
	print("(Escribe 'volver' en cualquier campo para cancelar)\n")

	while True:
		cedula = input("Ingrese la cédula del cliente: ").strip()
		if cedula.lower() == "volver":
			return
		validacion = validaciones.validar_cedula(cedula)
		if validacion:
			break
		else:
			print("Cédula inválida. Por favor, ingrese una cédula válida.")

	if connector.cliente_existe(cedula):
		print("Este cliente ya está registrado en el sistema.")
		os.system("pause")
		return

	while True:
		nombres = input("Ingrese los nombres: ").strip()
		if nombres.lower() == "volver":
			return
		validacion = validaciones.validar_nombre(nombres)
		if validacion:
			break
		else:
			print("Nombre inválido. Por favor, ingrese un nombre válido.")

	while True:
		apellidos = input("Ingrese los apellidos: ").strip()
		if apellidos.lower() == "volver":
			return
		validacion = validaciones.validar_nombre(apellidos)
		if validacion:
			break
		else:
			print("Apellido inválido. Por favor, ingrese un apellido válido.")

	while True:
		telefono = input("Ingrese el teléfono: ").strip()
		if telefono.lower() == "volver":
			return
		validacion = validaciones.validar_celular(telefono)
		if validacion:
			break
		else:
			print("Teléfono inválido. Por favor, ingrese un teléfono válido.")

	while True:
		correo = input("Ingrese el correo electrónico: ").strip()
		if correo.lower() == "volver":
			return
		validacion = validaciones.validar_email(correo)
		if validacion:
			break
		else:
			print("Correo inválido. Por favor, ingrese un correo válido.")

	while True:
		direccion = input("Ingrese la dirección: ").strip()
		if direccion.lower() == "volver":
			return
		if direccion:
			break
		else:
			print("Dirección inválida. Por favor, ingrese una dirección válida.")

	while True:
		fecha_nacimiento = input("Ingrese la fecha de nacimiento (DIA-MES-AÑO): ").strip()
		if fecha_nacimiento.lower() == "volver":
			return
		validacion = validaciones.validar_fecha_nacimiento(fecha_nacimiento)
		if validacion:
			break
		else:
			print("Fecha inválida. Debe tener formato (DIA-MES-AÑO) y el cliente debe ser mayor de edad.")

	fecha_mysql = datetime.strptime(fecha_nacimiento, "%d-%m-%Y").strftime("%Y-%m-%d")

	connector.insertar_cliente(cedula, nombres, apellidos, telefono, correo, direccion, fecha_mysql)
	print("=" * 50)
	print("✓ Cliente registrado correctamente.")
	print("=" * 50)
	os.system("pause")

def actualizar_cliente():
	os.system("cls")
	print("=== ACTUALIZAR CLIENTE ===")
	print("Clientes registrados:")
	connector.ver_clientes()
	print("")

	while True:
		cedula = input("Ingrese la cédula del cliente a actualizar: ")
		validacion = validaciones.validar_cedula(cedula)
		if validacion:
			break
		else:
			print("Cédula inválida. Por favor, ingrese una cédula válida.")

	while True:
		os.system("cls")
		print("Seleccione el campo a actualizar:")
		print("1. Nombres")
		print("2. Apellidos")
		print("3. Teléfono")
		print("4. Correo electrónico")
		print("5. Dirección")
		print("6. Fecha de nacimiento")
		print("7. Salir")
		try:
			opcion = int(input("Ingrese el número de la opción deseada: "))
			if opcion == 1:
				os.system("cls")
				nuevo_nombre = input("Ingrese el nuevo nombre: ")
				validacion = validaciones.validar_nombre(nuevo_nombre)
				if validacion:
					query = f"UPDATE cliente SET nombres = '{nuevo_nombre}' WHERE cedula_cliente = '{cedula}';"
					bdd.executar(query)
				else:
					print("Nombre inválido.")
					os.system("pause")
			elif opcion == 2:
				os.system("cls")
				nuevo_apellido = input("Ingrese el nuevo apellido: ")
				validacion = validaciones.validar_nombre(nuevo_apellido)
				if validacion:
					query = f"UPDATE cliente SET apellidos = '{nuevo_apellido}' WHERE cedula_cliente = '{cedula}';"
					bdd.executar(query)
				else:
					print("Apellido inválido.")
					os.system("pause")
			elif opcion == 3:
				os.system("cls")
				nuevo_telefono = input("Ingrese el nuevo teléfono: ")
				validacion = validaciones.validar_celular(nuevo_telefono)
				if validacion:
					query = f"UPDATE cliente SET telefono = '{nuevo_telefono}' WHERE cedula_cliente = '{cedula}';"
					bdd.executar(query)
				else:
					print("Teléfono inválido.")
					os.system("pause")
			elif opcion == 4:
				os.system("cls")
				nuevo_correo = input("Ingrese el nuevo correo: ")
				validacion = validaciones.validar_email(nuevo_correo)
				if validacion:
					query = f"UPDATE cliente SET correo_electronico = '{nuevo_correo}' WHERE cedula_cliente = '{cedula}';"
					bdd.executar(query)
				else:
					print("Correo inválido.")
					os.system("pause")
			elif opcion == 5:
				os.system("cls")
				nueva_direccion = input("Ingrese la nueva dirección: ")
				if nueva_direccion:
					query = f"UPDATE cliente SET direccion = '{nueva_direccion}' WHERE cedula_cliente = '{cedula}';"
					bdd.executar(query)
				else:
					print("Dirección inválida.")
					os.system("pause")
			elif opcion == 6:
				os.system("cls")
				nueva_fecha = input("Ingrese la nueva fecha de nacimiento (DIA-MES-AÑO): ").strip()
				validacion = validaciones.validar_fecha_nacimiento(nueva_fecha)
				if validacion:
					fecha_mysql = datetime.strptime(nueva_fecha, "%d-%m-%Y").strftime("%Y-%m-%d")
					query = f"UPDATE cliente SET fecha_nacimiento = '{fecha_mysql}' WHERE cedula_cliente = '{cedula}';"
					bdd.executar(query)
				else:
					print("Fecha inválida. Debe tener formato (DIA-MES-AÑO) y el cliente debe ser mayor de edad.")
					os.system("pause")
			elif opcion == 7:
				break
			else:
				print("Opción no válida.")
				os.system("pause")
		except ValueError:
			print("!/ERROR: Por favor, ingrese un número válido.")
			os.system("pause")

def gestion_productos():
	while True:
		os.system("cls")
		print("=== GESTIÓN DE PRODUCTOS ===")
		print("1. Ver productos activos")
		print("2. Ver productos inactivos")
		print("3. Desactivar/Activar producto")
		print("4. Volver")
		try:
			opcion = int(input("Ingrese el número de la opción deseada: "))
			if opcion == 1:
				os.system("cls")
				connector.ver_productos()
				os.system("pause")
			elif opcion == 2:
				os.system("cls")
				connector.ver_productos_inactivos()
				os.system("pause")
			elif opcion == 3:
				desactivar_activar_producto()
			elif opcion == 4:
				break
			else:
				print("Opción no válida.")
				os.system("pause")
		except ValueError:
			print("!/ERROR: Por favor, ingrese un número válido.")
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
	print("=== BANDEJA DE ENTRADA ===")
	connector.mostrar_alertas_stock()
	os.system("pause")

def ver_notas_venta():
	while True:
		os.system("cls")
		print("=== NOTAS DE VENTA DEL SISTEMA ===")
		connector.ver_todas_facturas()
		print("")
		numero = input("Ingrese el N° de nota de venta para ver el detalle ('volver' para salir): ").strip()
		if numero.lower() == "volver":
			return
		if not numero.isdigit():
			print("Ingrese un número válido.")
			os.system("pause")
			continue
		os.system("cls")
		if not connector.mostrar_nota_venta(int(numero)):
			os.system("pause")
			continue
		os.system("pause")
