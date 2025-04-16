#!/usr/bin/env python3
# algorithms/main.py

from read import leer_datos_manualmente
from enumeration import metodo_enumeracion


def main():
    print("=== LECTURA DE DATOS PARA PMD ===\n")
    datos = leer_datos_manualmente()

    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1) Enumeración Exhaustiva de Políticas")
#        print("2) Método 2 (pendiente)")
#        print("3) Método 3 (pendiente)")
        print("Q) Salir")
        opc = input("Elige una opción: ").strip().lower()

        if opc == '1':
            metodo_enumeracion(datos)
        elif opc in ('q', 'salir'):
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
