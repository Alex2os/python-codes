# importacion de las librerias

import pandas as pd # dataframes
import numpy as np # manejo de arreglos numericos
import matplotlib.pyplot as ptl # visualizacion o ploteo
from sklearn.linear_model import LinearRegression # regresion lienar
from sklearn.model_selection import train_test_split # reparticion de los datos
from mpl_toolkits.mplot3d import Axes3D # graficas en 3D para los datos
from sklearn.metrics import mean_squared_error, r2_score, root_mean_squared_error # calcular los errores de la regresion

# definimos el dataframe conteniendo los datos originales que vamos a usar en el código
data = pd.DataFrame({"horas-estudio": [5, 20, 5, 15, 10, 8, 12, 18, 6, 14, 9, 16, 7, 11, 13, 4, 17, 19, 3, 10, 6, 14, 8, 12, 15, 7, 9, 11, 13, 16],
                     "tareas-realizadas": [8, 2, 9, 11, 10, 7, 10, 3, 8, 12, 9, 5, 6, 11, 8, 10, 4, 1, 12, 7, 9, 6, 8, 10, 5, 11, 7, 9, 12, 4],
                     "calificacion-real": [10, 30, 20, 25, 15, 18, 22, 28, 12, 24, 17, 26, 14, 23, 21, 8, 27, 32, 6, 19, 13, 25, 16, 20, 29, 15, 18, 12, 24, 31]
                     })

# se muestran los datos en una grafica 3D
fig = ptl.figure(figsize=(7, 7))

ax = fig.add_subplot(111, projection='3d')
ax.scatter(data["horas-estudio"],
           data["tareas-realizadas"],
           data["calificacion-real"],
           color = "red")

ptl.show()

# se convierte el dataframe previamente definido a columnas individuales
x = data.loc[:,'horas-estudio':'tareas-realizadas'].values.reshape(-1,2)
y = data.iloc[:,2].values.reshape(-1,1)

# obtenemos los datos de prueba/aprendizaje para Y, X. asignamos un 30% para prueba y el otro queda como 70% para entrenamiento
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)

# declaramos nuestro modelo de aprendizaje
model = LinearRegression()

# entrenamos el modelo con los datos de entrenamiento
model.fit(x_train, y_train)

# realizamos y declaramos la predicción dados valores de prueba
prediction = model.predict(x_test)

# grafico para los datos de prueba
fig = ptl.figure(figsize=(7, 7))
ax = fig.add_subplot(111, projection='3d')

# le damos un titulo, y los labels correspondientes
title = ax.set_title("Datos de prueba")
xlabel = ax.set_xlabel("Horas de estudio")
ylabel = ax.set_ylabel("Tareas")
zlabel = ax.set_zlabel("Calificación")

# asignamos los datos de x_test y y_test. x_test contiene las dos variables independientes, por lo que usamos esto para las dos primeras coordenadas.
ax.scatter(x_test[:,0],
           x_test[:,1],
           y_test,
           color = "red")

ptl.show()
# -------------------------------------------
# figura para los datos de entrenamiento

fig = ptl.figure(figsize=(7, 7))
ax = fig.add_subplot(111, projection='3d')

# titulo y labels
title = ax.set_title("Datos de entrenamiento")
xlabel = ax.set_xlabel("Horas de estudio")
ylabel = ax.set_ylabel("Tareas")
zlabel = ax.set_zlabel("Calificación")

# asignamos los datos de x_train y y_train correspondientes
ax.scatter(x_train[:,0],
           x_train[:,1],
           y_train,
           color = "blue")

ptl.show()
# -------------------------------------------
# figura para datos de prueba y entrenamiento

fig = ptl.figure(figsize=(7, 7))
ax = fig.add_subplot(111, projection='3d')

# titulo y labels
title = ax.set_title("Datos de entrenamiento y prueba")
xlabel = ax.set_xlabel("Horas de estudio")
ylabel = ax.set_ylabel("Tareas")
zlabel = ax.set_zlabel("Calificación")

# asignamos los datos de x_train y y_train
ax.scatter(x_train[:,0],
           x_train[:,1],
           y_train,
           color = "blue")

# asignamos los datos de x_test y y_test
ax.scatter(x_test[:,0],
           x_test[:,1],
           y_test,
           color = "red")

ptl.show()

# grafica mostrando el plano con los datos calculados

# definimos los limites del plano, en este caso usando los valores de las variables independientes
# los valores son sacados de los minimos y los maximos respectivamente de cada columna, y asignamos un valor al final de "50" muestras, que-
# seran regresadas por la funcion a traves del intervalo que hemos indicado, en este caso para las columnas
x_range = np.linspace(x[:,0].min(), x[:,0].max(), 50)
y_range = np.linspace(x[:,1].min(), x[:,1].max(), 50)

