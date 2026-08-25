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