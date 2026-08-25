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