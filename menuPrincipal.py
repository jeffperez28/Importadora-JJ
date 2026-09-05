<<<<<<< HEAD
import os, connector, hash, validaciones, getpass, menuAdmin, menuBodeguero, menuVendedor


def menu_principal():
	while True:
		os.system("cls")
		os.system('color 07')
		print("█ █▀▄▀█ █▀█ █▀█ █▀█ ▀█▀ ▄▀█ █▀▄ █▀█ █▀█ ▄▀█   ░░█ ░░█")
		print("█ █░▀░█ █▀▀ █▄█ █▀▄ ░█░ █▀█ █▄▀ █▄█ █▀▄ █▀█   █▄█ █▄█")
		print("")
		print("╔══════════════════════════════╗")
		print("║ Bienvenido al menu principal ║")
		print("╠══════════════════════════════╣")
		print("║  Seleccione una opción:      ║")
		print("║   1. Inicio de sesion        ║")
		print("║   2. Salir                   ║")
		print("╚══════════════════════════════╝")
		try:
			opcion = int(input("Ingrese la opcion deseada: "))
			if opcion == 1:
				print("Has seleccionado 'Inicio de sesión'.")
				os.system("pause")
				inicio_sesion()
			elif opcion == 2:
				print("Has seleccionado 'Salir'.")
				os.system("pause")
				break
			else:
				print("Opcion no válida. Por favor, seleccione una opción válida.")
				os.system("pause")
		except ValueError:
			print("ERROR: Por favor ingrese un número válido.")
			os.system("pause")

def inicio_sesion():
	intentos_usuario = 3

	while intentos_usuario > 0:
		usuario_input = input("Ingrese su usuario (cédula): ").strip()

		if usuario_input == "":
			print("Por favor, ingrese un usuario válido.")
			os.system("pause")
			continue

		if usuario_input == "admin":
			intentos_password = 3
			while intentos_password > 0:
				password = getpass.getpass("Ingrese su contraseña: ")
				hashPass = hash.hash_password(password)

				rol = connector.inicioSesion(usuario_input, hashPass)

				if rol:
					print("Acceso concedido")
					os.system("pause")
					redirigir_menu(usuario_input, rol)
					return
				else:
					intentos_password -= 1
					if intentos_password > 0:
						print(f"Contraseña incorrecta. Quedan {intentos_password} intentos.")
						os.system("pause")
					else:
						print("Contraseña incorrecta. Revise su usuario o contraseña.")
						os.system("pause")
						break
			return

		else:
			validacion = validaciones.validar_cedula(usuario_input)
			if not validacion:
				intentos_usuario = intentos_usuario - 1
				if intentos_usuario > 0:
					print(f"Cédula inválida. Quedan {intentos_usuario} intentos.")
					os.system("pause")
				else:
					print("Ha excedido el número de intentos. Volviendo al menú principal.")
					os.system("pause")
				continue

			intentos_password = 3
			while intentos_password > 0:
				password = getpass.getpass("Ingrese su contraseña: ")
				hashPass = hash.hash_password(password)

				rol = connector.inicioSesion(usuario_input, hashPass)

				if rol:
					print("Acceso concedido")
					os.system("pause")
					redirigir_menu(usuario_input, rol)
					return
				else:
					intentos_password = intentos_password - 1
					if intentos_password > 0:
						print(f"Contraseña incorrecta. Quedan {intentos_password} intentos.")
						os.system("pause")
					else:
						print("Contraseña incorrecta. Revise su usuario o contraseña.")
						os.system("pause")
						break
			return

def redirigir_menu(usuario, rol):
	if rol == "ADMINISTRADOR":
		menuAdmin.menu_admin()
	elif rol == "BODEGUERO":
		menuBodeguero.menu_bodeguero()
	elif rol == "VENDEDOR":
		menuVendedor.menu_vendedor(usuario)
	else:
		print(f"Su rol '{rol}' no tiene un menú asignado en el sistema.")
		os.system("pause")
=======
import os, connector, hash, validaciones, getpass, nuevo_usuario, menuAdmin, menuBodeguero, menuVendedor, menuCliente
# os biblioteca de operaciones del sistema operativo
# system("cls") limpia la pantalla en Windows, en Linux y MacOS se usa "clear"

os.system("color 07")
def menu_principal():
    while True:
        os.system("cls")  # limpia la pantalla
        os.system("color 07")

        print("█ █▀▄▀█ █▀█ █▀█ █▀█ ▀█▀ ▄▀█ █▀▄ █▀█ █▀█ ▄▀█   ░░█ ░░█")
        print("█ █░▀░█ █▀▀ █▄█ █▀▄ ░█░ █▀█ █▄▀ █▄█ █▀▄ █▀█   █▄█ █▄█")
        print("")
        print("╔══════════════════════════════╗")
        print("║ Bienvenido al menu principal ║")
        print("╠══════════════════════════════╣")
        print("║  Seleccione una opción:      ║")
        print("║   1. Inicio de sesion        ║")
        print("║   2. Registrarse             ║")
        print("║   3. Salir                   ║")
        print("╚══════════════════════════════╝")
        try:
            opcion = int(input("Ingrese la opcion deseada: "))
            if opcion == 1:
                print("Has seleccionado 'Inicio de sesión'.")
                os.system("pause")  # genera una pausa
                inicio_sesion()
            elif opcion == 2:
                print("Has seleccionado 'Registrarse'.")
                os.system("cls")
                nuevo_usuario.nuevo_usuario()
            elif opcion == 3:
                print("Has seleccionado 'Salir'.")
                os.system("pause")
                break
            else:
                print("Opcion no válida. Por favor, seleccione una opción válida.")
                os.system("pause")
        except ValueError:
            # esto es para que al usuario no le aparezca un error raro porque el no entiende de eso,
            # este se activa si el usuario ingresa una letra en la parte de input
            print("ERROR: Por favor ingrese un número válido.")
            os.system("pause")


def inicio_sesion():
    while True:
        name_user = input("Ingrese su usuario (cédula): ")
        validacion = validaciones.validar_cedula(name_user)
        if validacion or name_user == "admin":
            break
        else:
            print("Cédula inválida. Por favor, ingrese una cédula válida")

    password = getpass.getpass("Ingrese su contraseña: ")
    hashPass = hash.hash_password(password)
    resultado = connector.inicio_sesion(name_user, hashPass)

    if resultado:
        print("Acceso concedido")
        os.system("pause")
        rol = connector.obtener_rol(name_user)
        if rol == "ADMIN":
            menuAdmin.menu_admin()
        elif rol == "BODEGUERO":
            menuBodeguero.menu_bodeguero()
        elif rol == "VENDEDOR":
            menuVendedor.menu_vendedor()
        elif rol == "CLIENTE":
            menuCliente.menu_cliente(name_user)
        else:
            print(f"Su rol '{rol}' no tiene un menú asignado en el sistema.")
            os.system("pause")
    else:
        print("Usuario o contraseña incorrectos")
        os.system("pause")



>>>>>>> 5a72e7ec9126216e70b7ab3b8a7123ad42060b0c
