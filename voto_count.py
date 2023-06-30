#!/usr/bin/env python3

import sys
import os
from datetime import datetime
from collections import Counter

def write_init(file, party):
    dir = "recuento_" + datetime.now().strftime("%Y-%m-%d")
    if not os.path.exists(dir):
        os.mkdir(dir)
    f = open(os.path.join(dir, file + ".txt"), "a")
    f.write("===\n" + party + "\n===\n")
    f.close()

def write_x(file, votes):
    dir = "recuento_" + datetime.now().strftime("%Y-%m-%d")
    string = "*"
    if votes % 10 == 0:
        string = string + "\n"
        if votes % 100 == 0:
            string = string + "\n"

    f = open(os.path.join(dir, file + ".txt"), "a")
    f.write(string)
    f.close()

def define_parties(file):
    dir = "recuento_" + datetime.now().strftime("%Y-%m-%d")
    if os.path.exists(os.path.join(dir, file + ".txt")):
        party = ""
        count = 0
        with open(os.path.join(dir, file + ".txt"), "r") as f:
            lines = f.readlines()

            party = lines[1].rstrip()
            for line in lines:
                count = count + Counter(line)["*"]

        return party,count
    else:
        write_init(file, file)
        return (file, 0)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def recuento(party_list, blancos, nulos, num_votantes):
    suma = 0
    print("*********")
    for i in range (0, len(party_list)):
        print("* " + str(i+1) + ". " + str(party_list[i][0]) + " - " + str(party_list[i][1]))
        suma = suma + party_list[i][1]
    print("* 0. Votos en blanco - " + str(blancos))
    print("* X. Votos nulos - " + str(nulos))
    print("*********")
    return num_votantes - (suma + blancos + nulos)

def get_int(input_str):
    while True:
        num = input(input_str)
        try:
            num = int(num)
            break
        except ValueError:
            if num == "e":
                return "e"
            if num == "q":
                return "q"
            if num == "h":
                return "h"
            if num == "r":
                return "r"
            eprint("[ERROR] Sólo se admiten enteros")
            continue
    return num

def help(party_list):
    iprint("*********")
    for i in range(0, len(party_list)):
        print("* " + str(i+1) + " - " + party_list[i][0])

    print("* 0 - Blancos")
    print("* -1 - Nulos")
    iprint("*********")

def run(num_votantes, num_partidos):
    party_list = []
    votos = num_votantes

    for i in range(0, num_partidos):
        party_list.append(define_parties(input("* Nombre del partido: ")))

    define_parties("_blancos")
    define_parties("_nulos")
    blancos = 0
    nulos = 0

    votos = recuento(party_list, blancos, nulos, num_votantes)

    while votos > 0:
        nuevo_voto = get_int(bcolors.WARNING + "* Partido con nuevo voto: " + bcolors.ENDC)
        if nuevo_voto == "e":
            recuento(party_list, blancos, nulos)
            delet = get_int("* ¿Dónde eliminar un voto de más?")
            if isinstance(delet, int):
                if delet >= -1 and delet <= len(party_list):
                    party_list[delet - 1] = (party_list[delet - 1][0], party_list[delet - 1][1] - 1)
                    votos = votos + 1
            continue

        if nuevo_voto == "h":
            help(party_list)
            continue
        if nuevo_voto == "q":
            break

        if nuevo_voto == "r":
            votos = recuento(party_list, blancos, nulos, num_votantes)
            continue

        if isinstance(nuevo_voto, int):
            if nuevo_voto == 0:
                blancos = blancos + 1
                write_x("_blancos", blancos)
                votos = votos - 1
                continue
            elif nuevo_voto == -1:
                nulos = nulos + 1
                votos = votos - 1
                write_x("_nulos", nulos)

                continue
            elif nuevo_voto > len(party_list) or nuevo_voto < -1:
                print(bcolors.FAIL + "[ERROR] Número de partido no válido." + bcolors.ENDC)
                help(party_list)
                continue
            else:
                party_list[nuevo_voto-1] = (party_list[nuevo_voto-1][0], party_list[nuevo_voto-1][1] + 1)
                write_x(party_list[nuevo_voto-1][0], party_list[nuevo_voto-1][1])
                votos = votos - 1

    recuento(party_list, blancos, nulos, num_votantes)
    party_list.append(("_blancos", blancos))
    party_list.append(("_nulos", blancos))

    return(party_list)