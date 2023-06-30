#!/usr/bin/env python3

from datetime import time
from datetime import date
from datetime import datetime
import os
import _aux as aux

def get_int(input_str):
    while True:
        num_censo = input(input_str)
        try:
            num_censo = int(num_censo)
            break
        except ValueError:
            if num_censo == "p" or num_censo == "porcentaje" or num_censo == "%":
                return "p"
            if num_censo == "q":
                return "q"
            if num_censo == "r":
                return "r"
            print("[ERROR] Sólo se admiten enteros")
            continue
    return num_censo

def get_percent(votantes, censo, archivo):
    percent = (votantes / censo) * 100
    string = "** PORCENTAJE DE VOTOS " + (datetime.now().strftime("%H:%M:%S")) + ": " + str(round(percent, 2)) + "% **"
    print(string)
    archivo.write(string + "\n")


def run(num_censo):
    lista_votos = []
    i = 0

    filestring = "censo_count_" + datetime.now().strftime("%Y-%m-%d") + ".txt"
    if os.path.exists(filestring):
        iprint("[INFO] Existe ya un registro de votos en " + os.path.realpath(filestring) + ".")
        preg = input("¿Borrar? S/n >")
        if preg == "S" or preg == "s":
            open(filestring, 'w').close()
        else:
            eprint("Abandonando programa debido a registro de votos existente.")
            exit(1)
    else:
        open(filestring, 'w').close()


    while len(lista_votos) < num_censo:
        numero = get_int("* Número de censo del nuevo votante: ")

        if numero == "p":
            f = open(filestring, "a")
            get_percent(i, num_censo, f)
            f.close()
            continue

        if numero == -1 or numero == "q":
            iprint("[INFO] La votación ha terminado.")
            #get_percent(i, num_censo, f)
            break

        if numero == "r":
            f = open(filestring, "a")
            get_percent(i, num_censo, f)
            f.close()
            aux.fileopen(os.path.realpath(filestring))
            continue

        if numero == 0:
            i = get_int("* Número de votos hasta ahora: ")
            f = open(filestring, "a")
            f.write("... [" + (datetime.now().strftime("%H:%M:%S")) + "] - ...\n")
            f.close()
            continue

        else:
            if numero > num_censo or numero in lista_votos :
                eprint("[ERROR] Valor inválido")
                continue
            else:
                lista_votos.append(numero)
                i = i + 1
                now = datetime.now()
                f = open(filestring, "a")
                f.write(str(i) + " [" + (now.strftime("%H:%M:%S")) + "] - " + str(numero) + "\n")
                f.close()
    
    return(i)