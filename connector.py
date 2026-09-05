<<<<<<< HEAD
import bdd
import os
from tabulate import tabulate


# USUARIOS (tabla: usuario)


def usuario_existe(cedula_usuario):
	query = f"SELECT * FROM usuario WHERE cedula_usuario = '{cedula_usuario}';"
	resultado = bdd.consulta(query)
	if resultado:
		return True
	else:
		return False

def obtener_rol(cedula_usuario):
	query = f"SELECT rol FROM usuario WHERE cedula_usuario = '{cedula_usuario}';"
	resultado = bdd.consulta(query)
	if resultado:
		return resultado[0][0]
	else:
		return None

def inicioSesion(cedula_usuario, password):
	query = f"SELECT rol FROM usuario WHERE cedula_usuario = '{cedula_usuario}' AND contrasena = '{password}';"
	resultado = bdd.consulta(query)
	if resultado:
		return resultado[0][0]
	else:
		return None

def obtener_usuario_datos(cedula_usuario):
	query = f"SELECT nombres, apellidos FROM usuario WHERE cedula_usuario = '{cedula_usuario}';"
	resultado = bdd.consulta(query)
	if resultado:
		return resultado[0]
	else:
		return None


# CLIENTES (tabla: cliente)


def cliente_existe(cedula_cliente):
	query = f"SELECT * FROM cliente WHERE cedula_cliente = '{cedula_cliente}';"
	resultado = bdd.consulta(query)
	if resultado:
		return True
	else:
		return False

def obtener_cliente(cedula_cliente):
	query = f"SELECT nombres, apellidos FROM cliente WHERE cedula_cliente = '{cedula_cliente}';"
	resultado = bdd.consulta(query)
	if resultado:
		return resultado[0]
	else:
		return None

def obtener_cliente_completo(cedula_cliente):
	query = f"SELECT cedula_cliente, nombres, apellidos, telefono, correo_electronico, direccion, fecha_nacimiento FROM cliente WHERE cedula_cliente = '{cedula_cliente}';"
	resultado = bdd.consulta(query)
	if resultado:
		return resultado[0]
	else:
		return None

def insertar_cliente(cedula, nombres, apellidos, telefono, correo, direccion, fecha_nacimiento, cedula_vendedor=None):
	if cedula_vendedor:
		query = f"INSERT INTO cliente (cedula_cliente, nombres, apellidos, telefono, correo_electronico, direccion, fecha_nacimiento, fk_cedula_vendedor) VALUES ('{cedula}', '{nombres}', '{apellidos}', '{telefono}', '{correo}', '{direccion}', '{fecha_nacimiento}', '{cedula_vendedor}');"
	else:
		query = f"INSERT INTO cliente (cedula_cliente, nombres, apellidos, telefono, correo_electronico, direccion, fecha_nacimiento) VALUES ('{cedula}', '{nombres}', '{apellidos}', '{telefono}', '{correo}', '{direccion}', '{fecha_nacimiento}');"
	bdd.executar(query, mostrar_mensaje=False)

def ver_clientes():
	query = "SELECT c.cedula_cliente, c.nombres, c.apellidos, c.telefono, c.correo_electronico, c.direccion, c.fecha_nacimiento, TIMESTAMPDIFF(YEAR, c.fecha_nacimiento, CURDATE()) AS edad, c.estado, u.nombres AS vendedor FROM cliente c LEFT JOIN usuario u ON c.fk_cedula_vendedor = u.cedula_usuario;"
	bdd.select(query)


# PRODUCTOS (tabla: producto)


def producto_existe(codigo_producto):
	query = f"SELECT * FROM producto WHERE codigo_producto = '{codigo_producto}';"
	resultado = bdd.consulta(query)
	if resultado:
		return True
	else:
		return False

def obtener_producto(codigo_producto):
	query = f"SELECT codigo_producto, nombre_producto, cantidad, costo FROM producto WHERE codigo_producto = '{codigo_producto}';"
	resultado = bdd.consulta(query)
	if resultado:
		return resultado[0]
	else:
		return None

