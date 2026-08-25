import os, connector

os.system("color 0E")
def menu_bodeguero():
    while True:
        os.system("cls")
        os.system("color 0E")
        
        print("█▀▄▀█ █▀▀ █▄░█ █░█   █▄▄ █▀█ █▀▄ █▀▀ █▀▀ █░█ █▀▀ █▀█ █▀█")
        print("█░▀░█ ██▄ █░▀█ █▄█   █▄█ █▄█ █▄▀ ██▄ █▄█ █▄█ ██▄ █▀▄ █▄█")
        print("")
        print("1. Control de stock")
        print("2. Cerrar sesión")
        try:
            opcion = int(input("Ingrese el número de la opción deseada: "))
            if opcion == 1:
                control_stock()
            elif opcion == 2:
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
        print("4. Eliminar producto")
        print("5. Volver")
        try:
            opcion = int(input("Ingrese el número de la opción deseada: "))
            if opcion == 1:
                os.system("cls")
                connector.ver_productos()
                os.system("pause")
            elif opcion == 2:
                os.system("cls")
                print("=== INSERTAR PRODUCTO ===")
                print("Ejemplo de productos ya registrados, como referencia:")
                connector.ver_muestra_productos(5)
                print("")
                codigo = input("Código de producto (6 caracteres, ej. P00007): ").strip().upper()

                # --- Validación temprana: se comprueba primero si el código ya existe ---
                # antes de pedir el resto de los datos del producto
                if connector.producto_existe(codigo):
                    print("Este producto ya existe en el sistema.")
                    os.system("pause")
                    continue

                nombre = input("Nombre del producto: ")
                unidad = input("Unidad (ej. Unidad, Kilogramo): ")
                costo = float(input("Costo: "))
                descuento = float(input("Descuento (%): "))
                stock = int(input("Stock inicial: "))
                connector.insertar_producto(codigo, nombre, unidad, costo, descuento, stock)
                os.system("pause")
            elif opcion == 3:
                os.system("cls")
                print("=== ACTUALIZAR PRODUCTO ===")
                connector.ver_productos()
                print("")
                codigo = input("Código del producto a actualizar: ")
                print("")
                print("Campos disponibles:")
                print("1) NOMBRE_PRODUCTO")
                print("2) UNIDAD_PRODUCTO")
                print("3) COSTO")
                print("4) DESCUENTO")
                print("5) STOCK")
                campos = {1: "NOMBRE_PRODUCTO", 2: "UNIDAD_PRODUCTO", 3: "COSTO", 4: "DESCUENTO", 5: "STOCK"}
                try:
                    opcion_campo = int(input("Seleccione el campo a actualizar: "))
                except ValueError:
                    print("!/ERROR: Por favor, ingrese un número válido.")
                    os.system("pause")
                    continue
                campo = campos.get(opcion_campo)
                if campo is None:
                    print("Opción no válida.")
                    os.system("pause")
                    continue
                valor = input("Ingrese el nuevo valor: ")
                connector.actualizar_producto(codigo, campo, valor)
                os.system("pause")
            elif opcion == 4:
                os.system("cls")
                print("=== ELIMINAR PRODUCTO ===")
                connector.ver_productos()
                print("")
                codigo = input("Ingrese el código de producto que desea eliminar: ")
                connector.eliminar_producto(codigo)
                os.system("pause")
            elif opcion == 5:
                break
            else:
                print("Opción no válida.")
                os.system("pause")
        except ValueError:
            print("!/ERROR: Por favor, ingrese un valor válido.")
            os.system("pause")

            