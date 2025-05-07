from tkinter import *
from tkinter import ttk

#ventanas a utilizar (5 ventanas + main)
from movimientos import view_movs
from empleados import view_emp
from productos import view_prod
from proveedores import view_prov
from comisiones import view_com

window = Tk()
window.geometry("1280x720")

style = ttk.Style()
style.theme_use('default')

#cambi el diseño de las tabs
style.configure('TNotebook.Tab', padding=[10, 10], font=('Arial', 15))

notebook = ttk.Notebook(window)

menu = Frame(notebook)
movimientos = view_movs(notebook)
empleados = view_emp(notebook)
productos = view_prod(notebook)
proveedores = view_prov(notebook)
comisiones = view_com(notebook)

notebook.add(menu, text="Menu principal")
notebook.add(movimientos, text="Movimientos")
notebook.add(empleados, text="Empleados")
notebook.add(productos, text="Productos")
notebook.add(proveedores, text="Proveedores")
notebook.add(comisiones, text="Comisiones")
notebook.pack(expand=True, fill=BOTH)

#Elementos del menu principal
titulo = Label(menu, text="Menu principal RAJTIR - MICRAS", 
               font=('Comic Sans MS', 30, 'bold'), 
               background="#ff5757",
               padx=20, pady=10)
titulo.pack(side=TOP)

area_img = Label(menu, text="*LOGO DE LA TIENDA*", font=('', 35, 'bold'), relief=FLAT, bd=150)
area_img.pack()

window.mainloop()