from tkinter import *
from tkinter import ttk, messagebox
from mysqlconn import *

#funciones para realizar cosas
cursor = init_conn()

def view_emp(parent):
    def agregar_empleado():
        nom = nom_entry.get()
        ed = ed_entry.get()
        tel = tel_entry.get()
        em = em_entry.get()
        tie = tie_entry.get()
        tur = tur_entry.get()
        try:
            cursor.execute("INSERT INTO empleado (Nom_emp, Ed_emp, Tel_emp, Em_emp, Tie_emp, Tur_emp) VALUES (%s, %s, %s, %s, %s, %s)",
                           (nom, ed, tel, em, tie, tur))
            conexion.commit()
            messagebox.showinfo("Éxito", "Empleado agregado correctamente")
            ver_empleados()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def modificar_empleado():
        id = id_entry.get()
        nom = nom_entry.get()
        ed = ed_entry.get()
        tel = tel_entry.get()
        em = em_entry.get()
        tie = tie_entry.get()
        tur = tur_entry.get()
        try:
            cursor.execute("""UPDATE empleado SET Nom_emp=%s, Ed_emp=%s, Tel_emp=%s, Em_emp=%s, Tie_emp=%s, Tur_emp=%s WHERE Id_emp=%s""",
                           (nom, ed, tel, em, tie, tur, id))
            conexion.commit()
            messagebox.showinfo("Éxito", "Empleado modificado correctamente")
            ver_empleados()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_empleado():
        id = id_entry.get()
        try:
            cursor.execute("DELETE FROM empleado WHERE Id_emp=%s", (id,))
            conexion.commit()
            messagebox.showinfo("Éxito", "Empleado eliminado correctamente")
            ver_empleados()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ver_empleados():
        for row in tree.get_children():
            tree.delete(row)
        cursor.execute("SELECT * FROM empleado")
        for row in cursor.fetchall():
            tree.insert("", END, values=row)
        id_entry.delete(0,END)
        nom_entry.delete(0, END)
        ed_entry.delete(0, END)
        tel_entry.delete(0, END)
        em_entry.delete(0, END)
        tie_entry.delete(0, END)

    # Contenedor principal
    frame = Frame(parent, bg="#d9d9d9")
    frame.pack(fill="both", expand=True)

    # Frame superior (formulario)
    form_frame = Frame(frame, bg="#d9d9d9")
    form_frame.pack(pady=10)

    Label(form_frame, text="ID Empleado (solo para modificar/eliminar):", bg="#d9d9d9").grid(row=0, column=0, sticky=W)
    id_entry = Entry(form_frame, width=40)
    id_entry.grid(row=0, column=1, padx=5, pady=2)

    Label(form_frame, text="Nombre:", bg="#d9d9d9").grid(row=1, column=0, sticky=W)
    nom_entry = Entry(form_frame, width=40)
    nom_entry.grid(row=1, column=1, padx=5, pady=2)

    Label(form_frame, text="Edad:", bg="#d9d9d9").grid(row=2, column=0, sticky=W)
    ed_entry = Entry(form_frame, width=40)
    ed_entry.grid(row=2, column=1, padx=5, pady=2)

    Label(form_frame, text="Teléfono:", bg="#d9d9d9").grid(row=3, column=0, sticky=W)
    tel_entry = Entry(form_frame, width=40)
    tel_entry.grid(row=3, column=1, padx=5, pady=2)

    Label(form_frame, text="Email:", bg="#d9d9d9").grid(row=4, column=0, sticky=W)
    em_entry = Entry(form_frame, width=40)
    em_entry.grid(row=4, column=1, padx=5, pady=2)

    Label(form_frame, text="Tiempo:", bg="#d9d9d9").grid(row=5, column=0, sticky=W)
    tie_entry = Entry(form_frame, width=40)
    tie_entry.grid(row=5, column=1, padx=5, pady=2)

    Label(form_frame, text="Turno:", bg="#d9d9d9").grid(row=6, column=0, sticky=W)
    tur_entry = ttk.Combobox(form_frame, width=40, state="readonly")
    tur_entry['values'] = ['Mañana', 'Tarde']
    tur_entry.grid(row=6, column=1, padx=5, pady=2)

    # Botones
    btn_frame = Frame(frame, bg="#d9d9d9")
    btn_frame.pack(pady=5)

    Button(btn_frame, text="Agregar", width=12, command=agregar_empleado).grid(row=0, column=0, padx=5)
    Button(btn_frame, text="Modificar", width=12, command=modificar_empleado).grid(row=0, column=1, padx=5)
    Button(btn_frame, text="Eliminar", width=12, command=eliminar_empleado).grid(row=0, column=2, padx=5)
    Button(btn_frame, text="Ver Empleados", width=15, command=ver_empleados).grid(row=0, column=3, padx=5)

    # Tabla con scrollbar
    table_frame = Frame(frame)
    table_frame.pack(padx=10, pady=10, fill=BOTH, expand=True)

    tree = ttk.Treeview(table_frame, columns=("ID", "Nombre", "Edad", "Teléfono", "Email", "Tiempo", "Turno"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Edad", text="Edad")
    tree.heading("Teléfono", text="Teléfono")
    tree.heading("Email", text="Email")
    tree.heading("Tiempo", text="Tiempo")
    tree.heading("Turno", text="Turno")
    tree.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = Scrollbar(table_frame, orient=VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Cargar datos al inicio
    ver_empleados()

    return frame