# definimos las librerias que vamos a usar en el environment

import pandas as pd # dataframes
import numpy as np # manejo de arreglos numericos
import matplotlib.pyplot as ptl # visualizacion o ploteo
from sklearn.linear_model import LinearRegression # regresion lienar
from sklearn.model_selection import train_test_split # reparticion de los datos


# definimos el dataframe conteniendo los datos originales que vamos a usar en el código
data =pd.DataFrame({"experiencia":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
                     "salario":[12,14,17,19,22,25,27,30,32,35,42,44,46,48,51,55]})

# mostramos los datos en una gráfica
data.plot(kind="scatter", x="experiencia", y="salario", color= "blue")
ptl.grid()
ptl.show()

# convertimos el dataframe previamente definido a columnas individuales (x, y)
x = data.iloc[:,0].values.reshape(-1,1)
y = data.iloc[:,1].values.reshape(-1,1)

# obtenemos los datos de prueba/aprendizaje para Y, X.
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

# declaramos nuestro modelo de aprendizaje
model = LinearRegression()

# entrenamos el modelo con los datos de entrenamiento
model.fit(x_train, y_train)

# realizamos y declaramos la predicción dados valores de prueba
prediction = model.predict(x_test)

# tenemos la gráfica para los datos de entrenamiento y de prueba.

# graficamos los datos de entrenamiento de color verde
ptl.scatter(x_train, y_train, color="green", label="Entrenamiento")

# graficamos los datos de prueba con color azul
ptl.scatter(x_test, y_test, color="blue", label="Prueba")

# añadimos labels para identificar
ptl.xlabel("Experiencia")
ptl.ylabel("Salario")
ptl.legend()

ptl.grid()
ptl.show()

# graficamos los datos de entrenamiento de color verde
ptl.scatter(x_train, y_train, color="green", label="Entrenamiento")

# graficamos los datos de prueba con color azul
ptl.scatter(x_test, y_test, color="blue", label="Prueba")

# graficamos la recta obtenida como prediccion
ptl.plot(x_test, prediction, color="red", label = "Recta")

ptl.legend()

# añadimos labels para identificar
ptl.xlabel("Experiencia")
ptl.ylabel("Salario")

# mostramos el grafico
ptl.grid()
ptl.show()

print()

# graficamos los datos de entrenamiento de color verde
ptl.scatter(x_train, y_train, color="green", label="Entrenamiento")

# graficamos los datos de prueba con color azul
ptl.scatter(x_test, y_test, color="blue", label="Prueba")

# graficamos la recta obtenida como prediccion (ahora como puntos individuales)
ptl.scatter(x_test, prediction, color="red", label = "Salario predicho")

ptl.legend()

# añadimos labels para identificar
ptl.xlabel("Experiencia")
ptl.ylabel("Salario")

# mostramos el grafico
ptl.grid()
ptl.show()

# mostramos una tabla de un dataframe que contiene el salario (valor real) y la experiencia, además de la predicción que hizo el modelo

data_resultados = pd.DataFrame({
    "salario-real": y_test.flatten(),
    "experiencia": x_test.flatten(),
    "salario-predicho": prediction.flatten()
})

# mostramos el dataframe/tabla
print(data_resultados)
print("-----------------------------------")

# sacamos la pendiente y la interseccion generadas por el modelo
pendiente = model.coef_[0][0]
interseccion = model.intercept_[0]

# imprimimos en pantalla
print("pendiente:", pendiente)
print("intersección:", interseccion)
