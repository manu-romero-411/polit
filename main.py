# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import censo_count
import dhondt
import _aux as aux

def get_int(input_str):
    while True:
        try:
            num = int(input(input_str))
            break
        except ValueError:
            aux.eprint("[ERROR] Sólo se admiten enteros")
            continue
    return num


def run_censo_count(num_censo):
    aux.iprint("****")
    lista_votantes = censo_count.run(num_censo)

    porcentaje = (lista_votantes/num_censo)*100
    print("Número de votos: " + str(lista_votantes) + " / " + str(num_censo) + " (" + str(round(porcentaje, 2)) + " %)")
    continua = input("* ¿Contar votos? S/n >")
    if continua == "S" or continua == "s":
        num_partidos = get_int("* Número de partidos que se han presentado: ")
        run_voto_count(num_censo, lista_votantes, num_partidos)
    else:
        aux.iprint("[INFO] Saliendo del programa...")
        exit(0)

def run_voto_count(num_censo, num_votantes, num_partidos):
    aux.iprint("****")
    lista_votos = censo_count.run(num_votantes, num_partidos)
    for i in range (0, len(lista_votos)):
        print("* " + str(i+1) + ". " + str(lista_votos[i][0]) + " - " + str(lista_votos[i][1]))
        suma = suma + lista_votos[i][1]

    continua = input("* ¿Sacar escaños? S/n >")
    if continua == "S" or continua == "s":
        run_repartir_escanos()
    else:
        aux.iprint("[INFO] Saliendo del programa...")
        exit(0)

def run_repartir_escanos():
    aux.iprint("****")
    metodo = input("* Introduce método de reparto (dhondt | sainte-lague | hare): ")
    num_partidos = get_int("* Introduce número de partidos: ")
    num_escanos = get_int("* Escaños totales de la circunscripción/municipio: ")
    votos_blancos = get_int("* Votos en blanco: ")
    dhondt.run(metodo, num_partidos, num_escanos, votos_blancos);
    exit(0)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("*** POLIT - PARA EL POLITICUCHO PICATECLAS ***")
    print("1 - Contar votantes a partir del censo")
    print("2 - Contar votos de cada partido")
    print("3 - Aplicar la ley D'Hondt para repartir escaños")
    print("q - Salir")
    while True:
        opcion = input("* Selecciona una opción: ")
        try:
            opcion = int(opcion)
            break
        except ValueError:
            if opcion == "q":
                exit(0)
            aux.eprint("[ERROR] Sólo se admiten enteros")
            continue

    if opcion == 1:
        aux.iprint("****")
        aux.ipraux.iprintint("CONTADOR DE VOTANTES DEL CENSO EN UNA MESA")
        run_censo_count(get_int("* Número de personas en el censo: "))
    elif opcion == 2:
        aux.iprint("****")
        aux.iprint("CONTADOR DE VOTOS POR PARTIDO")
        run_voto_count(get_int("* Número de personas en el censo: "), get_int("* Número de votantes: "), get_int("* Número de partidos: "))
    elif opcion == 3:
        aux.iprint("****")
        aux.iprint("CALCULADORA DE REPARTICIÓN DE ESCAÑOS")
        aux.iprint("****")
        run_repartir_escanos()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
