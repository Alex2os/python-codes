import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("mapa3.PNG")
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

vertices = np.load("verticeMapa3.npy")  # vertices en formato (y, x)

R = img_rgb[:, :, 0]
G = img_rgb[:, :, 1]
B = img_rgb[:, :, 2]

# mascara para las calles. en este caso buscamos que las calles se noten con el color blanco en rgb (255, 255, 255)
tolerancia_calles = 4

mascara_calles = (
    (R >= 255 - tolerancia_calles) &
    (G >= 255 - tolerancia_calles) &
    (B >= 255 - tolerancia_calles)
)

# realizamos una lista con los colores exactos, extraidos de los mapas proporcionados.
colors = [
    ("#858d93", 0),
    ("#c5c9d9", 0),
    ("#c5c5c9", 0),
    ("#c5c9cd", 0),
    ("#c4c8d8", 0),
    ("#787c80", 0),
    ("#797d81", 0),
    ("#cdcdd1", 0),
    ("#a7a9ad", 10),
]

mascara_letras_calle = np.zeros(mascara_calles.shape, dtype=bool)

for hex_color, tolerance in colors:
    rgb_color = np.array([
        int(hex_color[1:3], 16),
        int(hex_color[3:5], 16),
        int(hex_color[5:7], 16)
    ])

    diff = np.abs(img_rgb.astype(int) - rgb_color)

    current_mask = (
        (diff[:, :, 0] <= tolerance) &
        (diff[:, :, 1] <= tolerance) &
        (diff[:, :, 2] <= tolerance)
    )

    mascara_letras_calle = mascara_letras_calle | current_mask

# combinar las mascaras que realizamos
mask = mascara_calles | mascara_letras_calle
mask = mask.astype(np.uint8) * 255

# limpiar y conectar
kernel = np.ones((3, 3), np.uint8)

mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
mask = cv2.dilate(mask, kernel, iterations=1)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)


# --------------------------------------------------
# FUNCIONES PARA CONSTRUIR EL GRAFO Y APLICAR PRIM
# --------------------------------------------------

def calcular_distancia(v1, v2):
    y1, x1 = v1
    y2, x2 = v2

    dy = y2 - y1
    dx = x2 - x1

    distancia = np.sqrt((dy ** 2) + (dx ** 2))

    return distancia


def obtener_puntos_linea(y1, x1, y2, x2):
    puntos = []

    dy = abs(y2 - y1)
    dx = abs(x2 - x1)

    paso_y = 1 if y1 < y2 else -1
    paso_x = 1 if x1 < x2 else -1

    error = dx - dy

    y = y1
    x = x1

    while True:
        puntos.append((y, x))

        if y == y2 and x == x2:
            break

        error_doble = 2 * error

        if error_doble > -dy:
            error = error - dy
            x = x + paso_x

        if error_doble < dx:
            error = error + dx
            y = y + paso_y

    return puntos


def vertices_conectados(mask, v1, v2):
    y1, x1 = v1
    y2, x2 = v2

    puntos = obtener_puntos_linea(y1, x1, y2, x2)

    for y, x in puntos:
        if y < 0 or y >= mask.shape[0]:
            return False

        if x < 0 or x >= mask.shape[1]:
            return False

        if mask[y, x] == 0:
            return False

    return True


def construir_aristas(vertices, mask):
    aristas = []

    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):

            v1 = vertices[i]
            v2 = vertices[j]

            if vertices_conectados(mask, v1, v2):
                costo = calcular_distancia(v1, v2)
                aristas.append((i, j, costo))

    aristas = sorted(aristas, key=lambda arista: arista[2])

    return aristas


def prim(vertices, aristas):
    visitados = [0]
    arbol_expansion_minima = []
    costo_total = 0

    while len(visitados) < len(vertices):
        arista_encontrada = False

        for arista in aristas:
            origen, destino, costo = arista

            origen_visitado = origen in visitados
            destino_visitado = destino in visitados

            if origen_visitado and not destino_visitado:
                arbol_expansion_minima.append(arista)
                visitados.append(destino)
                costo_total = costo_total + costo
                arista_encontrada = True
                break

            elif destino_visitado and not origen_visitado:
                arbol_expansion_minima.append(arista)
                visitados.append(origen)
                costo_total = costo_total + costo
                arista_encontrada = True
                break

        if not arista_encontrada:
            print("No se pudo conectar todos los vertices.")
            break

    return arbol_expansion_minima, costo_total


def revisar_conexion(mask, vertices, a, b):
    y1, x1 = vertices[a]
    y2, x2 = vertices[b]

    puntos = obtener_puntos_linea(y1, x1, y2, x2)

    negros = 0
    blancos = 0

    for y, x in puntos:
        if mask[y, x] == 255:
            blancos = blancos + 1
        else:
            negros = negros + 1

    print("Conexion", a, "-", b)
    print("Pixeles blancos:", blancos)
    print("Pixeles negros:", negros)


# --------------------------------------------------
# CONSTRUIR GRAFO Y OBTENER ARBOL DE EXPANSION MINIMA
# --------------------------------------------------

aristas = construir_aristas(vertices, mask)
arbol_expansion_minima, costo_total = prim(vertices, aristas)

print("Lista de aristas ordenadas de menor a mayor:")
for arista in aristas:
    origen, destino, costo = arista
    print(origen, "-", destino, "costo:", round(costo, 2))

print("\nArbol de expansion minima:")
for arista in arbol_expansion_minima:
    origen, destino, costo = arista
    print(origen, "-", destino, "costo:", round(costo, 2))

print("\nCosto total:", round(costo_total, 2))


# --------------------------------------------------
# MOSTRAR MAPA ORIGINAL CON VERTICES Y MASCARA CON VERTICES
# --------------------------------------------------

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(img_rgb)
plt.scatter(vertices[:, 1], vertices[:, 0], s=35)
plt.title("Original Map with Vertices")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(mask, cmap="gray")
plt.scatter(vertices[:, 1], vertices[:, 0], s=35)
plt.title("Road Mask with Vertices")
plt.axis("off")

plt.show()


# --------------------------------------------------
# MOSTRAR ARBOL DE EXPANSION MINIMA EN EL MAPA ORIGINAL
# --------------------------------------------------

plt.figure(figsize=(8, 8))
plt.imshow(img_rgb)

color_arbol = "red"

for arista in arbol_expansion_minima:
    origen, destino, costo = arista

    y1, x1 = vertices[origen]
    y2, x2 = vertices[destino]

    plt.plot([x1, x2], [y1, y2], linewidth=2, color=color_arbol)

plt.scatter(vertices[:, 1], vertices[:, 0], s=35, color=color_arbol)

for i in range(len(vertices)):
    y, x = vertices[i]
    plt.text(x + 3, y + 3, str(i), fontsize=8, color=color_arbol)

plt.title("Minimum Spanning Tree - Prim")
plt.axis("off")
plt.show()

cv2.imwrite("mask_roads.png", mask)