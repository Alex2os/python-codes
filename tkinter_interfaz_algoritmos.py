from tkinter import *
import re

class aplicacion():
    def __init__(self):
        # info general de la clase
        self.raiz = Tk()
        self.raiz.geometry("600x400")
        self.raiz.resizable(width=False, height=False)
        self.raiz.title("Expresiones regulares")
        
        # label hasta arriba
        label = Label(self.raiz,text="Validación de expresiones regulares")
        label.pack(side=TOP)
        
        self.textos=Frame(self.raiz)
        self.textos.pack(side=TOP)
        self.frameDeAbajo=Frame(self.raiz)
        self.frameDeAbajo.pack(side=BOTTOM)
        
        # campos de texto
        self.t1=Entry(self.textos, width=40)
        self.t1.grid(row=0,column=0, padx=10, pady=10)
        
        self.t2=Entry(self.textos, width=40)
        self.t2.grid(row=1,column=0)
        
        self.t3=Entry(self.textos, width=40)
        self.t3.grid(row=2,column=0)
        
        self.t4=Entry(self.textos, width=40)
        self.t4.grid(row=3,column=0)
        
        # botones
        self.b1 = Button(self.textos, text = "validar", command = lambda:self.validar(1))
        self.b1.grid(row=0, column=1, padx=10, pady=10)
        
        self.b2 = Button(self.textos, text = "validar", command = lambda:self.validar(2))
        self.b2.grid(row=1, column=1, padx=10, pady=10)
        
        self.b3 = Button(self.textos, text = "validar", command = lambda:self.validar(3))
        self.b3.grid(row=2, column=1, padx=10, pady=10)
        
        self.b4 = Button(self.textos, text = "validar", command = lambda:self.validar(4))
        self.b4.grid(row=3, column=1, padx=10, pady=10)
        
        # label de los botones
        self.l1 = Label(self.textos, text = "...")
        self.l1.grid(row = 0, column = "2")
        
        self.l2 = Label(self.textos, text = "...")
        self.l2.grid(row = 1, column = "2")
        
        self.l3 = Label(self.textos, text = "...")
        self.l3.grid(row = 2, column = "2")
        
        self.l4 = Label(self.textos, text = "...")
        self.l4.grid(row = 3, column = "2")
        
        self.bsalir = Button(self.frameDeAbajo, text = "Salir", command = self.raiz.destroy)
        self.bsalir.pack(side = LEFT)
        self.blimpiar = Button(self.frameDeAbajo, text = "Limpiar", command = self.limpiar)
        self.blimpiar.pack(side = LEFT)
        
        self.raiz.mainloop()
        
    def limpiar(self):
        self.t1.delete(first = 0, last = "end")
        self.l1.config(fg="black", text = "...")

    def validar(self, numero):
        if(numero == 1):
            txtAValidar = self.t1.get()
            x=re.search("^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$", txtAValidar)
            
            if(x):
                self.l1.config(fg="green", text = "IPv4 valida")
            else:
                self.l1.config(fg="red", text = "IPv4 invalida")
        
        
        
# creamos una instancia de la clase para que tengamos la ventana
app=aplicacion()