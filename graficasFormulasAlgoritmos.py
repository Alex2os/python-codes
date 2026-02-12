import matplotlib.pyplot as plt
import numpy as np

# algoritmo: decimalBinario1
def algoritmo1Funcion(n):
    return 14 * np.log2(n) + 13

# algoritmo: decimalBinario2
def algoritmo2Funcion(n):
    return 14 * np.log2(n) + 15

# algoritmo: decimalBinario3
def algoritmo3Funcion(n):
    return 10 * np.log2(n) + 8

# variable para el intervalo (valores que va a tomar x para obtener el eje y)
t = np.arange(-100, 100, 1)

# grafica para todos los algoritmos juntos

plt.figure()

plt.plot(t, algoritmo1Funcion(t), "mv-", t, algoritmo2Funcion(t), "bo-", t, algoritmo3Funcion(t), "gp-")

plt.xlabel("Eje de las x")
plt.ylabel("Eje de las y")

plt.title("Graficas de todas las funciones")

plt.grid()
plt.show()

# grafica de decimalBinario1
plt.figure()

plt.plot(t, algoritmo1Funcion(t), "mv-")

plt.xlabel("Eje de las x")
plt.ylabel("Eje de las y")

plt.title("decimalBinario1")

plt.grid()
plt.show()

# grafica de decimalBinario2
plt.figure()

plt.plot(t, algoritmo2Funcion(t), 'bo-')

plt.xlabel("Eje de las x")
plt.ylabel("Eje de las y")

plt.title("decimalBinario2")

plt.grid()
plt.show()

# grafica de decimalBinario3
plt.figure()

plt.plot(t, algoritmo3Funcion(t), 'gp-')

plt.xlabel("Eje de las x")
plt.ylabel("Eje de las y")

plt.title("decimalBinario3")

plt.grid()
plt.show()