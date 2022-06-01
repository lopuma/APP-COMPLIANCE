from cgitb import text
import re
def cadena_valida(cadena):
    patron = "^\/*.*?\*/$"
    return bool(re.search(patron, cadena))

text = "/* Hola mundo */"

print(cadena_valida(text))
