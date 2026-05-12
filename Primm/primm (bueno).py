import cv2
import numpy as np
import matplotlib.pyplot as plt

# cargamos la imagen del mapa y el archivo .npy de dicho mapa

Mapa = "mapaChiquito.png"
Vertices = "verticeChiquito.npy"

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

# funcion para saber si dos vertices o nodos se pueden conectar
# lo que se hace en este caso es que en vez de checar posiciones entre los nodos, se checa toda la linea posible desde un nodo a-
# otro. lo anterior se hace ya que hay problemas si solo se checan ciertos puntos, por lo que mejor es usar un algoritmo para-
# poder checar la linea completa

# usamos linspace, lo cual hace que sea bastante facil obtener una linea recta entre dos puntos, y simplemente podemos ir-
# iterando e ir checando cada punto para estar seguros de que todos los puntos y la linea es correcta para poder conectar-
# dos nodos
def VerticesConectados(mascara, x1, x2):
    # el orden de estas variables importa bastante. tiene que ser como estan
    vertice_y1, vertice_x1 = x1
    vertice_y2, vertice_x2 = x2
    
    puntos_linea = 0
    
    # sacamos el numero de puntos maximo entre los dos vertices, esto para que con linspace tengamos este numero de puntos para-
    # iterar
    # como no se puede usar la funcion max(), se saca manualmente esta parte
    diferencia_y = abs(vertice_y2 - vertice_y1) + 1
    diferencia_x = abs(vertice_x2 - vertice_x1) + 1

    if diferencia_y > diferencia_x:
        puntos_linea = diferencia_y
    else:
        puntos_linea = diferencia_x
    
    # usamos linspace para generar dichos puntos a traves de los dos vertices, usando la variable de pasos 
    linea_x = np.linspace(vertice_x1, vertice_x2, puntos_linea, dtype=int)
    linea_y = np.linspace(vertice_y1, vertice_y2, puntos_linea, dtype=int)
    
    # despues podemos iterar a traves de los puntos y checar las condiciones para decidir si devolver false o true.
    for punto_x, punto_y in zip(linea_x, linea_y):
        
        # si el punto que estamos checando se sale del limite devolvemos false, o si es que es igual al tamaño de la mascara.shape-
        # respectivamente para tanto x como para y
        if(punto_x < 0 or punto_x >= mascara.shape[1]):
            return False
        
        if(punto_y < 0 or punto_y >= mascara.shape[0]):
            return False
        
        # si el punto de la mascara es cero (negro) se devuelve falso
        if mascara[punto_y, punto_x] == 0:
            return False
        
    # devolvemos true si pasa todos los puntos de control
    return True

# podemos usar una funcion tambien para crear las conexiones validas, como se vio en el algoritmo de primm.
# basicamente se hacen las conexiones entre los nodos o vertices con su costo o peso correspondiente
# de esta manera el algoritmo de primm mas tarde puede usar estos valores para funcionar apropiadamente

# recibimos la mascara y los vertices, para primero comprobar si es una conexion valida y luego para sacar la distancia euclidiana-
# si es que se pueden conectar. devuelve la lista completa de aristas en este caso, con peso y la conexion entre vertices.
def CrearAristas(mascara, vertices):
    
    # lista para devolver todos los aristas una vez armados del mapa y vertices actuales
    aristas = []
    
    # basicamente revisamos si dos vertices ([i] y [j]) se pueden conectar de forma correcta a traves de la funcion de VerticesConectados
    # despues de ello, si es que se puede se saca la distancia euclidiana y se añade la conexion a los aristas.
    # se repite hasta que no queden vertices en la lista de vertices que se envia
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):

            if VerticesConectados(mascara, vertices[i], vertices[j]):
                costo = DistanciaEuclidiana(vertices[i], vertices[j])
                aristas.append((costo, i, j))
    
    # ordenamos los vertices por peso, usando sort y especificando el index 0 [0] que es donde se contienen los pesos
    aristas.sort(key=lambda x: x[0])
    
    return aristas

# por ultimo podemos definir la funcion de primm para realizar el arbol de expansion minima.
# en este caso se le envian los vertices y las aristas previamente definidas. lo que se devuelve en este caso es el arbol de-
# expansion minima
def Primm(vertices, aristas):
    
    # arreglo para guardar el arbol resultante
    arbol_expansion_minima = []
    # vertices visitados hasta el momento
    vertices_visitados = [0] # inicializamos la variable para que no haya problemas en la iteracion
    
    # usamos el tamaño de los arreglos para la condicion de parar
    # si ya se visitaron todos los nodos, entonces se detiene el while
    while len(vertices_visitados) < len(vertices):
        
        vertice_agregado = False
        
        # sacamos todo lo que necesitamos de las aristas. en este caso es el costo y los dos vertices o nodos que se conectan
        
        # basicamente como ya tenemos las aristas ordenadas por el costo de menor a mayor, es por esto que se mete el primer-
        # vertice cada iteracion y se le hace break con los ifs, ademas de actualizar las variables de costo, arbol de expansion-
        # y los vertices visitados.
        for costo, x1, x2 in aristas:
        
            # si x1 ya esta dentro y x2 no
            if(x1 in vertices_visitados and x2 not in vertices_visitados):
                arbol_expansion_minima.append([costo, x1, x2])
                vertices_visitados.append(x2)
                vertice_agregado = True
                break
            
            # si x2 ya esta dentro y x1 no
            if(x2 in vertices_visitados and x1 not in vertices_visitados):
                arbol_expansion_minima.append([costo, x1, x2])
                vertices_visitados.append(x1)
                vertice_agregado = True
                break
            
        # si por alguna razon no se pudo conectar un vertice, se le hace break al while y regresa la lista como esta.
        if(not vertice_agregado):
            break 
    
    return arbol_expansion_minima
    
        
            
            
            
            
        
    
    
    
        
        
        
        
        
    
    
    
    
    



