#!/usr/bin/env python3
# algorithms/method_policy_improvement.py

"""
Iteración de Políticas (Policy Improvement) para PMD de costo medio.
Se resuelve g y v_0…v_{n-1} fijando v_{n-1}=0, luego se mejora la política
usando Δ₍i,a₎ = c_{i,a} + Σ_j P_a[i,j]·v_j – v_i.
"""

import numpy as np
from read import leer_datos_manualmente

def evaluar_politica(politica, datos):
    """
    Evalúa la política actual:
      - Incógnitas: v_0…v_{n-1}, g
      - Eqs i=0…n-1:  v_i – Σ_j Pπ(i)[i,j]·v_j – g = –c_{i,π(i)}
      - Ecuación n   : v_{n-1} = 0
    Retorna (g, v_signed) donde v_signed = –v_raw para ajustar signo.
    """
    n     = datos["num_estados"]
    probs = datos["probabilidades"]
    costos= datos["costos"]

    # Construir matriz de transición y vector de costos de la política
    Pmat = np.zeros((n, n))
    cvec = np.zeros(n)
    for i, a in enumerate(politica):
        Pmat[i, :] = probs[a][i]
        cvec[i]    = costos[a][i]

    # Montar sistema A·x = b con x = [v_0…v_{n-1}, g]
    N = n + 1
    A = np.zeros((N, N))
    b = np.zeros(N)

    # Ecuaciones i = 0…n-1
    for i in range(n):
        # Coeficientes de v_j
        for j in range(n):
            A[i, j] = (1.0 if i == j else 0.0) - Pmat[i, j]
        # Coeficiente de g
        A[i, n] = -1.0
        # Lado derecho = –c_i
        b[i]    = -cvec[i]

    # Ecuación n: v_{n-1} = 0
    A[n, n-1] = 1.0
    b[n]       = 0.0

    # Resolver el sistema
    sol    = np.linalg.solve(A, b)
    v_raw  = sol[:n]
    g      = sol[n]

    # --- Cambio: invertimos signo de v para que Δ funcione correctamente ---
    v_signed = -v_raw

    return g, v_signed

def metodo_policy_improvement(datos):
    problema_tipo = datos["problema_tipo"].lower()  # "maximizar" o "minimizar"
    n             = datos["num_estados"]
    politicas     = datos["politicas"]
    probs         = datos["probabilidades"]
    costos        = datos["costos"]

    # Construir D(i): acciones viables por estado
    D = {i: [] for i in range(n)}
    for a, estados in politicas.items():
        for i in estados:
            D[i].append(a)

    # 0) Leer política inicial
    while True:
        entrada = input(f"Ingrese política inicial ({n} acciones, coma-sep.): ")
        try:
            pol = tuple(int(x) for x in entrada.split(","))
            if len(pol) != n or any(pol[i] not in D[i] for i in range(n)):
                raise ValueError
            break
        except:
            print("Política inválida, inténtalo de nuevo.")

    iter_count = 0
    while True:
        iter_count += 1
        print(f"\n--- Iteración {iter_count} ---")

        # 1) Evaluar política
        g, v = evaluar_politica(pol, datos)
        print(f" g = {g:.6f}")
        for i, vi in enumerate(v):
            print(f" v_{i} = {vi:.6f}")

        # 2) Mejorar política
        nueva = []
        for i in range(n):
            candidatos = {}
            for a in D[i]:
                delta = costos[a][i] + np.dot(probs[a][i], v) - v[i]
                candidatos[a] = delta
            if problema_tipo.startswith("max"):
                mejor = max(candidatos, key=candidatos.get)
            else:
                mejor = min(candidatos, key=candidatos.get)
            nueva.append(mejor)
        nueva = tuple(nueva)

        print(" Política mejorada:", nueva)

        # 3) Verificar convergencia
        if nueva == pol:
            print(f"\nConvergió en {iter_count} iteraciones.")
            print("Política Óptima:", pol)
            print(f" g* = {g:.6f}")
            for i, vi in enumerate(v):
                print(f" v*_{i} = {vi:.6f}")
            break

        pol = nueva
