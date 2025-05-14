from tkinter import *
from tkinter import ttk

# ventanas a utilizar (5 ventanas + main)
from movimientos import view_movs
from empleados import view_emp
from productos import view_prod
from proveedores import view_prov
from comisiones import view_com

# Colores del modo oscuro
DARK_BG = "#2b2b2b"
DARK_FG = "#ffffff"
TAB_BG = "#3c3f41"
ACCENT_COLOR = "#ff5757"

window = Tk()
window.geometry("1280x720")
window.configure(bg=DARK_BG)

# Estilo general oscuro
style = ttk.Style()
style.theme_use('default')

#aqui inicio la imagen/logo de la tienda
logoMICRAS = PhotoImage(file=".\\recursos\\logo_RAJTIR.png")

# Estilo para las pestañas
style.configure('TNotebook',
                background=DARK_BG,
                borderwidth=0)

style.configure('TNotebook.Tab',
                background=TAB_BG,
                foreground=DARK_FG,
                padding=[10, 10],
                font=('Arial', 15))
style.map('TNotebook.Tab',
          background=[("selected", ACCENT_COLOR)],
          foreground=[("selected", DARK_BG)])

# Estilo general para otros elementos ttk
style.configure("TFrame", background=DARK_BG)
style.configure("TLabel", background=DARK_BG, foreground=DARK_FG)

notebook = ttk.Notebook(window)

menu = Frame(notebook, bg=DARK_BG)
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

# Elementos del menú principal
titulo = Label(menu,
               text="Menu principal RAJTIR - MICRAS",
               font=('Comic Sans MS', 30, 'bold'),
               background=ACCENT_COLOR,
               foreground="white",
               padx=20, pady=10)
titulo.pack(side=TOP)

area_img = Label(menu,
                 image=logoMICRAS,
                 font=('', 35, 'bold'),
                 bg=DARK_BG,
                 fg=DARK_FG,
                 relief=FLAT, bd=150)
area_img.pack()

window.mainloop()
