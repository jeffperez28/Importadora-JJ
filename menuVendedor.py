<<<<<<< HEAD
import os
import connector
import bdd
import validaciones
from datetime import datetime



def menu_vendedor(cedula_usuario):
	while True:
		os.system("cls")
		os.system("color 0A")
		print("█▀▄▀█ █▀▀ █▄░█ █░█   █░█ █▀▀ █▄░█ █▀▄ █▀▀ █▀▄ █▀█ █▀█")
		print("█░▀░█ ██▄ █░▀█ █▄█   ▀▄▀ ██▄ █░▀█ █▄▀ ██▄ █▄▀ █▄█ █▀▄")
		print("")
		print("1. Control de stock (consulta)")
		print("2. Gestión de clientes")
		print("3. Emisión de notas de venta")
		print("4. Ver mis notas de venta")
		print("5. Cerrar sesión")
		try:
			opcion = int(input("Ingrese el número de la opción deseada: "))
			if opcion == 1:
				os.system("cls")
				connector.ver_productos()
				os.system("pause")
			elif opcion == 2:
				gestion_clientes_vendedor(cedula_usuario)
			elif opcion == 3:
				emision_facturas(cedula_usuario)
			elif opcion == 4:
				ver_mis_notas_venta(cedula_usuario)
			elif opcion == 5:
				break
			else:
				print("Opción no válida.")
				os.system("pause")
		except ValueError:
			print("!/ERROR: Por favor, ingrese un número válido.")
			os.system("pause")

def cabecera_facturacion():
	os.system("cls")
	print("█▀▀ █▀▄▀█ █ █▀▀ █ █▀█ █▄░█   █▀▄ █▀▀   █▀▀ ▄▀█ █▀▀ ▀█▀ █░█ █▀█ █▀█ █▀")
	print("██▄ █░▀░█ █ ▄▄█ █ █▄█ █░▀█   █▄▀ ██▄   █▀░ █▀█ █▄▄ ░█░ █▄█ █▀▄ █▀█ ▄█")
	print("")
	print("CLIENTES REGISTRADOS EN EL SISTEMA:")
	connector.ver_todos_clientes_activos()
	print("\n" + "="*75 + "\n")