def descontar_stock(codigo_producto, cantidad):
	query = f"UPDATE producto SET cantidad = cantidad - {cantidad} WHERE codigo_producto = '{codigo_producto}';"
	bdd.executar(query, mostrar_mensaje=False)

def ver_productos():
	query = "SELECT codigo_producto, nombre_producto, cantidad, costo, estado FROM producto WHERE estado = 'activo';"
	bdd.select(query)

def ver_muestra_productos(limite=5):
	query = f"SELECT codigo_producto, nombre_producto, cantidad, costo, estado FROM producto WHERE estado = 'activo' LIMIT {int(limite)};"
	bdd.select(query)

def ver_productos_inactivos():
	query = "SELECT codigo_producto, nombre_producto, cantidad, costo, estado FROM producto WHERE estado = 'inactivo';"
	bdd.select(query)

def desactivar_producto(codigo_producto):
	query = f"UPDATE producto SET estado = 'inactivo' WHERE codigo_producto = '{codigo_producto}';"
	bdd.executar(query)

def activar_producto(codigo_producto):
	query = f"UPDATE producto SET estado = 'activo' WHERE codigo_producto = '{codigo_producto}';"
	bdd.executar(query)

def insertar_producto(codigo, nombre, cantidad, descripcion, costo):
	query = f"INSERT INTO producto (codigo_producto, nombre_producto, cantidad, descripcion, costo) VALUES ('{codigo}', '{nombre}', {cantidad}, '{descripcion}', {costo});"
	bdd.executar(query)

def actualizar_producto(codigo, campo, valor):
	campos_validos = ("nombre_producto", "cantidad", "descripcion", "costo")
	if campo not in campos_validos:
		print("Campo no válido.")
		os.system("pause")
		return
	query = f"UPDATE producto SET {campo} = '{valor}' WHERE codigo_producto = '{codigo}';"
	bdd.executar(query)


# FACTURAS (tabla: factura, detalle)


def crear_factura(cedula_cliente, cedula_usuario, total):
	query = f"INSERT INTO factura (fk_cedula_cliente, fk_cedula_usuario, total) VALUES ('{cedula_cliente}', '{cedula_usuario}', {total});"
	bdd.executar(query, mostrar_mensaje=False)

	query_id = "SELECT MAX(id_factura) FROM factura;"
	resultado = bdd.consulta(query_id)
	if resultado and resultado[0][0]:
		return resultado[0][0]
	return None

def insertar_detalle_factura(id_factura, codigo_producto, cantidad, valor_unitario, subtotal, descuento=0):
	query = f"INSERT INTO detalle (fk_id_factura, fk_codigo_producto, cantidad, valor_unitario, subtotal, descuento) VALUES ({id_factura}, '{codigo_producto}', {cantidad}, {valor_unitario}, {subtotal}, {descuento});"
	bdd.executar(query, mostrar_mensaje=False)

def ver_facturas_cliente(cedula_cliente):
	query = f"SELECT id_factura, fecha_elaboracion, total FROM factura WHERE fk_cedula_cliente = '{cedula_cliente}' ORDER BY fecha_elaboracion DESC;"
	bdd.select(query)

def ver_detalle_factura(id_factura):
	query = f"SELECT d.fk_codigo_producto, p.nombre_producto, d.cantidad, d.valor_unitario, d.subtotal, d.descuento FROM detalle d JOIN producto p ON p.codigo_producto = d.fk_codigo_producto WHERE d.fk_id_factura = {id_factura};"
	bdd.select(query)

def validar_factura_cliente(id_factura, cedula_cliente):
	query = f"SELECT id_factura FROM factura WHERE id_factura = {id_factura} AND fk_cedula_cliente = '{cedula_cliente}';"
	resultado = bdd.consulta(query)
	if resultado:
		return True
	else:
		return False

