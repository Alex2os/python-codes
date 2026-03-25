import cv2 as cv2

# cargamos el identificador de cara
cascPath = "a.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

# se carga la imagen que se va a usar para el filtro (lentes)
lentesNegros=cv2.imread("lentes_negros_borde_pequeño.png",cv2.IMREAD_UNCHANGED)

#obtener acceso a la webcam
video_capture = cv2.VideoCapture(1)

if not video_capture.isOpened():
        print('No se pudo acceder a la camara')
else:
    while True:

        #revisar si ya puedo leer imagenes de la camara
        ret, frame = video_capture.read()

        frame=cv2.flip(frame,1)

        imagenGrises = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        faces = faceCascade.detectMultiScale(
            imagenGrises,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        # se ajusta el color en bgr para que pueda funcionar con la imagen de lentesNegros
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

        # for para poner los lentes en el frame
        for (x, y, w, h) in faces:

            # le hacemos resize a lentesNegros y lo guardamos en una copia para que no pierda calidad-
            # cuando le estamos haciendo tantos resizes.
            lentesNegrosCopia = cv2.resize(lentesNegros,(w+20, h+20))

            # ponemos los lentes negros en el frame
            for i in range(lentesNegrosCopia.shape[0]):
                 for j in range(lentesNegrosCopia.shape[1]):
                      if(lentesNegrosCopia[i,j][3] != 0):
                           # se ajusta la posicion en el frame para los lentes
                           # y = filas, x = columna
                           frame[i + y-40, j + x-40] = lentesNegrosCopia[i,j]


        # Mostrar la deteccion
        cv2.imshow('Video', frame)
        #se motraran las caras mientra no presionemos la tecla q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    #liberar la camara
    video_capture.release()
    #cerrar todas las ventanas
    cv2.destroyAllWindows()


