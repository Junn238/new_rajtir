from tkinter import *
from tkinter import ttk

#funciones para realizar cosas
def agregarEmp(root):
    def mostrar_datos(base, top):
        print(f"Nombre: {addName.get()}\nEdad: {addEdad.get()}\nTelefono: {addTel.get()}\nCorreo: {addMail.get()}\nTurno: {addTurno.get()}")
        base.destroy()
        window = Toplevel(top)
        Label(window, text="Los datos han sido agregados correctamente").pack(side=TOP)
        Button(window, text="Confirmar", command=lambda: window.destroy()).pack(side=BOTTOM)

    window = Toplevel(root)
    window.geometry("640x360")
    nombre = Label(window, text="Nombre: ").grid(row=0, column=0)
    addName = Entry(window)
    addName.grid(row=0, column=1)

    edad = Label(window, text="Edad: ").grid(row=1, column=0)
    addEdad = Entry(window)
    addEdad.grid(row=1, column=1)

    Telefono = Label(window, text="Telefono: ").grid(row=2, column=0)
    addTel = Entry(window)
    addTel.grid(row=2, column=1)

    Correo = Label(window, text="Correo: ").grid(row=3, column=0)
    addMail = Entry(window)
    addMail.grid(row=3, column=1)

    Turno = Label(window, text="Turno: ").grid(row=4, column=0)
    addTurno = ttk.Combobox(window, state="readonly")
    addTurno['values'] = ['Mañana', 'Tarde', 'Noche']
    addTurno.grid(row=4, column=1)

    completar = Button(window, text="Añadir",   #siempre agregar lambda al command de un elemento ?? 
                       command=lambda: mostrar_datos(window, root))
    completar.grid(row=5, column=0, columnspan=2)

#funcion principal
def view_emp(root):
    empleados = Frame(root)
    
    add_emp = Button(empleados, text=("Agregar empleado"), command=lambda: agregarEmp(empleados)).pack()

    return empleados