def obtener_factura_info(id_factura):
	query = f"SELECT id_factura, fk_cedula_cliente, fk_cedula_usuario, fecha_elaboracion, total FROM factura WHERE id_factura = {id_factura};"
	resultado = bdd.consulta(query)
	if resultado:
		return resultado[0]
	else:
		return None

def obtener_detalle_factura_lista(id_factura):
	query = f"SELECT p.nombre_producto, d.cantidad, d.valor_unitario, d.subtotal, d.descuento FROM detalle d JOIN producto p ON p.codigo_producto = d.fk_codigo_producto WHERE d.fk_id_factura = {id_factura};"
	resultado = bdd.consulta(query)
	return resultado if resultado else []

def mostrar_nota_venta(id_factura):
	info = obtener_factura_info(id_factura)
	if info is None:
		print("No existe una nota de venta con ese número.")
		return False

	_, cedula_cliente, cedula_usuario, fecha, total = info
	cliente = obtener_cliente_completo(cedula_cliente)
	vendedor = obtener_usuario_datos(cedula_usuario)
	detalles = obtener_detalle_factura_lista(id_factura)

	nombres_cliente, apellidos_cliente = cliente[1], cliente[2]
	telefono_cliente, correo_cliente, direccion_cliente = cliente[3], cliente[4], cliente[5]
	nombres_vendedor, apellidos_vendedor = vendedor if vendedor else ("Desconocido", "")

	fecha_str = fecha.strftime('%d/%m/%Y %H:%M') if hasattr(fecha, 'strftime') else str(fecha)

	subtotal = float(total)
	descuento_total = sum(float(d[4]) for d in detalles)
	iva = subtotal * 0.12
	total_pagar = subtotal + iva

	print("=" * 78)
	print("NOTA DE VENTA".center(78))
	print("=" * 78)
	print(f"IMPORTADORA JJ{'N°: ' + str(id_factura):>64}")
	print(f"{'Fecha: ' + fecha_str:>78}")
	print("-" * 78)
	print(f"Cliente:   {nombres_cliente} {apellidos_cliente}")
	print(f"Cédula:    {cedula_cliente}")
	print(f"Teléfono:  {telefono_cliente}")
	print(f"Correo:    {correo_cliente}")
	print(f"Dirección: {direccion_cliente}")
	print(f"Vendedor:  {nombres_vendedor} {apellidos_vendedor}")
	print("-" * 78)

	tabla = [[d[1], d[0], f"${float(d[2]):.2f}", f"${float(d[3]):.2f}"] for d in detalles]
	headers = ["Cant.", "Descripción", "Vr. Unitario", "Importe"]
	print(tabulate(tabla, headers=headers, tablefmt='grid'))

	print()
	print(f"{'SUBTOTAL:':>65} ${subtotal:.2f}")
	if descuento_total > 0:
		print(f"{'DESCUENTO:':>65} ${descuento_total:.2f}")
	print(f"{'IVA (12%):':>65} ${iva:.2f}")
	print(f"{'TOTAL:':>65} ${total_pagar:.2f}")
	print("=" * 78)
	return True


# USUARIOS - VER LISTA


def ver_usuarios():
	query = "SELECT cedula_usuario, nombres, apellidos, telefono, correo_electronico, rol, estado FROM usuario WHERE estado = 'activo';"
	bdd.select(query)

def ver_vendedores():
	query = "SELECT cedula_usuario, nombres, apellidos, telefono FROM usuario WHERE rol = 'VENDEDOR' AND estado = 'activo';"
	bdd.select(query)

def ver_usuarios_inactivos():
	query = "SELECT cedula_usuario, nombres, apellidos, telefono, correo_electronico, rol, estado FROM usuario WHERE estado = 'inactivo';"
	bdd.select(query)

def desactivar_usuario(cedula_usuario):
	query = f"UPDATE usuario SET estado = 'inactivo' WHERE cedula_usuario = '{cedula_usuario}';"
	bdd.executar(query)

