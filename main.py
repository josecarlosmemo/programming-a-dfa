# Autor: José Carlos Martínez Núñez
# Matrícula: A01639664


# Instrucciones de uso:
# 1. Instalar deppendencias. Ingresar el  siguiente comando a Terminal/cmd
# pip3 install tabulate
# 2. Ejecutar el programa.
# 3. Ingresar el archivo a leer.
# 4. Ver los resultados.


import string
from tabulate import tabulate

# Lista de Tokens
tokens = []

# Mapa de Tokens y Tipos
symbolToToken = {'+': "Asignación", '*': "Multiplicación", '^': "Potencia", '=': "Asignción",
                 '(': "Paréntesis que abre",
                 ')': "Paréntesis que cierra", '/': "División", '-': "Resta"}

# Símbolos Directos
# Son los símbolos que representan un token con solo un caracter
# Se lleva de manera directa a un estado final
directSymbols = [4,5,6,7,8,9]

def nextState(char, currentState):
    # Estado Comentario
    if currentState == 1 and char == "/":
        return 2
    elif char == "/": # Estado /
        return 1

    if currentState == 2 and char != "\n":
        return 2

    # Estado Final Termina Linea
    if char == "\n":
        return 3

    # Estados de Símbolos Directos
    if char == ")":
        return 4
    if char == "+":
        return 5
    if char == "(":
        return 6
    if char == "=":
        return 7
    if char == "*":
        return 8
    if char == "^":
        return 9

    # Comienzan Númericos

    if currentState == 14 and char.isdigit():
        return 14
    if currentState == 14 and char in "eE":
        return 15
    if currentState == 16 and char.isdigit():
        return 17

    if currentState == 15 and (char.isdigit()):
        return 17

    if currentState == 15 and char == "-":
        return 16
    if currentState == 17 and char.isdigit():
        return 17

    if currentState == 11 and char.isdigit():
        return 12
    elif char == "-":
        return 11

    if currentState == 13 and char.isdigit():
        return 14
    elif currentState == 12 and char == ".":
        return 14

    if currentState == 12 and char.isdigit():
        return 12
    elif char.isdigit():
        return 12
    elif char == ".":
        return 13

    # Comienzan Variables
    if char.isalpha():
        return 10
    if currentState == 10 and (char.isalnum() or char == "_"):
        return 10

def addToList(readString, currentState, char):
    if readString:
        if currentState in [10] and nextState(char, currentState) in [1, 3, 11, None] + directSymbols:
            ## VARIABLES ##
            '''
            Una variable se considera completa una vez que pasamos del estado q10 (Estado Final de las Variables)
            a los siguientes estados:
            q1: Estado de "/"
            q3: Estado de "\n"
            [q4...q9]:  Estados de Símbolos Directos
            q11: Estado de "-"
            None: Estado de vacío
            '''
            try:
                tokens.append([readString, "Variable"])
            except:
                tokens.append([readString, "Error"])
            return ""
        elif currentState in directSymbols:
            ## SÍMBOLOS DIRECTOS  ##
            '''
            Estos son los símbolos que representan un token por sí solos, solo basta un caracter para llegar a sus
            respectivos finales:
            [q4...q9]: Estados de Símbolos Directos
            '''
            try:
                tokens.append([readString, symbolToToken[readString]])
            except:
                tokens.append([readString, "Error"])

            return ""
        elif currentState in [14, 17] and nextState(char, currentState) in [1,3,  10, 11, None] + directSymbols:
            ## NÚMEROS REALES ##
            '''
            Un número real se considera completo una vez que se pase de los estados [q14,q17] (Estados Finales de Números Reales)
            a los siguientes estados:
            q1: Estado de "/"
            q3: Estado de "\n"
            [q4...q9]:  Estados de Símbolos Directos
            q10: Estado de Variables
            q11: Estado de "-"
            None: Estado de vacío
            '''
            try:

                tokens.append([readString, "Real"])
            except:
                tokens.append([readString, "Error"])

            return ""

        elif currentState in [12] and nextState(char, currentState) not in [12, 14]:
            ## ENTEROS ##
            '''
            Un número entero se considera terminado cuando pasa de recibir números enteros (q12) o un punto decimal (q14)
            
            
            '''
            try:
                tokens.append([readString, "Entero"])
            except:
                tokens.append([readString, "Error"])

            return ""


        elif currentState in [11] and nextState(char, currentState) not in [12]:
            ## RESTAS ##
            '''
            Se considera una resta cuando pasamos del estado del símbolo "-" (q11) a cualquier cosa que no sea un número (q12). 
            '''

            try:
                tokens.append([readString, symbolToToken[readString]])
            except:
                tokens.append([readString, "Error"])

            return ""
        elif currentState in [1] and nextState(char, currentState) not in [2]:
            ## DIVISIÓN ##
            '''
            Se considera una división cuando pasamos del estado del símbolo "/" a cualquier estado que no sea el de comentario (q2).
            '''
            try:

                tokens.append([readString, symbolToToken[readString]])
            except:
                tokens.append([readString, "Error"])

            return ""
        elif currentState in [2] and char == "\n":
            ## COMENTARIOS ##
            '''
            Un comentario se considera terminado cuando nos encontramos en el estado de comentarios (q2) y recibimos una "\n".
            '''
            try:

                tokens.append([readString, "Comentario"])
            except:
                tokens.append([readString, "Error"])
            return ""

        elif readString.count(".") > 1 or (
                currentState in [10] and (readString[0].isdigit() or readString[0] == "_")):
            ## ERRORES ##
            tokens.append([readString, "Error"])
            return ""
        else:
            return readString

def lexerAritmetico(fileName):
    # Leemos el archivo
    file = open(fileName, 'r')

    for line in file:
        readString = ""
        currentState = 0

        for char in line + "\n":
            # Revisamos si el string leido es un token
            if readString:
                readString = addToList(readString, currentState, char)

            # Agregamos el caracter al string leido, ignoramos espacios solo sí no es un comentario
            if currentState != 2 and char not in string.whitespace:
                readString += char
            elif currentState == 2:
                readString += char
            # Actualizamos el estado
            currentState = nextState(char, currentState)

    # Imprimimos tabla de tokens
    print(tabulate(tokens, headers=["Token", "Tipo"], tablefmt="fancy_grid", stralign="center", disable_numparse=True))
    file.close()
if __name__ == '__main__':
    lexerAritmetico(input("Arrastrar o ingresar el nombre del archivo a leer: "))
