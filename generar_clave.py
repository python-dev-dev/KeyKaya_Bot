# PERMITE GENERAR LA CLAVE ALEATORIA SEGURA
from secrets import token_urlsafe
from random import randint
from SoporteTexto import msn_ayuda

# dalta arreglar

def generate_key():
    rango = int(randint(8,17))
    generate = str(token_urlsafe(rango))
    return generate

def ayuda_key():
    rangex = randint(0,4)
    return msn_ayuda[rangex]