def activar_usuario(cedula_usuario):
	query = f"UPDATE usuario SET estado = 'activo' WHERE cedula_usuario = '{cedula_usuario}';"
	bdd.executar(query)


# CARTERA VENDEDOR-CLIENTE

def ver_clientes_vendedor(cedula_vendedor):
	query = f"SELECT cedula_cliente, nombres, apellidos, telefono, correo_electronico, direccion, estado FROM cliente WHERE fk_cedula_vendedor = '{cedula_vendedor}' AND estado = 'activo';"
	bdd.select(query)

def ver_todos_clientes_activos():
	query = "SELECT c.cedula_cliente, c.nombres, c.apellidos, c.telefono, c.direccion, u.nombres AS vendedor FROM cliente c LEFT JOIN usuario u ON c.fk_cedula_vendedor = u.cedula_usuario WHERE c.estado = 'activo';"
	bdd.select(query)

def cliente_asignado_vendedor(cedula_vendedor, cedula_cliente):
	query = f"SELECT fk_cedula_vendedor FROM cliente WHERE cedula_cliente = '{cedula_cliente}' AND fk_cedula_vendedor = '{cedula_vendedor}';"
	resultado = bdd.consulta(query)
	if resultado:
		return True
	else:
		return False

def asignar_cliente_vendedor(cedula_vendedor, cedula_cliente):
	if cliente_asignado_vendedor(cedula_vendedor, cedula_cliente):
		print("Este cliente ya está en su cartera.")
		return False
	query = f"UPDATE cliente SET fk_cedula_vendedor = '{cedula_vendedor}' WHERE cedula_cliente = '{cedula_cliente}';"
	bdd.executar(query, mostrar_mensaje=False)
	return True

def desasignar_cliente_vendedor(cedula_cliente):
	query = f"UPDATE cliente SET fk_cedula_vendedor = NULL WHERE cedula_cliente = '{cedula_cliente}';"
	bdd.executar(query)

def ver_clientes_sin_asignar():
	query = "SELECT cedula_cliente, nombres, apellidos, telefono, correo_electronico, direccion, estado FROM cliente WHERE fk_cedula_vendedor IS NULL AND estado = 'activo';"
	bdd.select(query)

def obtener_vendedor_cliente(cedula_cliente):
	query = f"SELECT fk_cedula_vendedor FROM cliente WHERE cedula_cliente = '{cedula_cliente}';"
	resultado = bdd.consulta(query)
	if resultado and resultado[0][0]:
		return resultado[0][0]
	else:
		return None

def ver_clientes_vendedor_inactivos(cedula_vendedor):
	query = f"SELECT cedula_cliente, nombres, apellidos, telefono, correo_electronico, direccion, estado FROM cliente WHERE fk_cedula_vendedor = '{cedula_vendedor}' AND estado = 'inactivo';"
	bdd.select(query)

def actualizar_cliente_vendedor(cedula_vendedor, cedula_cliente, campo, valor):
	if not cliente_asignado_vendedor(cedula_vendedor, cedula_cliente):
		print("Este cliente no pertenece a su cartera.")
		return False
	campos_validos = ("nombres", "apellidos", "telefono", "correo_electronico", "direccion", "fecha_nacimiento")
	if campo not in campos_validos:
		print("Campo no válido.")
		return False
	query = f"UPDATE cliente SET {campo} = '{valor}' WHERE cedula_cliente = '{cedula_cliente}';"
	bdd.executar(query)
	return True

def desactivar_cliente_vendedor(cedula_vendedor, cedula_cliente):
	if not cliente_asignado_vendedor(cedula_vendedor, cedula_cliente):
		print("Este cliente no pertenece a su cartera.")
		return False
	query = f"UPDATE cliente SET estado = 'inactivo' WHERE cedula_cliente = '{cedula_cliente}';"
	bdd.executar(query)
	return True

