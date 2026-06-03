"""
============================================================
  SIMULADOR DE CHISPAZO
============================================================
Proyecto de practica de Python - Programacion logica y de azar.

Este programa simula el juego de loteria mexicano "Chispazo":
  - Eliges 5 numeros del 1 al 28.
  - La "urna" sortea 5 numeros al azar.
  - Ganas un premio segun cuantos numeros aciertes (2, 3, 4 o 5).

FUNCIONA EN TODOS LADOS:
  - En una terminal (Codespaces, CMD, etc.): muestra un menu para jugar.
  - Si no hay terminal interactiva (al darle "Run" en algunos sitios):
    corre solo una DEMOSTRACION automatica para que siempre veas resultados.

Conceptos de Python que se practican aqui:
  - Modulo random (numeros al azar, como el ejercicio de dados)
  - Listas y conjuntos (sets) para comparar numeros
  - Diccionarios para guardar estadisticas
  - Lectura/escritura de archivos JSON
  - Funciones, ciclos, condicionales y validacion de datos
  - Conteo de frecuencias con collections.Counter
  - Combinatoria con math.comb para calcular probabilidades

Autor: (tu nombre)
============================================================
"""

import sys
import random
import json
import os
from collections import Counter
from math import comb


# ------------------------------------------------------------
# CONSTANTES DEL JUEGO (valores que no cambian)
# ------------------------------------------------------------
NUMERO_MINIMO = 1
NUMERO_MAXIMO = 28
NUMEROS_POR_JUGADA = 5
PRECIO_JUGADA = 10  # pesos (dato real del Chispazo)
ARCHIVO_ESTADISTICAS = "estadisticas.json"

# Premios aproximados en pesos. El premio de 5 aciertos en la vida real
# no es fijo (depende de las ventas). Aqui son solo de referencia.
PREMIOS = {5: 200000, 4: 1247, 3: 50, 2: 10}


# ------------------------------------------------------------
# ENTRADA SEGURA
# Esta funcion lee lo que escribe el usuario. Si NO hay terminal
# disponible (por ejemplo al ejecutar sin consola), en vez de cerrar
# el programa con un error, devuelve None y el programa lo maneja solo.
# ------------------------------------------------------------
def leer(mensaje):
    try:
        return input(mensaje)
    except (EOFError, KeyboardInterrupt):
        return None


# ------------------------------------------------------------
# FUNCIONES DEL JUEGO
# ------------------------------------------------------------
def generar_jugada_aleatoria():
    """Genera 5 numeros distintos del 1 al 28, ordenados."""
    numeros = random.sample(range(NUMERO_MINIMO, NUMERO_MAXIMO + 1), NUMEROS_POR_JUGADA)
    return sorted(numeros)


def pedir_jugada_manual():
    """Pide 5 numeros al usuario y valida que sean correctos.

    Devuelve la lista de numeros, o None si no hay entrada disponible.
    """
    while True:
        entrada = leer(f"Escribe {NUMEROS_POR_JUGADA} numeros del {NUMERO_MINIMO} al "
                       f"{NUMERO_MAXIMO} separados por espacios: ")
        if entrada is None:
            return None  # no hay terminal: el que llama decidira que hacer

        partes = entrada.split()

        if len(partes) != NUMEROS_POR_JUGADA:
            print(f"  -> Debes escribir exactamente {NUMEROS_POR_JUGADA} numeros.\n")
            continue
        try:
            numeros = [int(p) for p in partes]
        except ValueError:
            print("  -> Solo se permiten numeros enteros.\n")
            continue
        if any(n < NUMERO_MINIMO or n > NUMERO_MAXIMO for n in numeros):
            print(f"  -> Los numeros deben estar entre {NUMERO_MINIMO} y {NUMERO_MAXIMO}.\n")
            continue
        if len(set(numeros)) != NUMEROS_POR_JUGADA:
            print("  -> No puedes repetir numeros.\n")
            continue
        return sorted(numeros)


def realizar_sorteo():
    """La urna saca 5 numeros ganadores al azar."""
    return generar_jugada_aleatoria()


