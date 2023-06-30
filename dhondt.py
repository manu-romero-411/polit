import argparse
import math
from operator import itemgetter
from prettytable import PrettyTable
import _aux as aux

def generar_lista_partidos(num):
    lista_partidos = []
    for i in range(1, num + 1):
        aux.iprint("****")
        nombre = input("* Partido " + str(i) + " - Nombre: ")
        num_votos = 0
        bucle = True
        while bucle:
            try:
                num_votos = int(input("* Partido " + str(i) + " - Votos: "))
            except ValueError:
                aux.eprint("[ERROR] Se debe introducir un entero positivo")
            else:
                bucle = False
        partido = (nombre, num_votos)
        lista_partidos.append(partido)
        aux.iprint("****")

    return(sorted(lista_partidos, key=itemgetter(1), reverse=True))

def hare_calc(sillas, lista_partidos):
    calculo = []
    aux2 = []
    suma = 0
    for i in range(0,len(lista_partidos)):
        suma = suma + lista_partidos[i][1]
    
    coc = suma / sillas

    sumaaux = 0
    for i in range(0,len(lista_partidos)):
        division = math.modf(lista_partidos[i][1]/coc)
        aux2.append((lista_partidos[i][0], division[0]))
        sumaaux = sumaaux + int(division[1])
        for j in range(0, int(division[1])):
            calculo.append((lista_partidos[i][0], j))

    aux2 = sorted(aux2, key=itemgetter(1), reverse=True)

    for i in range(0, sillas - int(sumaaux)):
        calculo.append(aux2[i])
    
    return(calculo)


def dhondt_calc(sillas, lista_partidos):
    calculo = []
    divisor = 0
    for i in range(0, sillas):
        divisor = divisor + 1
        for j in range(0, len(lista_partidos)):
            division = lista_partidos[j][1]/divisor
            calculo.append((lista_partidos[j][0], division))

    return(sorted(calculo, key=itemgetter(1), reverse=True)[:sillas])

def sainte_lague_calc(sillas, lista_partidos):
    calculo = []
    divisor = 1
    for i in range(0, sillas, 2):
        for j in range(0, len(lista_partidos)):
            division = lista_partidos[j][1]/divisor
            calculo.append((lista_partidos[j][0], division))
        divisor = divisor + 2

    return(sorted(calculo, key=itemgetter(1), reverse=True)[:sillas])

def run(metodo, num_partidos, num_escanos, votos_blancos):
    lista_partidos = generar_lista_partidos(num_partidos)
    pop = votos_blancos
    for i in lista_partidos:
        pop = pop + i[1]

    coste = pop/num_escanos
    calculos = []
    if metodo == "dhondt":
        calculos = dhondt_calc(num_escanos, lista_partidos)
    elif metodo == "sainte_lague":
        calculos = sainte_lague_calc(num_escanos, lista_partidos)
    elif metodo == "hare":
        calculos = hare_calc(num_escanos, lista_partidos)
    else:
        aux.eprint("[ERROR] Método inválido: " + metodo)
        exit(1)

    resultados = []
    for i in lista_partidos:
        cont = 0
        for j in calculos:
            if j[0] == i[0]:
                cont = cont + 1
        if cont == 0:
            resultados.append((i[0], i[1], cont, -1))
        else:
            ratio = (i[1]/cont - coste) * 100 / pop
            resultados.append((i[0], i[1], cont, ratio))

    tabla_result = PrettyTable(["Partido", "Votos", "Escaños", "% Sobrecoste escaño"])
    for i in resultados:
        tabla_result.add_row([i[0], i[1], i[2], i[3]])

    print(tabla_result)
    return resultados