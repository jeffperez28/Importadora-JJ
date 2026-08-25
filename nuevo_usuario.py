import os, validaciones, connector, hash
from datetime import datetime

def nuevo_usuario():
    while True:
        cedula = input("Ingrese su cédula (10 dígitos): ")
        if not validaciones.validar_cedula(cedula):
            print("Cédula inválida. Por favor, ingrese una cédula válida.")
            continue
        if connector.usuario_existe(cedula):
            print("Esta cédula ya se encuentra registrada en nuestro sistema.")
            continue
        print("Cédula válida.")
        break

    while True:
        nombre = input("Ingrese sus nombres: ")
        if validaciones.validar_nombre(nombre):
            print("Nombre válido.")
            break
        print("Nombre inválido. Por favor, ingrese un nombre válido.")

    while True:
        apellido = input("Ingrese sus apellidos: ")
        if validaciones.validar_nombre(apellido):
            print("Apellido válido.")
            break
        print("Apellido inválido. Por favor, ingrese un apellido válido.")

    while True:
        celular = input("Ingrese su numero de celular: ")
        if validaciones.validar_celular(celular):
            print("Celular Válido.")
            break
        print("Celular inválido. Por favor, ingrese un numero de celular válido")

    while True:
        email = input("Ingrese su correo electronico: ")
        if validaciones.validar_email(email):
            print("Correo electrónico válido")
            break
        print("Correo inválido. Porfavor, ingrese un correo válido")

    while True:
        direccion = input("Ingrese su direccion: ")
        break

    while True:
        contrasena = input("Ingrese su contraseña: ")
        if validaciones.validar_contrasena(contrasena):
            print("Contraseña valida")
            break
        print("Contraseña invalida. Porfavor, la contraseña debe tener al menos 8 caracteres entre ellos mayuscula y minuscula, carateres especiales como @, -, _ y tambien un numero")

    while True:
        fecha = input("Ingrese su fecha de nacimiento en formato (DIA-MES-AÑO): ")
        if validaciones.validar_fecha_nacimiento(fecha):
            print("Fecha de nacimiento valida")
            break
        print("Fecha de nacimiento invalida porfavor ingrese la fecha en formato (DIA-MES-AÑO)")

    # Todo usuario nuevo se registra como CLIENTE.
    # Solo el administrador puede luego cambiarle el rol a BODEGUERO, VENDEDOR o ADMIN.
    rol = "CLIENTE"

    hashPass = hash.hash_password(contrasena)

    # MySQL guarda las columnas DATE internamente en formato AAAA-MM-DD,
    # aunque al usuario se le pidió DIA-MES-AÑO.
    fecha_mysql = datetime.strptime(fecha, "%d-%m-%Y").strftime("%Y-%m-%d")

    connector.insertar_usuario(
        cedula, nombre, apellido, celular, email, direccion, fecha_mysql, cedula, hashPass, rol
    )
    os.system("pause")


