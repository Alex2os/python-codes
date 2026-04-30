import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import math


# =========================
# 1. CARGAR MAPA Y VÉRTICES
# =========================

nombre_mapa = "mapaChiquito.png"
nombre_vertices = "verticeChiquito.npy"

imagen = Image.open(nombre_mapa).convert("RGB")
mapa = np.array(imagen)

vertices = np.load(nombre_vertices)

print("Tamaño del mapa:", imagen.size)
print("Cantidad de vértices:", len(vertices))
print("Vértices:")
print(vertices)


# =========================
# 2. FUNCIÓN PARA DISTANCIA
# =========================

def calcular_distancia(v1, v2):
    x1, y1 = v1
    x2, y2 = v2

    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    return distancia


# ==========================================
# 3. FUNCIÓN PARA REVISAR SI UN PIXEL ES CALLE
# ==========================================

def es_pixel_calle(pixel):
    r, g, b = pixel

    # Calles del mapa: normalmente son blancas o gris muy claro.
    # Edificios/fondo tienden a ser más beige o gris oscuro.
    if r >= 220 and g >= 220 and b >= 220:
        return True
    else:
        return False


# =====================================================
# 4. VALIDAR SI DOS VÉRTICES SE PUEDEN CONECTAR
# =====================================================

def conexion_valida(mapa, v1, v2, muestras=40, porcentaje_minimo=0.80):
    alto, ancho, canales = mapa.shape

    x1, y1 = v1
    x2, y2 = v2

    puntos_validos = 0
    puntos_totales = 0

    for i in range(muestras + 1):
        t = i / muestras

        x = round(x1 + (x2 - x1) * t)
        y = round(y1 + (y2 - y1) * t)

        # Revisar que el punto esté dentro del mapa
        if x >= 0 and x < ancho and y >= 0 and y < alto:
            pixel = mapa[y, x]
            puntos_totales += 1

            if es_pixel_calle(pixel):
                puntos_validos += 1

    if puntos_totales == 0:
        return False

    porcentaje_valido = puntos_validos / puntos_totales

    if porcentaje_valido >= porcentaje_minimo:
        return True
    else:
        return False


# ==============================================
# 5. CREAR LISTA DE ARISTAS VÁLIDAS
# ==============================================

def crear_aristas(vertices, mapa):
    aristas = []

    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            v1 = vertices[i]
            v2 = vertices[j]

            if conexion_valida(mapa, v1, v2):
                costo = calcular_distancia(v1, v2)

                # Se guarda:
                # índice del vértice 1, índice del vértice 2, costo
                aristas.append([i, j, costo])

    # Ordenar de menor a mayor costo
    aristas.sort(key=lambda arista: arista[2])

    return aristas


# ==============================================
# 6. ALGORITMO DE PRIM MANUAL
# ==============================================

def prim(vertices, aristas, inicio=0):
    visitados = [inicio]
    arbol_expansion_minima = []
    costo_total = 0

    while len(visitados) < len(vertices):
        se_agrego_arista = False

        for arista in aristas:
            v1 = arista[0]
            v2 = arista[1]
            costo = arista[2]

            condicion_1 = v1 in visitados and v2 not in visitados
            condicion_2 = v2 in visitados and v1 not in visitados

            if condicion_1:
                arbol_expansion_minima.append(arista)
                visitados.append(v2)
                costo_total += costo
                se_agrego_arista = True
                break

            elif condicion_2:
                arbol_expansion_minima.append(arista)
                visitados.append(v1)
                costo_total += costo
                se_agrego_arista = True
                break

        if se_agrego_arista == False:
            print("No se pudo conectar todos los vértices.")
            break

    return arbol_expansion_minima, costo_total


# ==============================================
# 7. EJECUTAR PROCESO
# ==============================================

aristas = crear_aristas(vertices, mapa)

print("\nLista de aristas ordenadas de menor a mayor:")
for arista in aristas:
    print(f"V{arista[0]} - V{arista[1]} | Costo: {arista[2]:.2f}")

arbol, costo_total = prim(vertices, aristas, inicio=0)

print("\nÁrbol de expansión mínima:")
for arista in arbol:
    print(f"V{arista[0]} - V{arista[1]} | Costo: {arista[2]:.2f}")

print(f"\nCosto total del árbol de expansión mínima: {costo_total:.2f}")


# ==============================================
# 8. SHOW MAP WITH MINIMUM SPANNING TREE
# ==============================================

# Base map that matches the graph coordinates
mapa_base = np.transpose(mapa, (1, 0, 2))

# Rotate the map -90 degrees (clockwise)
mapa_grafico = np.rot90(mapa_base, k=-1)

# Mirror it one more time horizontally
mapa_grafico = np.flip(mapa_grafico, axis=1)

alto_grafico, ancho_grafico, _ = mapa_grafico.shape
alto_base, ancho_base, _ = mapa_base.shape

plt.figure(figsize=(8, 8))
plt.imshow(mapa_grafico)

# Draw all valid edges in light gray
for arista in aristas:
    i = arista[0]
    j = arista[1]

    # DO NOT CHANGE THIS PART
    x1, y1 = vertices[i]
    x2, y2 = vertices[j]

    # Step 1: rotate graph coordinates -90 degrees
    x1_rot = alto_base - 1 - y1
    y1_rot = x1

    x2_rot = alto_base - 1 - y2
    y2_rot = x2

    # Step 2: mirror horizontally
    x1_final = ancho_grafico - 1 - x1_rot
    x2_final = ancho_grafico - 1 - x2_rot

    plt.plot([x1_final, x2_final], [y1_rot, y2_rot],
             linewidth=1, alpha=0.25, color="gray")

# Draw MST edges
for arista in arbol:
    i = arista[0]
    j = arista[1]

    # DO NOT CHANGE THIS PART
    x1, y1 = vertices[i]
    x2, y2 = vertices[j]

    # Step 1: rotate graph coordinates -90 degrees
    x1_rot = alto_base - 1 - y1
    y1_rot = x1

    x2_rot = alto_base - 1 - y2
    y2_rot = x2

    # Step 2: mirror horizontally
    x1_final = ancho_grafico - 1 - x1_rot
    x2_final = ancho_grafico - 1 - x2_rot

    plt.plot([x1_final, x2_final], [y1_rot, y2_rot],
             linewidth=3, color="red")

# Draw vertices
for i in range(len(vertices)):
    # DO NOT CHANGE THIS PART
    x, y = vertices[i]

    # Step 1: rotate graph coordinates -90 degrees
    x_rot = alto_base - 1 - y
    y_rot = x

    # Step 2: mirror horizontally
    x_final = ancho_grafico - 1 - x_rot

    plt.scatter(x_final, y_rot, s=80, color="blue")
    plt.text(x_final + 5, y_rot + 5, f"V{i}", fontsize=10)

plt.title("Árbol de Expansión Mínima - Algoritmo de Prim")
plt.axis("off")
plt.show()

