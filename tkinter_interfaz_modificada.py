from tkinter import *
import random # generar numeros aleatorios

class aplicacion():
    def __init__(self):
        # info general de la clase
        self.raiz = Tk()
        self.raiz.geometry("600x400")
        self.raiz.resizable(width=False, height=False)
        self.raiz.title("Cuadros coloridos")
        
        # label hasta arriba
        label = Label(self.raiz,text="Haz click en el botón para generar colores aleatorios")
        label.pack(side=TOP)
        
        self.textos=Frame(self.raiz)
        self.textos.pack(side=TOP)
        self.framePrincipal=Frame(self.raiz)
        self.framePrincipal.pack(side=TOP)
        
        self.botonGenerarColores = Button(self.framePrincipal, text = "Generar", command = self.cambiarColorRandom)
        self.botonGenerarColores.grid(row = 0, column = 0)
        
        self.frameColores = Frame(self.raiz)
        self.frameColores.pack(side=TOP)
        
        self.frameColor1 = Frame(self.frameColores, height = 100, width = 100)
        self.frameColor1.grid(row = 1, column=0)
        
        self.frameColor2 = Frame(self.frameColores, height = 100, width = 100)
        self.frameColor2.grid(row = 1, column=1)
        
        self.frameColor3 = Frame(self.frameColores, height = 100, width = 100)
        self.frameColor3.grid(row = 1, column=2)
        
        self.frameColor4 = Frame(self.frameColores, height = 100, width = 100)
        self.frameColor4.grid(row = 2, column=0)
        
        self.frameColor5 = Frame(self.frameColores, height = 100, width = 100)
        self.frameColor5.grid(row = 2, column=1)
        
        self.frameColor6 = Frame(self.frameColores, height = 100, width = 100)
        self.frameColor6.grid(row = 2, column=2)
        
        self.frameColor7 = Frame(self.frameColores, height = 100, width = 100)
        self.frameColor7.grid(row = 3, column=0)
        
        self.frameColor8 = Frame(self.frameColores, height = 100, width = 100)
        self.frameColor8.grid(row = 3, column=1)
        
        self.frameColor9 = Frame(self.frameColores, height = 100, width = 100)
        self.frameColor9.grid(row = 3, column=2)
        
        
        self.frameDeAbajo = Frame(self.raiz)
        self.frameDeAbajo.pack(side = BOTTOM)
        
        self.bsalir = Button(self.frameDeAbajo, text = "Salir", command = self.raiz.destroy)
        self.bsalir.pack(side = LEFT)

        self.raiz.mainloop()
        
    def cambiarColorRandom(self):
        
        color_fondo = []
        
        for i in range (9):
            numero_aleatorio= random.randint(100000, 999999)
            color_fondo.append("#" + str(numero_aleatorio))
        
        
        self.frameColor1.config(bg = color_fondo[0])
        self.frameColor2.config(bg = color_fondo[1])
        self.frameColor3.config(bg = color_fondo[2])
        self.frameColor4.config(bg = color_fondo[3])
        self.frameColor5.config(bg = color_fondo[4])
        self.frameColor6.config(bg = color_fondo[5])
        self.frameColor7.config(bg = color_fondo[6])
        self.frameColor8.config(bg = color_fondo[7])
        self.frameColor9.config(bg = color_fondo[8])
        
        
# creamos una instancia de la clase para que tengamos la ventana
app=aplicacion()