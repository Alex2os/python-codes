
import matplotlib.pyplot as plt
import numpy as np

# funcion original
def f(x):
    return ( 5*np.sin(x)**5 ) + ( 3*x**4 ) + ( 10*np.cos(x)**3 ) + ( 5*x**2 ) + x + 30
    
# primera derivada
def fPrima(x):
    return ( 12*x**3 ) + ( 10*x ) + ( 25*np.sin(x)**4 * np.cos(x) ) - ( 30*np.cos(x)**2 * np.sin(x) ) + 1

# segunda derivada
def fDoblePrima(x):
    return ( 100*np.sin(x)**3*np.cos(x)**2 ) - ( 25*np.sin(x)**5 ) + ( 36*x**2 ) + ( 60*np.cos(x)*np.sin(x)**2 ) - ( 30*np.cos(x)**3 ) + 10
    
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
