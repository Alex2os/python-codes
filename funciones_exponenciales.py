import matplotlib.pyplot as plt
import numpy as np

# funcion original
def f(x):
    return (
        4*x**5 - 7*x**4 +
        3*x**3 + 6*x**2 - 
        2*x + 9
        )
    
# primera derivada
def fPrima(x):
    return (
        20*x**4 - 28*x**3 + 
        9*x**2 + 12*x - 2
        )

# segunda derivada
def fDoblePrima(x):
    return (
        80*x**3 - 84*x**2 + 
        18*x + 12
        )

# variable para el intervalo (valores que va a tomar x para obtener el eje y)
t = np.arange(-1, 1, 0.03)

# grafica para todas las funciones juntas

plt.figure()

plt.plot(t, f(t), "mv-", t, fPrima(t), "bo-", t, fDoblePrima(t), "gp-")

plt.xlabel("Eje de las x")
plt.ylabel("Eje de las y")

plt.title("Graficas de todas las funciones")

plt.grid()
plt.show()

# grafica de la funcion original
plt.figure()

plt.plot(t, f(t), "mv-")

plt.xlabel("Eje de las x")
plt.ylabel("Eje de las y")

plt.title("Función normal")

plt.grid()
plt.show()

# grafica de la primera derivada
plt.figure()

plt.plot(t, fPrima(t), 'bo-')

plt.xlabel("Eje de las x")
plt.ylabel("Eje de las y")

plt.title("Primera derivada")

plt.grid()
plt.show()

# grafica de la segunda derivada
plt.figure()

plt.plot(t, fDoblePrima(t), 'gp-')

plt.xlabel("Eje de las x")
plt.ylabel("Eje de las y")

plt.title("Segunda derivada")

plt.grid()
plt.show()