def emision_facturas(cedula_usuario):
	cabecera_facturacion()

	while True:
		cedula_cliente = input("Ingrese la cédula del cliente ('volver' para cancelar): ").strip()

		if cedula_cliente.lower() == "volver":
			return

		cliente = connector.obtener_cliente(cedula_cliente)
		if cliente is None:
			print("No existe ningún cliente con esa cédula.")
			os.system("pause")
			cabecera_facturacion()
			continue

		nombres_cliente, apellidos_cliente = cliente
		print(f"\n✓ Cliente: {nombres_cliente} {apellidos_cliente} | Cédula: {cedula_cliente}\n")
		break

	carrito = []

	while True:
		os.system("cls")
		print("█▀▀ █▀▄▀█ █ █▀▀ █ █▀█ █▄░█   █▀▄ █▀▀   █▀▀ ▄▀█ █▀▀ ▀█▀ █░█ █▀█ █▀█ █▀")
		print("██▄ █░▀░█ █ ▄▄█ █ █▄█ █░▀█   █▄▀ ██▄   █▀░ █▀█ █▄▄ ░█░ █▄█ █▀▄ █▀█ ▄█")
		print("")
		print(f"Cliente: {nombres_cliente} {apellidos_cliente} | Cédula: {cedula_cliente}")
		print("")
		print("Productos disponibles:")
		connector.ver_productos()
		print("")

		while True:
			codigo_producto = input("Ingrese el código del producto: ").strip().upper()

			if not codigo_producto:
				respuesta = input("No se ha ingresado ningún código. ¿Desea continuar? (s/n): ").strip().lower()
				if respuesta == "n":
					break
				else:
					continue

			respuesta = input("¿Desea continuar con este código? (s/n): ").strip().lower()
			if respuesta == "s":
				break
			else:
				continue

		if not codigo_producto:
			break

		producto = connector.obtener_producto(codigo_producto)
		if producto is None:
			print("No existe un producto con ese código.")
			respuesta = input("¿Desea continuar? (s/n): ").strip().lower()
			if respuesta != "s":
				break
			os.system("cls")
			continue

		cod, nombre, cantidad_stock, costo = producto
		print(f"Producto: {nombre} | Precio: ${costo} | Stock disponible: {cantidad_stock}")

		respuesta = input("¿Desea continuar con este producto? (s/n): ").strip().lower()
		if respuesta != "s":
			os.system("cls")
			continue

		if cantidad_stock <= 0:
			print("Este producto no tiene stock disponible.")
			os.system("pause")
			os.system("cls")
			continue

		try:
			cantidad = int(input("Ingrese la cantidad: "))
		except ValueError:
			print("Cantidad inválida.")
			os.system("pause")
			os.system("cls")
			continue

		if cantidad <= 0:
			print("La cantidad debe ser mayor a 0.")
			os.system("pause")
			os.system("cls")
			continue

		if cantidad > cantidad_stock:
			print(f"No hay suficiente stock. Solo quedan {cantidad_stock} unidades.")
			os.system("pause")
			os.system("cls")
			continue

		print(f"¿Desea continuar con esta cantidad? (s/n): ")
		respuesta = input().strip().lower()
		if respuesta != "s":
			os.system("cls")
			continue

		subtotal = float(costo) * cantidad

		carrito.append((cod, nombre, cantidad, float(costo), subtotal))
		print(f"Se agregó: {cantidad} x {nombre} = ${subtotal:.2f}")

		respuesta = input("¿Desea agregar otro producto? (s/n): ").strip().lower()
		os.system("cls")
		if respuesta != "s":
			break

	if not carrito:
		print("No se agregó ningún producto. Factura cancelada.")
		os.system("pause")
		return

	total = sum(subtotal for _, _, _, _, subtotal in carrito)

	id_factura = connector.crear_factura(cedula_cliente, cedula_usuario, total)
	if id_factura is None:
		print("No se pudo registrar la nota de venta en la base de datos. Se cancela la operación.")
		os.system("pause")
		return

	for cod, nombre, cantidad, precio_unitario, subtotal in carrito:
		connector.descontar_stock(cod, cantidad)
		connector.insertar_detalle_factura(id_factura, cod, cantidad, precio_unitario, subtotal)

	os.system("cls")
	connector.mostrar_nota_venta(id_factura)
	print("\nGracias por su compra. Su nota de venta ha sido registrada en el sistema.")
	os.system("pause")

def gestion_clientes_vendedor(cedula_vendedor):
	while True:
		os.system("cls")
		print("=== GESTIÓN DE MI CARTERA DE CLIENTES ===")
		print("1. Ver mis clientes")
		print("2. Tomar cliente sin asignar")
		print("3. Registrar nuevo cliente")
		print("4. Actualizar cliente")
		print("5. Desactivar/Activar cliente")
		print("6. Volver")
		try:
			opcion = int(input("Ingrese el número de la opción deseada: "))
			if opcion == 1:
				os.system("cls")
				connector.ver_clientes_vendedor(cedula_vendedor)
				os.system("pause")
			elif opcion == 2:
				buscar_asignar_cliente_vendedor(cedula_vendedor)
			elif opcion == 3:
				registrar_cliente_vendedor(cedula_vendedor)
			elif opcion == 4:
				actualizar_cliente_vendedor(cedula_vendedor)
			elif opcion == 5:
				desactivar_activar_cliente_vendedor(cedula_vendedor)
			elif opcion == 6:
				break
			else:
				print("Opción no válida.")
				os.system("pause")
		except ValueError:
			print("!/ERROR: Por favor, ingrese un número válido.")
			os.system("pause")

def buscar_asignar_cliente_vendedor(cedula_vendedor):
	os.system("cls")
	print("=== TOMAR CLIENTE SIN ASIGNAR ===")
	print("\nClientes que no pertenecen a ninguna cartera:")
	connector.ver_clientes_sin_asignar()
	print("")

	while True:
		cedula = input("Ingrese la cédula del cliente ('volver' para cancelar): ").strip()
		if cedula.lower() == "volver":
			return
		validacion = validaciones.validar_cedula(cedula)
		if validacion:
			break
		else:
			print("Cédula inválida. Por favor, ingrese una cédula válida.")

	if not connector.cliente_existe(cedula):
		print("Este cliente no existe en el sistema.")
		os.system("pause")
		return

	vendedor_actual = connector.obtener_vendedor_cliente(cedula)
	if vendedor_actual is not None:
		if vendedor_actual == cedula_vendedor:
			print("Este cliente ya está en su cartera.")
		else:
			print("Este cliente pertenece a la cartera de otro vendedor.")
			print("Solicite al administrador que se lo reasigne.")
		os.system("pause")
		return

	connector.asignar_cliente_vendedor(cedula_vendedor, cedula)
	print("=" * 50)
	print("✓ Cliente agregado a su cartera.")
	print("=" * 50)
	os.system("pause")

