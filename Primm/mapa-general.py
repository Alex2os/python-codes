import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import math


# =========================
# 1. LOAD MAP AND VERTICES
# =========================

# Change these depending on the map pair:
# mapaChiquito.PNG  -> verticeChiquito.npy
# mapa1.png         -> verticeMapa1.npy
# mapa2.png         -> verticeMapa2.npy
# mapa3.png         -> verticeMapa3.npy

nombre_mapa = "mapa2.png"
nombre_vertices = "verticeMapa2.npy"

imagen = Image.open(nombre_mapa).convert("RGB")
mapa_original = np.array(imagen)

vertices = np.load(nombre_vertices)

# IMPORTANT:
# The vertices work correctly over the transposed map.
# So from now on, street detection will also use this same map.
mapa_trabajo = np.transpose(mapa_original, (1, 0, 2))

print("Tamaño del mapa original:", imagen.size)
print("Tamaño del mapa de trabajo:", mapa_trabajo.shape)
print("Cantidad de vértices:", len(vertices))
print("Vértices:")
print(vertices)


# =========================
# 2. DISTANCE FUNCTION
# =========================

def calcular_distancia(v1, v2):
    x1, y1 = v1
    x2, y2 = v2

    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    return distancia


# ==========================================
# 3. CHECK IF A PIXEL IS STREET COLOR
# ==========================================

def es_color_calle(pixel, tolerancia=18):
    pixel = np.array(pixel, dtype=int)

    colores_calle = [
        # Originales
        np.array([248, 249, 250], dtype=int),
        np.array([249, 250, 251], dtype=int),
        np.array([247, 248, 249], dtype=int),
        np.array([255, 255, 255], dtype=int),
        np.array([241, 241, 241], dtype=int),
        np.array([240, 240, 240], dtype=int),
        np.array([239, 239, 239], dtype=int),
        np.array([238, 238, 238], dtype=int),
        np.array([237, 237, 237], dtype=int),
        # Nuevos colores de mapa2.png y otros mapas (beige, amarillos, grises oscuros)
        np.array([254, 248, 241], dtype=int),
        np.array([255, 247, 238], dtype=int),
        np.array([255, 248, 237], dtype=int),
        np.array([189, 189, 193], dtype=int),
        np.array([225, 229, 229], dtype=int),
        np.array([217, 221, 221], dtype=int),
        np.array([197, 201, 217], dtype=int),
        np.array([250, 250, 254], dtype=int),
        np.array([229, 229, 233], dtype=int),
        np.array([245, 245, 245], dtype=int),
        np.array([213, 213, 217], dtype=int),
        np.array([197, 197, 201], dtype=int),
        np.array([209, 213, 213], dtype=int),
        np.array([242, 242, 242], dtype=int),
        np.array([206, 206, 206], dtype=int),
        np.array([233, 233, 233], dtype=int)
    ]

    # Threshold heurístico general (por si el color no está exactamente en la lista):
    # Muchos pixeles de calle son claros (RGB altos) y no muy saturados.
    r, g, b = pixel[0], pixel[1], pixel[2]
    if r > 190 and g > 190 and b > 190:
        if max(r, g, b) - min(r, g, b) < 35:
            return True

    for color in colores_calle:
        diferencia = np.abs(pixel - color)

        if np.all(diferencia <= tolerancia):
            return True

    return False


# =====================================================
# 4. CHECK IF TWO VERTICES CAN BE CONNECTED
# =====================================================