def activar_cliente_vendedor(cedula_vendedor, cedula_cliente):
	if not cliente_asignado_vendedor(cedula_vendedor, cedula_cliente):
		print("Este cliente no pertenece a su cartera.")
		return False
	query = f"UPDATE cliente SET estado = 'activo' WHERE cedula_cliente = '{cedula_cliente}';"
	bdd.executar(query)
	return True


# ALERTAS DE STOCK

def obtener_productos_alerta():
	query = "SELECT codigo_producto, nombre_producto, cantidad, costo FROM producto WHERE estado = 'activo' ORDER BY cantidad ASC;"
	resultado = bdd.consulta(query)
	return resultado if resultado else []

def mostrar_alertas_stock():
	productos = obtener_productos_alerta()
	if not productos:
		return

	alertas_criticas = [p for p in productos if p[2] < 15]
	alertas_bajas = [p for p in productos if 15 <= p[2] < 35]

	if alertas_criticas or alertas_bajas:
		print("⚠️  BANDEJA DE ENTRADA - ALERTAS DE STOCK")

		if alertas_criticas:
			print("🔴 STOCK CRÍTICO (< 15 unidades):\n")
			headers = ["Código", "Nombre", "Cantidad", "Costo"]
			print(tabulate(alertas_criticas, headers=headers, tablefmt='grid'))

		if alertas_bajas:
			print("\n🟠 STOCK BAJO (< 35 unidades):\n")
			headers = ["Código", "Nombre", "Cantidad", "Costo"]
			print(tabulate(alertas_bajas, headers=headers, tablefmt='grid'))

		print()

def ver_facturas_vendedor(cedula_vendedor):
	query = f"SELECT id_factura AS 'N°', fk_cedula_cliente AS 'Cédula Cliente', fecha_elaboracion AS 'Fecha', total AS 'Total' FROM factura WHERE fk_cedula_usuario = '{cedula_vendedor}' ORDER BY fecha_elaboracion DESC;"
	bdd.select(query)

def ver_todas_facturas():
	query = "SELECT id_factura AS 'N°', fk_cedula_cliente AS 'Cédula Cliente', fk_cedula_usuario AS 'Cédula Vendedor', fecha_elaboracion AS 'Fecha', total AS 'Total' FROM factura ORDER BY fecha_elaboracion DESC;"
	bdd.select(query)
=======
import mysql.connector
from tabulate import tabulate

def conectar():
	return mysql.connector.connect(
		host="localhost",
		user="root",
		password="root",
		database="importadorajj",
		auth_plugin='mysql_native_password'
	)

def prueba_conexion():
    try:
        conexion = conectar()
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos.")
            conexion.close()
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")

def ejecutar(query, valores=None):
	try:
		conexion = conectar()
		cursor = conexion.cursor()
		if valores:
			cursor.execute(query, valores)
		else:
			cursor.execute(query)
		conexion.commit()
		return cursor.rowcount
	except Exception as e:
		print(f"Error al ejecutar la operación: {e}")
		return -1
	finally:
		if conexion.is_connected():
			cursor.close()
			conexion.close()

def select(query, valores=None):
	try:
		conexion = conectar()
		cursor = conexion.cursor()
		if valores:
			cursor.execute(query, valores)
		else:
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

def consulta(query, valores=None):
	try:
		conexion = conectar()
		cursor = conexion.cursor()
		if valores:
			cursor.execute(query, valores)
		else:
			cursor.execute(query)
		resultados = cursor.fetchall()
		return resultados
	except Exception as e:
		print(f"Error al consultar datos: {e}")
	finally:
		if conexion.is_connected():
			cursor.close()
			conexion.close()


# ==========================================================
# USUARIOS (tabla: users)
# ==========================================================

def inicio_sesion(name_user, password):
	resultado = consulta(
		"SELECT * FROM users WHERE NAME_USER = %s AND PASSWORD = %s",
		(name_user, password)
	)
	return bool(resultado)

