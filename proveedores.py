from tkinter import *
from tkinter import ttk

def view_prov(root):
    proveedores = Frame(root)

    text = Label(proveedores, text="prueba hola")
    text.pack()

    return proveedores