def registrar_cliente_vendedor(cedula_vendedor):
	os.system("cls")
	print("=== REGISTRAR NUEVO CLIENTE ===")
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
		print("Intente asignárselo desde 'Buscar cliente existente'.")
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

	connector.insertar_cliente(cedula, nombres, apellidos, telefono, correo, direccion, fecha_mysql, cedula_vendedor)
	os.system("cls")
	print("=" * 50)
	print("✓ Cliente registrado y agregado a su cartera.")
	print("=" * 50)
	os.system("pause")

def actualizar_cliente_vendedor(cedula_vendedor):
	os.system("cls")
	print("=== ACTUALIZAR CLIENTE ===")
	print("Mis clientes:")
	connector.ver_clientes_vendedor(cedula_vendedor)
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
					connector.actualizar_cliente_vendedor(cedula_vendedor, cedula, "nombres", nuevo_nombre)
				else:
					print("Nombre inválido.")
					os.system("pause")
			elif opcion == 2:
				os.system("cls")
				nuevo_apellido = input("Ingrese el nuevo apellido: ")
				validacion = validaciones.validar_nombre(nuevo_apellido)
				if validacion:
					connector.actualizar_cliente_vendedor(cedula_vendedor, cedula, "apellidos", nuevo_apellido)
				else:
					print("Apellido inválido.")
					os.system("pause")
			elif opcion == 3:
				os.system("cls")
				nuevo_telefono = input("Ingrese el nuevo teléfono: ")
				validacion = validaciones.validar_celular(nuevo_telefono)
				if validacion:
					connector.actualizar_cliente_vendedor(cedula_vendedor, cedula, "telefono", nuevo_telefono)
				else:
					print("Teléfono inválido.")
					os.system("pause")
			elif opcion == 4:
				os.system("cls")
				nuevo_correo = input("Ingrese el nuevo correo: ")
				validacion = validaciones.validar_email(nuevo_correo)
				if validacion:
					connector.actualizar_cliente_vendedor(cedula_vendedor, cedula, "correo_electronico", nuevo_correo)
				else:
					print("Correo inválido.")
					os.system("pause")
			elif opcion == 5:
				os.system("cls")
				nueva_direccion = input("Ingrese la nueva dirección: ")
				if nueva_direccion:
					connector.actualizar_cliente_vendedor(cedula_vendedor, cedula, "direccion", nueva_direccion)
				else:
					print("Dirección inválida.")
					os.system("pause")
			elif opcion == 6:
				os.system("cls")
				nueva_fecha = input("Ingrese la nueva fecha de nacimiento (DIA-MES-AÑO): ").strip()
				validacion = validaciones.validar_fecha_nacimiento(nueva_fecha)
				if validacion:
					fecha_mysql = datetime.strptime(nueva_fecha, "%d-%m-%Y").strftime("%Y-%m-%d")
					connector.actualizar_cliente_vendedor(cedula_vendedor, cedula, "fecha_nacimiento", fecha_mysql)
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

def desactivar_activar_cliente_vendedor(cedula_vendedor):
	os.system("cls")
	print("=== DESACTIVAR/ACTIVAR CLIENTE ===")
	print("1. Desactivar cliente")
	print("2. Activar cliente")
	print("3. Volver")
	try:
		opcion = int(input("Ingrese el número de la opción deseada: "))
		if opcion == 1:
			os.system("cls")
			print("=== MIS CLIENTES ACTIVOS ===")
			connector.ver_clientes_vendedor(cedula_vendedor)
			print("")
			cedula = input("Ingrese la cédula del cliente a desactivar: ")
			validacion = validaciones.validar_cedula(cedula)
			if validacion:
				connector.desactivar_cliente_vendedor(cedula_vendedor, cedula)
			else:
				print("Cédula inválida.")
				os.system("pause")
		elif opcion == 2:
			os.system("cls")
			print("=== MIS CLIENTES INACTIVOS ===")
			connector.ver_clientes_vendedor_inactivos(cedula_vendedor)
			print("")
			cedula = input("Ingrese la cédula del cliente a activar: ")
			validacion = validaciones.validar_cedula(cedula)
			if validacion:
				connector.activar_cliente_vendedor(cedula_vendedor, cedula)
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

