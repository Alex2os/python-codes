import cv2
import numpy as np
import matplotlib.pyplot as plt

# cargamos la imagen del mapa y el archivo .npy de dicho mapa

Mapa = "mapa1.png"
Vertices = "verticeMapa1.npy"

MapaImagen = cv2.imread(Mapa)
MapaVertices = np.load(Vertices)

# convertimos nuestra imagen de BGR a RGB
# esto nos sirve para la funcion de crear mascara mas adelante.
ImagenRGB = cv2.cvtColor(MapaImagen, cv2.COLOR_BGR2RGB)

# para realizar la mascara de la forma correcta, ponemos los colores que vamos a usar en una lista para poder iterar a traves de ella-
# mas tarde
# los colores para la mascara estan en formato RGB
ColoresMascara = [
    [[255, 255, 255], 4], # tolerancia para las calles es 4, que es el color blanco
    [[133, 141, 147], 0],
    [[197, 201, 217], 0],
    [[197, 197, 201], 0],
    [[197, 201, 205], 0],
    [[196, 200, 216], 0],
    [[120, 124, 128], 0],
    [[121, 125, 129], 0],
    [[205, 205, 209], 0],
    [[167, 169, 173], 10], # tolerancia 10. todos los demas tienen tolerancia cero.
]


def CrearMascara(imagen, colores):
    
    # primero creamos una variable para guardar la mascara
    mascara = np.zeros(imagen.shape[:2], dtype = np.uint8)
    
    # iteramos a traves de los valores en nuestra lista
    for color, tolerancia in colores:
        
        # obtenemos el color y lo transformamos en un arreglo np
        color = np.array(color, dtype = np.int16)
        
        # sacamos los limites para la tolerancia de cada color. cada tupla de color viene con su tolerancia, la cual se saca junto con el for.
        color_lower = np.clip(color - tolerancia, 0, 255).astype(np.uint8)
        color_upper = np.clip(color + tolerancia, 0, 255).astype(np.uint8)
        
        # sacamos la mascara nueva
        mascara_nueva = cv2.inRange(imagen, color_lower, color_upper)
        
        # finalmente podemos actualizar la mascara, poniendola encima de la que ya tenemos.
        mascara = cv2.bitwise_or(mascara_nueva, mascara)
        
    # despues podemos regresar nuestra mascara
    return mascara
        
# creamos nuestra mascara del mapa con los colores y la imagen en rgb
MascaraMapa = CrearMascara(ImagenRGB, ColoresMascara)

# antes de mostrar la mascara o usarla la limpiamos para que se vea bien. en este caso usamos las siguientes funciones:

# creamos un kernel de 3x3 para limpiar la mascara.
kernel = np.ones((3, 3), np.uint8)

# despues le podemos aplica morphologyEx para ayudar a pulir nuestra mascara, usando morph_close para poder cerrar algunas partes negras en la mascara y que sean blancas 
MascaraMapa = cv2.morphologyEx(MascaraMapa, cv2.MORPH_CLOSE, kernel, iterations=2)
# tambien podemos usar dilate para hacer crecer las partes blancas. esto sirve despues para cuando se implemente primm en los nodos y checar si se pueden conectar o no.
MascaraMapa = cv2.dilate(MascaraMapa, kernel, iterations=1)
# le hacemos un morphology de nuevo despues del dilate.
MascaraMapa = cv2.morphologyEx(MascaraMapa, cv2.MORPH_CLOSE, kernel, iterations=1)

# mostramos la mascara y el mapa original
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 2)
plt.imshow(MapaImagen)
plt.title("Mapa original")
plt.axis("off")

plt.subplot(1, 2, 1)
plt.imshow(MascaraMapa, cmap="gray")
plt.title("Máscara del mapa")
plt.axis("off")

plt.show()

# mostramos la mascara y el mapa original pero con los vertices/nodos
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(MascaraMapa, cmap="gray")
plt.scatter(MapaVertices[: ,1], MapaVertices[:,0], s=30)
plt.title("Máscara del mapa (vértices)")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(MapaImagen)
plt.scatter(MapaVertices[: ,1], MapaVertices[:,0], s=30)
plt.title("Mapa original (vértices)")
plt.axis("off")

plt.show()

# ahora podemos empezar con las funciones para realizar el arbol de expansion minima

# funcion para la distancia euclidiana para calcular el costo entre dos vertices/nodos
def DistanciaEuclidiana(x1, x2):
    return np.sqrt(np.sum((x1 - x2)**2))