def contar_aciertos(jugada, sorteo):
    """Cuenta cuantos numeros coinciden usando interseccion de conjuntos."""
    return len(set(jugada) & set(sorteo))


def describir_resultado(aciertos):
    """Devuelve el mensaje y el premio segun los aciertos."""
    premio = PREMIOS.get(aciertos, 0)
    if aciertos >= 2:
        return f"Acertaste {aciertos} numeros. Premio: ${premio:,} pesos", premio
    return f"Acertaste {aciertos} numeros. Esta vez no hubo premio.", 0


# ------------------------------------------------------------
# ESTADISTICAS (guardar/cargar en archivo JSON)
# ------------------------------------------------------------
def estadisticas_vacias():
    return {
        "jugadas_totales": 0,
        "gastado": 0,
        "ganado": 0,
        "aciertos": {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0},
    }


def cargar_estadisticas():
    """Lee el archivo. Si no existe o esta danado, empieza de cero (sin crashear)."""
    if os.path.exists(ARCHIVO_ESTADISTICAS):
        try:
            with open(ARCHIVO_ESTADISTICAS, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except (json.JSONDecodeError, OSError):
            return estadisticas_vacias()
    return estadisticas_vacias()


def guardar_estadisticas(stats):
    """Guarda las estadisticas. Si no se puede escribir, avisa pero no crashea."""
    try:
        with open(ARCHIVO_ESTADISTICAS, "w", encoding="utf-8") as archivo:
            json.dump(stats, archivo, indent=2, ensure_ascii=False)
    except OSError:
        print("  (Aviso: no se pudo guardar el historial en este entorno.)")


def actualizar_estadisticas(stats, aciertos, premio):
    stats["jugadas_totales"] += 1
    stats["gastado"] += PRECIO_JUGADA
    stats["ganado"] += premio
    stats["aciertos"][str(aciertos)] += 1
    return stats


# ------------------------------------------------------------
# ACCIONES
# ------------------------------------------------------------
def jugar_una_partida():
    """Juega una partida: manual o automatica contra el sorteo."""
    print("\n--- NUEVA PARTIDA ---")
    print("1) Elegir mis numeros")
    print("2) Jugada rapida (numeros al azar)")
    opcion = leer("Opcion: ")

    if opcion is not None and opcion.strip() == "1":
        jugada = pedir_jugada_manual()
        if jugada is None:  # no hubo entrada: usamos una al azar
            jugada = generar_jugada_aleatoria()
            print(f"Sin entrada disponible, jugada al azar: {jugada}")
    else:
        jugada = generar_jugada_aleatoria()
        print(f"Tu jugada rapida es: {jugada}")

    sorteo = realizar_sorteo()
    print(f"\nNumeros ganadores de la urna: {sorteo}")

    aciertos = contar_aciertos(jugada, sorteo)
    mensaje, premio = describir_resultado(aciertos)
    print(mensaje)

    stats = cargar_estadisticas()
    stats = actualizar_estadisticas(stats, aciertos, premio)
    guardar_estadisticas(stats)


def simular_muchos_sorteos(cantidad=None):
    """Repite muchos sorteos y compara la probabilidad real vs la teorica."""
    if cantidad is None:
        while True:
            texto = leer("\nCuantos sorteos quieres simular? (ej. 100000): ")
            if texto is None:
                cantidad = 100000  # valor por defecto si no hay entrada
                break
            try:
                cantidad = int(texto)
                if cantidad > 0:
                    break
            except ValueError:
                pass
            print("  -> Escribe un numero entero positivo.")

    jugada_fija = generar_jugada_aleatoria()
    print(f"\nUsaremos siempre esta jugada: {jugada_fija}")
    print(f"Simulando {cantidad:,} sorteos...\n")

    conteo = Counter()
    for _ in range(cantidad):
        aciertos = contar_aciertos(jugada_fija, realizar_sorteo())
        conteo[aciertos] += 1

    total_combinaciones = comb(NUMERO_MAXIMO, NUMEROS_POR_JUGADA)
    print(f"{'Aciertos':>8} | {'Veces':>10} | {'Real %':>9} | {'Teorica %':>10}")
    print("-" * 48)
    for aciertos in range(NUMEROS_POR_JUGADA, -1, -1):
        veces = conteo.get(aciertos, 0)
        real = veces / cantidad * 100
        favorables = comb(NUMEROS_POR_JUGADA, aciertos) * comb(
            NUMERO_MAXIMO - NUMEROS_POR_JUGADA, NUMEROS_POR_JUGADA - aciertos)
        teorica = favorables / total_combinaciones * 100
        print(f"{aciertos:>8} | {veces:>10,} | {real:>8.4f}% | {teorica:>9.4f}%")

    print(f"\nProbabilidad de acertar los 5: 1 entre {total_combinaciones:,}")
    print("Mientras mas sorteos simules, mas se parecen las columnas Real y Teorica.")
    print("Eso confirma que el sorteo es justo y completamente aleatorio.")


def ver_estadisticas():
    stats = cargar_estadisticas()
    print("\n--- TUS ESTADISTICAS ---")
    print(f"Partidas jugadas: {stats['jugadas_totales']}")
    print(f"Total gastado:    ${stats['gastado']:,} pesos")
    print(f"Total ganado:     ${stats['ganado']:,} pesos")
    print(f"Balance:          ${stats['ganado'] - stats['gastado']:,} pesos")
    print("\nAciertos por partida:")
    for aciertos, veces in stats["aciertos"].items():
        print(f"  {aciertos} aciertos: {veces} veces")


# ------------------------------------------------------------
# MODO DEMOSTRACION (corre solo, sin necesidad de escribir nada)
# Se usa cuando el programa se ejecuta sin terminal interactiva.
# ------------------------------------------------------------
def ejecutar_demostracion():
    print("=== DEMOSTRACION AUTOMATICA ===")
    print("(No se detecto terminal interactiva, asi que corre solo.)\n")

    jugada = generar_jugada_aleatoria()
    sorteo = realizar_sorteo()
    print(f"Jugada de ejemplo: {jugada}")
    print(f"Sorteo de la urna: {sorteo}")
    aciertos = contar_aciertos(jugada, sorteo)
    print(describir_resultado(aciertos)[0])

    simular_muchos_sorteos(cantidad=100000)
    print("\nFin de la demostracion. Para jugar tu mismo, ejecutalo en una terminal.")


# ------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ------------------------------------------------------------
def mostrar_bienvenida():
    print("=" * 50)
    print("        BIENVENIDO AL SIMULADOR DE CHISPAZO")
    print("=" * 50)
    print("Eliges 5 numeros del 1 al 28 y la urna sortea 5.")
    print("Recuerda: es un simulador para aprender, no para ganar dinero.\n")


def menu_interactivo():
    while True:
        print("\n========= MENU =========")
        print("1) Jugar una partida")
        print("2) Simular muchos sorteos (ver probabilidades)")
        print("3) Ver mis estadisticas")
        print("4) Salir")
        opcion = leer("Elige una opcion: ")

        if opcion is None:  # se perdio la entrada: salimos limpio
            print("\nEntrada terminada. Hasta luego!")
            break
        opcion = opcion.strip()

        if opcion == "1":
            jugar_una_partida()
        elif opcion == "2":
            simular_muchos_sorteos()
        elif opcion == "3":
            ver_estadisticas()
        elif opcion == "4":
            print("\nGracias por jugar. Hasta luego!")
            break
        else:
            print("  -> Opcion no valida. Elige 1, 2, 3 o 4.")


def main():
    mostrar_bienvenida()
    # Si hay terminal interactiva, mostramos el menu; si no, corre la demo.
    if sys.stdin.isatty():
        menu_interactivo()
        # Pausa final para que la ventana no se cierre de golpe (doble clic).
        leer("\nPresiona Enter para cerrar...")
    else:
        ejecutar_demostracion()


if __name__ == "__main__":
    main()
