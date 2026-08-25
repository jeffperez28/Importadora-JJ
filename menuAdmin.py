import os, hash, connector, nuevo_usuario


def menu_admin():
    while True:
        os.system("cls")
        os.system("color 09")
        print("█▀▄▀█ █▀▀ █▄░█ █░█   █▀█ █▀▄ █▀▄▀█ █ █▄░█ █ █▀ ▀█▀ █▀█ ▄▀█ █▀▄ █▀█ █▀█")
        print("█░▀░█ ██▄ █░▀█ █▄█   █▀█ █▄▀ █░▀░█ █ █░▀█ █ ▄█ ░█░ █▀▄ █▀█ █▄▀ █▄█ █▀▄")
        print("")
        print("1. Gestión de usuarios")
        print("2. Cerrar sesión")
        try:
            opcion = int(input("Ingrese el número de la opción deseada: "))
            if opcion == 1:
                gestion_usuarios()
            elif opcion == 2:
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
        print("4. Eliminar usuario")
        print("5. Cambiar rol de un usuario")
        print("6. Volver")
        try:
            opcion = int(input("Ingrese el número de la opción deseada: "))
            if opcion == 1:
                os.system("cls")
                connector.ver_usuarios()
                os.system("pause")
            elif opcion == 2:
                os.system("cls")
                nuevo_usuario.nuevo_usuario()
            elif opcion == 3:
                os.system("cls")
                print("=== USUARIOS REGISTRADOS ===")
                connector.ver_usuarios()
                print("")
                name_user = input("Ingrese el name_user (cédula) del usuario a actualizar: ")
                print("Campos disponibles: NOMBRES, APELLIDOS, CELULAR, EMAIL, DIRECCION, PASSWORD")
                campo = input("Ingrese el campo a actualizar: ").upper()
                if campo == "ROL":
                    print("Para cambiar el rol use la opción 5 del menú.")
                    os.system("pause")
                    continue
                valor = input("Ingrese el nuevo valor: ")
                if campo == "PASSWORD":
                    valor = hash.hash_password(valor)
                connector.actualizar_usuario(name_user, campo, valor)
                os.system("pause")
            elif opcion == 4:
                os.system("cls")
                print("=== USUARIOS REGISTRADOS ===")
                connector.ver_usuarios()
                print("")
                name_user = input("Ingrese el name_user (cédula) del usuario a eliminar: ")
                connector.eliminar_usuario(name_user)
                os.system("pause")
            elif opcion == 5:
                cambiar_rol()
            elif opcion == 6:
                break
            else:
                print("Opción no válida.")
                os.system("pause")
        except ValueError:
            print("!/ERROR: Por favor, ingrese un número válido.")
            os.system("pause")


def cambiar_rol():
    os.system("cls")
    print("=== CAMBIAR ROL DE USUARIO ===")
    print("=== USUARIOS REGISTRADOS ===")
    connector.ver_usuarios()
    print("")
    name_user = input("Ingrese el name_user (cédula) del usuario: ")
    print("Roles disponibles:")
    print("1. ADMIN")
    print("2. BODEGUERO")
    print("3. VENDEDOR")
    print("4. CLIENTE")
    try:
        opcion_rol = int(input("Seleccione el nuevo rol: "))
        roles = {1: "ADMIN", 2: "BODEGUERO", 3: "VENDEDOR", 4: "CLIENTE"}
        if opcion_rol in roles:
            connector.actualizar_usuario(name_user, "ROL", roles[opcion_rol])
        else:
            print("Opción no válida.")
    except ValueError:
        print("!/ERROR: Por favor, ingrese un número válido.")
    os.system("pause")

