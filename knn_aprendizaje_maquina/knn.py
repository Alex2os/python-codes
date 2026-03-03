
import numpy as np
import pandas as pd # librería para el dataframe
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split # librería para dividir los datos 
from collections import Counter # libreria para contar la mayoria de clases posteriormente en la funcion de prediccion de clases.
import os

os.system('clear') # limpiar la pantalla cada vez que se corre el programa (solo para cuando se corre en otro ambiente)

# declaramos la funcion para obtener la distancia manhattan, que estamos usando en este caso.
# a esta funcion se le envian los valores de X_train y X_test, respectivamente
# como dichos valores son arreglos (conteniendo los atributos del .csv), entonces podemos restarlos entre ellos, sacando su valor absoluto y sumatoria a la vez
# para lo anterior usamos numpy, con np.sum y np.abs para sacar la formula y distancia de manhattan dado una tupla
# se manda primero la tupla a predecir y despues la de entrenamiento.
def distancia_manhattan(x1, x2):
    return np.sum(np.abs(x1 - x2))

# la funcion para predecir los valores de x_test. en este caso enviamos x_test, x_train y y_train (este ultimo para definir la clase de cada x_train) y por ultimo el valor_k que usaremos.
def predecir_valores(x_test, x_train, y_train, valor_k):
    print("Prediciendo para k =", valor_k)
    
    predicciones = []
    
    # hacemos un for para calcular la distancia entre la tupla que queremos predecir en x_test
    for tupla_test in x_test:
        
        distancias_totales = []
        
        i = 0
        
        # tenemos otro for para que en cada tupla_test se realice el calculo con todas las ditancias de x_train.
        for tupla_train in x_train:
            
            distancia = distancia_manhattan(tupla_test, tupla_train)
            
            distancias_totales.append([distancia, y_train[i]])
            
            i = i + 1 # usamos i para meter el valor de la clase a distancias_totales, usandose para el index.
        
        # despues de sacar los valores de las distancias, podemos trabajar para predecir una clase por mayoria usando el valor de k.
        
        # primero podemos ordenar las distancias totales por valor (de mas pequeño a mayor) para asi obtener los valores mas pequeños al inicio
        distancias_totales = sorted(distancias_totales)
        
        # despues sacamos los valores mas pequeños de acuerdo al valor k
        distancias_totales = distancias_totales[:valor_k] # cortamos hasta el valor k, dependiendo de este es el tamaño final del arreglo en cada iteracion de cada tupla en test.
        
        # imprimimos las distancias totales.
        print(distancias_totales)
        print("---------")
        
        # para la siguiente parte tenemos que encontrar la mayoria de clases que se encuentran en las distancias mas cortas.
        # para lo anterior, tenemos que sacar primero las clases para luego obtener la mayoria, usando la siguiente linea de codigo:
        clases = [clase for _, clase in distancias_totales] # obtenemos el segundo valor de distancias_totales, ignorando el primero con (_), por lo que en clases se guardan todas las clases de las distancias mas cortas.
        
        # despues podemos usar la libreria de Counter para devolver el valor mas comun y asi asignarlo a clase mayoria, y asi predecir la clase con exito.
        clase_mayoria = Counter(clases).most_common(1)[0][0]
        
        # imprimimos la clase predicha
        print("Clase predicha para la tupla:", clase_mayoria)
        print(("---------"))
        
        # por ultimo añadimos la prediccion a la variable de predicciones.
        predicciones.append([tupla_test, clase_mayoria])
        
    return predicciones

# empieza el programa
# importamos y creamos nuestro dataframe conteniendo los datos, en este caso especificando que es IRIS_PLANT.csv.
iris_dataframe = pd.read_csv("IRIS_PLANT.csv")

# podemos crear una scatter matrix para poder visualizar de manera correcta los 4 atributos distintos que tenemos en cada tupla.
pd.plotting.scatter_matrix(
    iris_dataframe.iloc[:, 0:4],
    figsize=(10,10)
)

# mostramos el grafico
plt.show()

X = iris_dataframe.iloc[:, :-1].values   # sacamos los atributos del .csv para asignarlos a X
Y = iris_dataframe.iloc[:, -1].values    # y ponemos que Y es igual a la clase a la que pertenece la tupla.

# obtenemos los datos de entrenamiento y de prueba a través de la función de sklearn train_test_split.
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

# calculamos predicciones para todos los valores de k
prediccion_k1 = predecir_valores(X_test, X_train, Y_train, 1)
dataframe_k1 = pd.DataFrame(prediccion_k1)

prediccion_k3 = predecir_valores(X_test, X_train, Y_train, 3)
dataframe_k3 = pd.DataFrame(prediccion_k3)

prediccion_k5 = predecir_valores(X_test, X_train, Y_train, 5)
dataframe_k5 = pd.DataFrame(prediccion_k5)


print("Dataframe de k = 1", dataframe_k1)
print("Dataframe de k = 3", dataframe_k3)
print("Dataframe de k = 5", dataframe_k5)




    