def obtener_rol(name_user):
	resultado = consulta("SELECT ROL FROM users WHERE NAME_USER = %s", (name_user,))
	if resultado:
		return resultado[0][0]
	return None

def usuario_existe(name_user):
	resultado = consulta("SELECT 1 FROM users WHERE NAME_USER = %s", (name_user,))
	return bool(resultado)

def obtener_cliente(name_user):
	resultado = consulta(
		"SELECT NOMBRES, APELLIDOS FROM users WHERE NAME_USER = %s",
		(name_user,)
	)
	if resultado:
		return resultado[0]
	return None

def insertar_usuario(ci, nombres, apellidos, celular, email, direccion, fecha_nacimiento, name_user, password, rol):
	query = """INSERT INTO users
			   (CI_USER, NOMBRES, APELLIDOS, CELULAR, EMAIL, DIRECCION, FECHA_NACIMIENTO, NAME_USER, PASSWORD, ROL)
			   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
	valores = (ci, nombres, apellidos, celular, email, direccion, fecha_nacimiento, name_user, password, rol)
	if ejecutar(query, valores) > 0:
		print("Usuario insertado con éxito.")
	else:
		print("No se pudo insertar el usuario.")

def ver_usuarios():
	select("SELECT CI_USER, NOMBRES, APELLIDOS, CELULAR, EMAIL, NAME_USER, ROL FROM users;")

def actualizar_usuario(name_user, campo, valor):
	campos_validos = ("NOMBRES", "APELLIDOS", "CELULAR", "EMAIL", "DIRECCION", "PASSWORD", "ROL")
	if campo not in campos_validos:
		print("Campo no válido.")
		return
	query = f"UPDATE users SET {campo} = %s WHERE NAME_USER = %s"
	filas = ejecutar(query, (valor, name_user.strip()))
	if filas > 0:
		print("Usuario actualizado con éxito.")
	elif filas == 0:
		print(f"No se encontró ningún usuario con NAME_USER = '{name_user}'. No se actualizó nada.")
	else:
		print("No se pudo actualizar el usuario.")

def eliminar_usuario(name_user):
	filas = ejecutar("DELETE FROM users WHERE NAME_USER = %s", (name_user.strip(),))
	if filas > 0:
		print("Usuario eliminado con éxito.")
	elif filas == 0:
		print(f"No se encontró ningún usuario con NAME_USER = '{name_user}'. No se eliminó nada.")
	else:
		print("No se pudo eliminar el usuario.")


# ==========================================================
# PRODUCTOS (tabla: productos)
# ==========================================================

def producto_existe(codigo):
	resultado = consulta("SELECT 1 FROM productos WHERE CODIGO_PRODUCTO = %s", (codigo.strip().upper(),))
	return bool(resultado)

def insertar_producto(codigo, nombre, unidad, costo, descuento, stock):
	query = """INSERT INTO productos
			   (CODIGO_PRODUCTO, NOMBRE_PRODUCTO, UNIDAD_PRODUCTO, COSTO, DESCUENTO, STOCK)
			   VALUES (%s, %s, %s, %s, %s, %s)"""
	if ejecutar(query, (codigo, nombre, unidad, costo, descuento, stock)) > 0:
		print("Producto insertado con éxito.")
	else:
		print("No se pudo insertar el producto.")

def obtener_producto(codigo):
	resultado = consulta(
		"SELECT CODIGO_PRODUCTO, NOMBRE_PRODUCTO, UNIDAD_PRODUCTO, COSTO, DESCUENTO, STOCK FROM productos WHERE CODIGO_PRODUCTO = %s",
		(codigo,)
	)
	if resultado:
		return resultado[0]
	return None

def descontar_stock(codigo, cantidad):
	query = "UPDATE productos SET STOCK = STOCK - %s WHERE CODIGO_PRODUCTO = %s"
	return ejecutar(query, (cantidad, codigo))

def ver_productos():
	select("SELECT * FROM productos;")

def ver_muestra_productos(limite=5):
	select(f"SELECT * FROM productos LIMIT {int(limite)};")

def actualizar_producto(codigo, campo, valor):
	campos_validos = ("NOMBRE_PRODUCTO", "UNIDAD_PRODUCTO", "COSTO", "DESCUENTO", "STOCK")
	if campo not in campos_validos:
		print("Campo no válido.")
		return
	query = f"UPDATE productos SET {campo} = %s WHERE CODIGO_PRODUCTO = %s"
	filas = ejecutar(query, (valor, codigo.strip()))
	if filas > 0:
		print("Producto actualizado con éxito.")
	elif filas == 0:
		print(f"No se encontró ningún producto con CODIGO_PRODUCTO = '{codigo}'. No se actualizó nada.")
	else:
		print("No se pudo actualizar el producto.")

def eliminar_producto(codigo):
	filas = ejecutar("DELETE FROM productos WHERE CODIGO_PRODUCTO = %s", (codigo.strip(),))
	if filas > 0:
		print("Producto eliminado con éxito.")
	elif filas == 0:
		print(f"No se encontró ningún producto con CODIGO_PRODUCTO = '{codigo}'. No se eliminó nada.")
	else:
		print("No se pudo eliminar el producto.")


# ==========================================================
# FACTURAS (tablas: facturas, detalle_factura)
# ==========================================================

def crear_factura(ci_cliente, total):
	"""Inserta la cabecera de la factura y devuelve el ID_FACTURA generado, o None si falló."""
	try:
		conexion = conectar()
		cursor = conexion.cursor()
		cursor.execute(
			"INSERT INTO facturas (CI_CLIENTE, TOTAL) VALUES (%s, %s)",
			(ci_cliente, total)
		)
		conexion.commit()
		id_factura = cursor.lastrowid
		return id_factura
	except Exception as e:
		print(f"Error al registrar la factura: {e}")
		return None
	finally:
		if conexion.is_connected():
			cursor.close()
			conexion.close()

def insertar_detalle_factura(id_factura, codigo_producto, cantidad, precio_unitario, subtotal):
	query = """INSERT INTO detalle_factura
			   (ID_FACTURA, CODIGO_PRODUCTO, CANTIDAD, PRECIO_UNITARIO, SUBTOTAL)
			   VALUES (%s, %s, %s, %s, %s)"""
	return ejecutar(query, (id_factura, codigo_producto, cantidad, precio_unitario, subtotal))

def ver_facturas_cliente(ci_cliente):
	select(
		"SELECT ID_FACTURA, FECHA_FACTURA, TOTAL FROM facturas WHERE CI_CLIENTE = %s ORDER BY FECHA_FACTURA DESC;",
		(ci_cliente.strip(),)
	)

def ver_detalle_factura(id_factura):
	select(
		"""SELECT d.CODIGO_PRODUCTO, p.NOMBRE_PRODUCTO, d.CANTIDAD, d.PRECIO_UNITARIO, d.SUBTOTAL
		   FROM detalle_factura d
		   JOIN productos p ON p.CODIGO_PRODUCTO = d.CODIGO_PRODUCTO
		   WHERE d.ID_FACTURA = %s;""",
		(id_factura,)
	)

def validar_factura_cliente(id_factura, ci_cliente):
	"""Valida que una factura existe y pertenece al cliente especificado.
	   Retorna True si existe, False si no existe."""
	try:
		conexion = conectar()
		cursor = conexion.cursor()
		cursor.execute(
			"SELECT id_factura FROM facturas WHERE id_factura = %s AND ci_cliente = %s;",
			(id_factura, ci_cliente)
		)
		resultado = cursor.fetchone()
		cursor.close()
		conexion.close()
		return resultado is not None
	except Exception as e:
		print(f"Error al validar la factura: {e}")
		return False
>>>>>>> 5a72e7ec9126216e70b7ab3b8a7123ad42060b0c