def conexion_valida(mapa, v1, v2, porcentaje_minimo=0.55):
    alto, ancho, _ = mapa.shape

    # --- CHEQUEO DEL PUNTO MEDIO EXACTO (SUGERENCIA DEL USUARIO) ---
    # Sacamos el punto medio exacto entre v1 y v2
    pm_exacto_x = int(round((v1[0] + v2[0]) / 2.0))
    pm_exacto_y = int(round((v1[1] + v2[1]) / 2.0))
    
    # Si el punto medio exacto no es calle, rechazamos la conexión inmediatamente
    # (Evita falsos positivos donde la línea cruza un edificio por el medio)
    if 0 <= pm_exacto_x < ancho and 0 <= pm_exacto_y < alto:
        if not es_color_calle(mapa[pm_exacto_y, pm_exacto_x]):
            return False
    else:
        return False
    # ---------------------------------------------------------------

    # Función recursiva para obtener los puntos medios (promedios)
    def obtener_puntos_medios(p1, p2, profundidad):
        if profundidad == 0:
            return []
        
        # Sacar el punto medio (promedio) de estos
        pm = ((p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0)
        
        # Recursión para sacar múltiples puntos medios
        puntos_izq = obtener_puntos_medios(p1, pm, profundidad - 1)
        puntos_der = obtener_puntos_medios(pm, p2, profundidad - 1)
        
        return puntos_izq + [pm] + puntos_der

    distancia = calcular_distancia(v1, v2)
    
    if distancia == 0:
        return False

    # Determinamos la profundidad de la recursión basada en la distancia.
    # Una profundidad de N genera (2^N - 1) puntos medios.
    # log2(distancia) nos asegura que revisamos aproximadamente cada pixel.
    if distancia < 2:
        profundidad = 1
    else:
        profundidad = int(math.log2(distancia)) + 1

    puntos = obtener_puntos_medios(v1, v2, profundidad)
    
    puntos_validos = 0
    puntos_totales = len(puntos)
    
    if puntos_totales == 0:
        return False

    for p in puntos:
        x = int(round(p[0]))
        y = int(round(p[1]))
        
        if 0 <= x < ancho and 0 <= y < alto:
            # Comprobar el color de los pixeles
            if es_color_calle(mapa[y, x]):
                puntos_validos += 1

    porcentaje = puntos_validos / puntos_totales

    return porcentaje >= porcentaje_minimo


# ==============================================
# 5. CREATE VALID EDGE LIST
# ==============================================

def crear_aristas(vertices, mapa):
    aristas = []

    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            v1 = vertices[i]
            v2 = vertices[j]

            if conexion_valida(mapa, v1, v2):
                costo = calcular_distancia(v1, v2)

                aristas.append([i, j, costo])

    aristas.sort(key=lambda arista: arista[2])

    return aristas


# ==============================================
# 6. PRIM ALGORITHM
# ==============================================

def prim(vertices, aristas, inicio=0):
    n = len(vertices)
    
    # Según las instrucciones: "No se puede usar nada que sea inf, max o números grandes, más allá de 1417"
    infinito = 1417
    
    # Construimos la matriz de adyacencia (el grafo) a partir de las aristas
    grafo = [[infinito for _ in range(n)] for _ in range(n)]
    
    for arista in aristas:
        u, v, costo = arista
        grafo[u][v] = costo
        grafo[v][u] = costo
        
    # Inicializamos arreglos para el algoritmo de Prim
    key = [infinito] * n
    padre = [-1] * n
    visitados = [False] * n
    
    key[inicio] = 0
    
    arbol_expansion_minima = []
    costo_total = 0
    
    for _ in range(n):
        # Encontrar el vértice con el valor mínimo de key que no ha sido visitado
        min_val = infinito + 1
        u = -1
        for i in range(n):
            if not visitados[i] and key[i] < min_val:
                min_val = key[i]
                u = i
                
        # Si u es -1, significa que no hay más vértices conectables (grafo desconectado)
        if u == -1:
            print("No se pudo conectar todos los vértices. Algunos quedaron aislados.")
            break
            
        visitados[u] = True
        
        # Si tiene un padre (es decir, no es el nodo de inicio), lo agregamos al MST
        if padre[u] != -1:
            arbol_expansion_minima.append([padre[u], u, grafo[u][padre[u]]])
            costo_total += grafo[u][padre[u]]
            
        # Actualizamos los valores de key para los vértices adyacentes a u
        for v in range(n):
            if grafo[u][v] != infinito and not visitados[v] and grafo[u][v] < key[v]:
                key[v] = grafo[u][v]
                padre[v] = u
                
    return arbol_expansion_minima, costo_total


# ==============================================
# 7. RUN PROCESS
# ==============================================

# IMPORTANT:
# We create edges using mapa_trabajo, not mapa_original.
aristas = crear_aristas(vertices, mapa_trabajo)

print("\nCantidad de aristas válidas:", len(aristas))

arbol, costo_total = prim(vertices, aristas, inicio=0)

print("\nÁrbol de expansión mínima:")
for arista in arbol:
    print(f"V{arista[0]} - V{arista[1]} | Costo: {arista[2]:.2f}")

print(f"\nCosto total del árbol de expansión mínima: {costo_total:.2f}")


# ==============================================
# 8. SHOW MAP WITH MINIMUM SPANNING TREE
# ==============================================

# Base map is already the same map used for street detection
mapa_base = mapa_trabajo

# Rotate -90 degrees
mapa_grafico = np.rot90(mapa_base, k=-1)

# Mirror once horizontally
mapa_grafico = np.flip(mapa_grafico, axis=1)

alto_grafico, ancho_grafico, _ = mapa_grafico.shape
alto_base, ancho_base, _ = mapa_base.shape

plt.figure(figsize=(12, 10))
plt.imshow(mapa_grafico)

# Draw all valid edges in light gray
for arista in aristas:
    i = arista[0]
    j = arista[1]

    x1, y1 = vertices[i]
    x2, y2 = vertices[j]

    # Rotate graph coordinates -90 degrees
    x1_rot = alto_base - 1 - y1
    y1_rot = x1

    x2_rot = alto_base - 1 - y2
    y2_rot = x2

    # Mirror horizontally
    x1_final = ancho_grafico - 1 - x1_rot
    x2_final = ancho_grafico - 1 - x2_rot

    plt.plot(
        [x1_final, x2_final],
        [y1_rot, y2_rot],
        linewidth=1,
        alpha=0.12,
        color="gray"
    )

# Draw MST edges in red
for arista in arbol:
    i = arista[0]
    j = arista[1]

    x1, y1 = vertices[i]
    x2, y2 = vertices[j]

    # Rotate graph coordinates -90 degrees
    x1_rot = alto_base - 1 - y1
    y1_rot = x1

    x2_rot = alto_base - 1 - y2
    y2_rot = x2

    # Mirror horizontally
    x1_final = ancho_grafico - 1 - x1_rot
    x2_final = ancho_grafico - 1 - x2_rot

    plt.plot(
        [x1_final, x2_final],
        [y1_rot, y2_rot],
        linewidth=3,
        color="red"
    )

# Draw vertices
for i in range(len(vertices)):
    x, y = vertices[i]

    # Rotate graph coordinates -90 degrees
    x_rot = alto_base - 1 - y
    y_rot = x

    # Mirror horizontally
    x_final = ancho_grafico - 1 - x_rot

    plt.scatter(x_final, y_rot, s=45, color="blue")
    plt.text(
        x_final + 5,
        y_rot + 5,
        f"V{i}",
        fontsize=8,
        color="black",
        bbox=dict(facecolor="white", alpha=0.7, edgecolor="none")
    )

plt.title("Árbol de Expansión Mínima - Algoritmo de Prim")
plt.axis("off")
plt.show()