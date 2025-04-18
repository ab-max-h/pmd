#!/usr/bin/env python3
# algorithms/main.py

from read import leer_datos_manualmente
from enumeration import metodo_enumeracion
from pro_lineal import metodo_programacion_lineal
from pol_mejoradas import metodo_policy_improvement


def main():
    print("=== LECTURA DE DATOS PARA PMD ===\n")
    datos = leer_datos_manualmente()

    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1) Enumeración Exhaustiva de Políticas")
        print("2) Programación Lineal")
        print("3) Mejoramiento de políticas")
        print("Q) Salir")
        opc = input("Elige una opción: ").strip().lower()

        if opc == '1':
            metodo_enumeracion(datos)
        elif opc == '2':
            metodo_programacion_lineal(datos)
        elif opc == '3':
            metodo_policy_improvement(datos)
        elif opc in ('q', 'salir'):
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