# despues realizamos y convertimos los valores que definimos anteriormente a una meshgrid. esto lo usaremos para calcular y modelar el plano en las lineas que siguen
x_grid, y_grid = np.meshgrid(x_range, y_range)

# lo que hacemos ahora es convertir los valores de y_grid y x_grid a una lista para poder enviarselos a nuestro modelo y poder predecir valores para z_grid
grid_points = np.c_[x_grid.ravel(), y_grid.ravel()]
z_grid = model.predict(grid_points)

# una vez prediciendolos, convertimos los valores de z_grid al mismo formato que x_grid (basicamente igual al de x_grid y y_grid)
z_grid = z_grid.reshape(x_grid.shape)

# por ultimo podemos crear la grafica para mostrar los datos que calculamos y el plano
fig = ptl.figure(figsize=(7, 7))
ax = fig.add_subplot(111, projection='3d')

# datos de prueba
ax.scatter(
    x_test[:,0],
    x_test[:,1],
    y_test,
    color='red',
)

# plano del modelo, ajustandolo para que se vea un poco transparente
ax.plot_surface(
    x_grid, # usamos x_grid
    y_grid, # y_grid
    z_grid, # y z_grid, que fue el que predijimos en el modelo
    alpha=0.4,
    color = "blue"
)

# poner el titulo y los labels respectivamente
ax.set_title("Gráfica con el plano ajustado al modelo (datos de prueba)")
ax.set_xlabel("Horas de estudio")
ax.set_ylabel("Tareas")
ax.set_zlabel("Calificación")

ptl.show()
#---------------------------------------------

# grafica con plano con los datos de entrenamiento
fig = ptl.figure(figsize=(7, 7))
ax = fig.add_subplot(111, projection='3d')

# datos de entrenamiento
ax.scatter(
    x_train[:,0],
    x_train[:,1],
    y_train,
    color='green',
)

# plano del modelo, ajustandolo para que se vea un poco transparente
ax.plot_surface(
    x_grid, # usamos x_grid
    y_grid, # y_grid
    z_grid, # y z_grid, que fue el que predijimos en el modelo
    alpha=0.4,
    color = "blue"
)

# poner el titulo y los labels respectivamente
ax.set_title("Gráfica con el plano ajustado al modelo (datos de entrenamiento)")
ax.set_xlabel("Horas de estudio")
ax.set_ylabel("Tareas")
ax.set_zlabel("Calificación")

ptl.show()
#---------------------------------------------
# grafica con plano con los datos de prueba y entrenamiento
fig = ptl.figure(figsize=(7, 7))
ax = fig.add_subplot(111, projection='3d')

# datos de entrenamiento
ax.scatter(
    x_train[:,0],
    x_train[:,1],
    y_train,
    color='green',
)

# datos de prueba
ax.scatter(
    x_test[:,0],
    x_test[:,1],
    y_test,
    color='red',
)

# plano del modelo, ajustandolo para que se vea un poco transparente
ax.plot_surface(
    x_grid, # usamos x_grid
    y_grid, # y_grid
    z_grid, # y z_grid, que fue el que predijimos en el modelo
    alpha=0.4,
    color = "blue"
)

# poner el titulo y los labels respectivamente
ax.set_title("Gráfica con el plano ajustado al modelo (datos de entrenamiento y prueba)")
ax.set_xlabel("Horas de estudio")
ax.set_ylabel("Tareas")
ax.set_zlabel("Calificación")

ptl.show()

# mostramos una tabla de un dataframe que contriene e la calificacion-real, calificaion-predicha, horas de estudio y tareas entregadas
data_resultados = pd.DataFrame({"horas-estudio":x_test[:,0].flatten(),"tareas-realizadas":x_test[:,1].flatten(),"calificacion-real":y_test.flatten(),"prediccion":prediction.flatten(),
"diferencia": y_test.flatten()-prediction.flatten()})

# mostramos el dataframe conteniendo la informacion
print(data_resultados)
print("-----------------------------------")

# sacamos la pendiente y la interseccion generadas por el modelo
peso_estudio = model.coef_[0][0]
peso_tareas = model.coef_[0][1]
intercepto = model.intercept_[0]

# imprimimos en pantalla los datos acerca del modelo
print("Intercepto (Theta 0):", intercepto)
print("Peso de estudio (Theta 1):", peso_estudio)
print("Peso de tareas (Theta 2):", peso_tareas)
print("mean_squared_error",mean_squared_error(y_test, prediction))
print("r2_scorer",r2_score(y_test, prediction))
print("root_mean_squared_error",root_mean_squared_error(y_test, prediction))
print()
print(f"Ecuación del modelo: y = {intercepto} + {peso_estudio}x1 + {peso_tareas}x2")
