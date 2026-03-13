import cv2 as cv2
import numpy as np

imagenMar=cv2.imread('mar.jpg')

minBGR = np.array([130, 150, 120]) # BGR
maxBGR = np.array([190, 190, 190]) # muy blanco

camera = cv2.VideoCapture(1)

while (True):
    
    ret, frame = camera.read()

    if not ret:
        print("Error leyendo la cámara")
        break
    
    # imprimir el tamaño y altura del arreglo de la camara
    # print(frame.shape)
    
    # checamos cada pixel de frame con los intervalos de antes especificados
    maskBGR = cv2.inRange(frame,minBGR,maxBGR)
    
    # le hacemos un bitwise a la mascara anterior (la invertimos)
    mask_inv = cv2.bitwise_not(maskBGR)
    
    # sacamos la parte de la imagen que tiene pixeles blancos (en este caso sería la persona u objeto)
    resultBGR = cv2.bitwise_and(frame, frame, mask = mask_inv)
    
    # extraemos la imagen del mar y usamos la máscara original, poniendo el fondo en esa parte
    result_inv = cv2.bitwise_and(imagenMar, imagenMar, mask = maskBGR)
    
    # por ultimo lo añadimos a frame, que es lo que mostraremos en pantalla para la parte extraida y el fondo
    frame=cv2.add(resultBGR,result_inv)
    
    # finalmente mostramos el frame resultante
    cv2.imshow("camara", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # cerrar el programa
        break
 
camera.release()
cv2.destroyAllWindows()

