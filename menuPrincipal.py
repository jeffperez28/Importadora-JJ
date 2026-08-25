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