def ver_mis_notas_venta(cedula_vendedor):
	while True:
		os.system("cls")
		print("=== MIS NOTAS DE VENTA ===")
		connector.ver_facturas_vendedor(cedula_vendedor)
		print("")
		numero = input("Ingrese el N° de nota de venta para ver el detalle ('volver' para salir): ").strip()
		if numero.lower() == "volver":
			return
		if not numero.isdigit():
			print("Ingrese un número válido.")
			os.system("pause")
			continue

		info = connector.obtener_factura_info(int(numero))
		if info is None or info[2] != cedula_vendedor:
			print("Esa nota de venta no existe o no le pertenece.")
			os.system("pause")
			continue

		os.system("cls")
		connector.mostrar_nota_venta(int(numero))
		os.system("pause")
=======
import os, connector

def menu_vendedor():
    while True:
        os.system("cls")
        os.system("color 0A")
        print("█▀▄▀█ █▀▀ █▄░█ █░█   █░█ █▀▀ █▄░█ █▀▄ █▀▀ █▀▄ █▀█ █▀█")
        print("█░▀░█ ██▄ █░▀█ █▄█   ▀▄▀ ██▄ █░▀█ █▄▀ ██▄ █▄▀ █▄█ █▀▄")
        print("")
        print("1. Control de stock (consulta)")
        print("2. Emisión de facturas")
        print("3. Cerrar sesión")
        try:
            opcion = int(input("Ingrese el número de la opción deseada: "))
            if opcion == 1:
                os.system("cls")
                connector.ver_productos()
                os.system("pause")
            elif opcion == 2:
                emision_facturas()
            elif opcion == 3:
                break
            else:
                print("Opción no válida.")
                os.system("pause")
        except ValueError:
            print("!/ERROR: Por favor, ingrese un número válido.")
            os.system("pause")


