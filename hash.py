import hashlib

def hash_password(password):
    hashPass = hashlib.md5(password.encode('utf-8')).hexdigest()
    return hashPass

#Pruebas hasheando la contraseña del usuario
"""password = input ("Ingrese su contraseña: ")
resultadoHash = hash_password(password)
print(f"Tu clave hasheada es: {resultadoHash}")"""

