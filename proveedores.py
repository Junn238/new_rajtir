from tkinter import *
from tkinter import ttk, messagebox
from mysqlconn import *

cursor = init_conn()

def view_prov(parent):
    def agregar_proveedor():
        ho = ho_entry.get()
        nom = nom_entry.get()
        ubi = ubi_entry.get()
        mar = mar_entry.get()

        try:
            cursor.execute(
                "INSERT INTO proveedor (Ho_prov, Nom_prov, Ubi_pro, Mar_prov) VALUES (%s, %s, %s, %s)",
                (ho, nom, ubi, mar))
            conexion.commit()
            messagebox.showinfo("Éxito", "Proveedor agregado correctamente")
            limpiar_campos()
            ver_proveedores()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def modificar_proveedor():
        idp = id_entry.get()
        ho = ho_entry.get()
        nom = nom_entry.get()
        ubi = ubi_entry.get()
        mar = mar_entry.get()

        try:
            cursor.execute(
                "UPDATE proveedor SET Ho_prov=%s, Nom_prov=%s, Ubi_pro=%s, Mar_prov=%s WHERE Id_prov=%s",
                (ho, nom, ubi, mar, idp))
            conexion.commit()
            messagebox.showinfo("Éxito", "Proveedor modificado correctamente")
            limpiar_campos()
            ver_proveedores()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_proveedor():
        idp = id_entry.get()
        try:
            cursor.execute("DELETE FROM proveedor WHERE Id_prov=%s", (idp,))
            conexion.commit()
            messagebox.showinfo("Éxito", "Proveedor eliminado correctamente")
            limpiar_campos()
            ver_proveedores()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ver_proveedores():
        cursor.execute("SELECT * FROM proveedor")
        rows = cursor.fetchall()
        for row in tree.get_children():
            tree.delete(row)
        for row in rows:
            tree.insert("", END, values=row)

    def limpiar_campos():
        id_entry.delete(0,  END)
        ho_entry.delete(0,  END)
        nom_entry.delete(0, END)
        ubi_entry.delete(0, END)
        mar_entry.delete(0, END)

    # Frame principal
    frame = ttk.Frame(parent, padding=10)
    frame.pack(fill="both", expand=True)

    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(7, weight=1)

    # Campos
    campos = [
        ("ID Proveedor (solo para modificar/eliminar):", "id_entry"),
        ("Horario", "ho_entry"),
        ("Nombre", "nom_entry"),
        ("Ubicación", "ubi_entry"),
        ("Marca", "mar_entry")
    ]

    entry_widgets = {}
    for i, (label, name) in enumerate(campos):
        ttk.Label(frame, text=label).grid(row=i, column=0, sticky="e", pady=2, padx=5)
        entry = ttk.Entry(frame)
        entry.grid(row=i, column=1, sticky="ew", pady=2, padx=5)
        entry_widgets[name] = entry

    id_entry = entry_widgets["id_entry"]
    ho_entry = entry_widgets["ho_entry"]
    nom_entry = entry_widgets["nom_entry"]
    ubi_entry = entry_widgets["ubi_entry"]
    mar_entry = entry_widgets["mar_entry"]

    # Botones
    btn_frame = ttk.Frame(frame)
    btn_frame.grid(row=5, column=0, columnspan=2, pady=10)

    ttk.Button(btn_frame, text="Agregar", command=agregar_proveedor).grid(row=0, column=0, padx=5)
    ttk.Button(btn_frame, text="Modificar", command=modificar_proveedor).grid(row=0, column=1, padx=5)
    ttk.Button(btn_frame, text="Eliminar", command=eliminar_proveedor).grid(row=0, column=2, padx=5)
    ttk.Button(btn_frame, text="Ver Proveedores", command=ver_proveedores).grid(row=0, column=3, padx=5)

    # Tabla
    tree = ttk.Treeview(frame, columns=("ID", "Horario", "Nombre", "Ubicación", "Marca"), show="headings")
    tree.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=10)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=6, column=2, sticky="ns")

    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    ver_proveedores()
    return frame
