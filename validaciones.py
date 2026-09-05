import re
from datetime import datetime

def validar_cedula(cedula):
    """
    Valida si una cédula ecuatoriana es válida.
    """
    if len(cedula) != 10 or not cedula.isdigit():
        return False

    provincia = int(cedula[:2])
    if not (1 <= provincia <= 24 or provincia == 30):
        return False

    tercer_digito = int(cedula[2])
    if tercer_digito >= 6:
        return False

    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]

    suma = 0
    for i in range(9):
        valor = int(cedula[i]) * coeficientes[i]
        if valor >= 10:
            valor -= 9
        suma += valor

    digito_verificador = 10 - (suma % 10)
    if digito_verificador == 10:
        digito_verificador = 0

    return digito_verificador == int(cedula[9])


def validar_nombre(nombre: str) -> bool:
    """
    Valida si una cadena de texto es un nombre válido.
    Permite letras (incluyendo tildes y ñ) y espacios entre palabras.
    """
    if not isinstance(nombre, str):
        return False

    nombre_limpio = nombre.strip()

    if not nombre_limpio:
        return False

    patron = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+(?:\s+[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+)*$"

    return bool(re.match(patron, nombre_limpio))


def validar_celular(celular):
    inicio = celular[:2]
    if inicio != "09":
        return False
    elif celular.isdigit() and len(celular) == 10:
        return True


def validar_email(email: str) -> bool:
    """
    Valida la estructura de un correo electrónico.
    """
    if not isinstance(email, str) or not email.strip():
        return False

    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    return bool(re.match(patron, email.strip()))


def validar_contrasena(contrasena):
    # ^               : Inicio de la cadena
    # (?=.*[a-z])     : Al menos una letra minuscula
    # (?=.*[A-Z])     : Al menos una letra mayuscula
    # (?=.*\d)        : Al menos un numero
    # (?=.*[\W_])     : Al menos un caracter especial
    # .{8,}           : Al menos 8 caracteres de longitud
    patron = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$'

    return bool(re.match(patron, contrasena))


def calcular_edad(fecha_nac, hoy):
    """
    Calcula los anios cumplidos a la fecha indicada.
    """
    edad = hoy.year - fecha_nac.year
    if (hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day):
        edad -= 1
    return edad


def validar_fecha_nacimiento(fecha_str, formato="%d-%m-%Y", edad_minima=18):
    """
    Valida que la fecha exista, no sea futura y que la persona
    sea mayor de edad (18 anios por defecto).
    Formato por defecto: DD-MM-AAAA (ejemplo: '25-08-1995')
    """
    try:
        fecha_nac = datetime.strptime(fecha_str, formato).date()
        hoy = datetime.now().date()

        if fecha_nac > hoy:
            return False

        edad = calcular_edad(fecha_nac, hoy)

        if edad < edad_minima:
            return False

        if edad > 120:
            return False

        return True

    except ValueError:
        return False
        