def emision_facturas():
    os.system("cls")
    print("█▀▀ █▀▄▀█ █ █▀▀ █ █▀█ █▄░█   █▀▄ █▀▀   █▀▀ ▄▀█ █▀▀ ▀█▀ █░█ █▀█ █▀█ █▀")
    print("██▄ █░▀░█ █ ▄▄█ █ █▄█ █░▀█   █▄▀ ██▄   █▀░ █▀█ █▄▄ ░█░ █▄█ █▀▄ █▀█ ▄█")
    print(" ")
    print("CLIENTES REGISTRADOS EN EL SISTEMA: ")
    connector.ver_usuarios()
    print("\n" + "="*75 + "\n")

    while True:
        cedula_cliente = input("Ingrese la cédula del cliente registrado: ").strip()
        cliente = connector.obtener_cliente(cedula_cliente)
        if cliente is None:
            print("No existe ningún cliente registrado con esa cédula.")
            os.system("pause")
            os.system("cls")
            print("█▀▀ █▀▄▀█ █ █▀▀ █ █▀█ █▄░█   █▀▄ █▀▀   █▀▀ ▄▀█ █▀▀ ▀█▀ █░█ █▀█ █▀█ █▀")
            print("██▄ █░▀░█ █ ▄▄█ █ █▄█ █░▀█   █▄▀ ██▄   █▀░ █▀█ █▄▄ ░█░ █▄█ █▀▄ █▀█ ▄█")
            print("")
            print(" CLIENTES REGISTRADOS EN EL SISTEMA: ")
            connector.ver_usuarios()
            print("\n" + "="*75 + "\n")
            continue
        nombres_cliente, apellidos_cliente = cliente
        print(f"\n✓ Cliente: {nombres_cliente} {apellidos_cliente} | Cédula: {cedula_cliente}\n")
        break

    carrito = []  # Lista temporal en memoria: cada item es (codigo, nombre, cantidad, precio_unitario, subtotal)

    while True:
        os.system("cls")
        print("█▀▀ █▀▄▀█ █ █▀▀ █ █▀█ █▄░█   █▀▄ █▀▀   █▀▀ ▄▀█ █▀▀ ▀█▀ █░█ █▀█ █▀█ █▀")
        print("██▄ █░▀░█ █ ▄▄█ █ █▄█ █░▀█   █▄▀ ██▄   █▀░ █▀█ █▄▄ ░█░ █▄█ █▀▄ █▀█ ▄█")
        print("")
        print(f"Cliente: {nombres_cliente} {apellidos_cliente} | Cédula: {cedula_cliente}")
        print("")
        print("Productos disponibles:")
        connector.ver_productos()
        print("")
        codigo = input("Ingrese el código del producto: ").strip().upper() #.strip().upper() limpia espacios al inicio/final y convierte el texto a mayúsculas

        # --- Validación temprana: se comprueba primero si el producto existe ---
        # antes de pedir cualquier otro dato (cantidad, etc.)
        producto = connector.obtener_producto(codigo)
        if producto is None:
            print("No existe un producto con ese código.")
            os.system("pause")
            os.system("cls")
            continue

        cod, nombre, unidad, costo, descuento, stock = producto
        print(f"Producto: {nombre} | Precio: ${costo} | Descuento: {descuento}% | Stock disponible: {stock}")

        if stock <= 0:
            print("Este producto no tiene stock disponible.")
            os.system("pause")
            os.system("cls")
            continue

        try:
            cantidad = int(input(f"Ingrese la cantidad ({unidad}): "))
        except ValueError:
            print("Cantidad inválida.")
            os.system("pause")
            os.system("cls")
            continue

        if cantidad <= 0:
            print("La cantidad debe ser mayor a 0.")
            os.system("pause")
            os.system("cls")
            continue

        if cantidad > stock:
            print(f"No hay suficiente stock. Solo quedan {stock} unidades.")
            os.system("pause")
            os.system("cls")
            continue

        precio_con_descuento = float(costo) * (1 - float(descuento) / 100)
        subtotal = precio_con_descuento * cantidad

        carrito.append((cod, nombre, cantidad, precio_con_descuento, subtotal))
        print(f"Se agregó: {cantidad} x {nombre} = ${subtotal:.2f}")

        respuesta = input("¿Desea agregar otro producto? (s/n): ").strip().lower()
        os.system("cls")
        if respuesta != "s":
            break

    if not carrito:
        print("No se agregó ningún producto. Factura cancelada.")
        os.system("pause")
        return

    # Se calcula el total antes de guardar, porque la cabecera de la factura lo necesita
    total = sum(subtotal for _, _, _, _, subtotal in carrito)

    # Se registra primero la cabecera de la factura (queda en la tabla 'facturas')
    id_factura = connector.crear_factura(cedula_cliente, total)
    if id_factura is None:
        print("No se pudo registrar la factura en la base de datos. Se cancela la operación.")
        os.system("pause")
        return

    # Cierre de la factura: se descuenta el stock real, se guarda el detalle y se muestra el resumen
    print("=" * 75)
    print("RESUMEN DE SU FACTURA")
    print("=" * 75)
    print(f"Factura N°: {id_factura}")
    print(f"Cliente: {nombres_cliente} {apellidos_cliente} | Cédula: {cedula_cliente}")
    print(f"Fecha: {__import__('datetime').datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("\n" + "-" * 75)
    print(f"{'Código':<10}{'Producto':<35}{'Cant.':<8}{'P. Unit.':<12}{'Subtotal':<10}")
    print("-" * 75)
    
    for cod, nombre, cantidad, precio_unitario, subtotal in carrito:
        print(f"{cod:<10}{nombre:<35}{cantidad:<8}{precio_unitario:<12.2f}{subtotal:<10.2f}")
        connector.descontar_stock(cod, cantidad)
        connector.insertar_detalle_factura(id_factura, cod, cantidad, precio_unitario, subtotal)

    print("-" * 75)
    
    # Cálculo de IVA (12% para Ecuador)
    subtotal_neto = total
    iva = subtotal_neto * 0.12
    total_con_iva = subtotal_neto + iva
    
    print(f"SUBTOTAL: ${subtotal_neto:<20.2f}")
    print(f"IVA (12%): ${iva:<20.2f}")
    print("-" * 75)
    print(f"TOTAL A PAGAR: ${total_con_iva:<20.2f}")
    print("=" * 75)
    print("Gracias por su compra. Su factura ha sido registrada en el sistema.")
    print("")
    os.system("pause")
>>>>>>> 5a72e7ec9126216e70b7ab3b8a7123ad42060b0c
