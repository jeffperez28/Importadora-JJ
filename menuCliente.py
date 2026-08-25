import os, connector


def menu_cliente(name_user):
    while True:
        os.system("cls")
        os.system("color 0B")
        print("█▀▄▀█ █▀▀ █▄░█ █░█   █▀▀ █░░ █ █▀▀ █▄░█ ▀█▀ █▀▀")
        print("█░▀░█ ██▄ █░▀█ █▄█   █▄▄ █▄▄ █ ██▄ █░▀█ ░█░ ██▄")
        print("")
        print("1. Ver mis datos")
        print("2. Ver productos disponibles")
        print("3. Ver mis facturas")
        print("4. Cerrar sesión")
        try:
            opcion = int(input("Ingrese el número de la opción deseada: "))
            if opcion == 1:
                os.system("cls")
                ver_mis_datos(name_user)
                os.system("pause")
            elif opcion == 2:
                os.system("cls")
                connector.ver_productos()
                os.system("pause")
            elif opcion == 3:
                os.system("cls")
                ver_mis_facturas(name_user)
                os.system("pause")
            elif opcion == 4:
                break
            else:
                print("Opción no válida.")
                os.system("pause")
        except ValueError:
            print("!/ERROR: Por favor, ingrese un número válido.")
            os.system("pause")


def ver_mis_datos(name_user):
    print("=== MIS DATOS ===")
    connector.select(
        "SELECT CI_USER, NOMBRES, APELLIDOS, CELULAR, EMAIL, DIRECCION, NAME_USER, ROL "
        "FROM users WHERE NAME_USER = %s;",
        (name_user.strip(),)
    )


def ver_mis_facturas(name_user):
    print("=== MIS FACTURAS ===")
    connector.ver_facturas_cliente(name_user)
    print("")
    respuesta = input("¿Desea ver el detalle de alguna factura? (s/n): ").strip().lower()
    if respuesta == "s":
        try:
            id_factura = int(input("Ingrese el número de factura: "))
        except ValueError:
            print("Número de factura inválido.")
            return
        
        # Validar que la factura existe y pertenece al cliente
        if not connector.validar_factura_cliente(id_factura, name_user):
            print(f"La factura N° {id_factura} no existe en el sistema o no pertenece a su cuenta.")
            return
        
        print("")
        print(f"=== DETALLE DE LA FACTURA N° {id_factura} ===")
        connector.ver_detalle_factura(id_factura)