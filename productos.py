from tkinter import *
from tkinter import ttk, messagebox
from mysqlconn import *

cursor = init_conn()

# Diccionario para proveedores
proveedor_dict = {}

def actualizar_proveedores():
    """Recarga los proveedores desde la BD y actualiza el combobox."""
    global proveedor_dict
    cursor.execute("SELECT Id_prov, Nom_prov FROM proveedor")
    proveedores = cursor.fetchall()
    proveedor_dict = {nombre: id_ for id_, nombre in proveedores}
    proveedor_combo['values'] = list(proveedor_dict.keys())

def agregar_producto():
    nom = nom_entry.get()
    val = val_entry.get()
    mar = mar_entry.get()
    can = can_entry.get()
    des = des_entry.get()
    proveedor_nombre = proveedor_combo.get()
    id_prov = proveedor_dict.get(proveedor_nombre)

    try:
        if id_prov is None:
            raise ValueError("Selecciona un proveedor válido.")
        cursor.execute(
            "INSERT INTO producto (Nom_pro, Val_pro, Mar_pro, Can_pro, Des_pro, Id_prov) VALUES (%s, %s, %s, %s, %s, %s)",
            (nom, val, mar, can, des, id_prov))
        conexion.commit()
        messagebox.showinfo("Éxito", "Producto agregado correctamente")
        limpiar_campos()
        ver_productos()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def modificar_producto():
    idp = id_entry.get()
    nom = nom_entry.get()
    val = val_entry.get()
    mar = mar_entry.get()
    can = can_entry.get()
    des = des_entry.get()
    proveedor_nombre = proveedor_combo.get()
    id_prov = proveedor_dict.get(proveedor_nombre)

    try:
        if not idp:
            raise ValueError("Proporcione el ID del producto a modificar.")
        if id_prov is None:
            raise ValueError("Selecciona un proveedor válido.")
        cursor.execute(
            "UPDATE producto SET Nom_pro=%s, Val_pro=%s, Mar_pro=%s, Can_pro=%s, Des_pro=%s, Id_prov=%s WHERE Id_pro=%s",
            (nom, val, mar, can, des, id_prov, idp))
        conexion.commit()
        messagebox.showinfo("Éxito", "Producto modificado correctamente")
        limpiar_campos()
        ver_productos()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def eliminar_producto():
    idp = id_entry.get()

    try:
        if not idp:
            raise ValueError("Proporcione el ID del producto a eliminar.")
        cursor.execute("DELETE FROM producto WHERE Id_pro=%s", (idp,))
        conexion.commit()
        messagebox.showinfo("Éxito", "Producto eliminado correctamente")
        limpiar_campos()
        ver_productos()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def ver_productos():
    actualizar_proveedores()
    cursor.execute("""
        SELECT p.Id_pro, p.Nom_pro, p.Val_pro, p.Mar_pro, p.Can_pro, p.Des_pro, pr.Nom_prov
        FROM producto p
        LEFT JOIN proveedor pr ON p.Id_prov = pr.Id_prov
    """)
    rows = cursor.fetchall()
    for row in tree.get_children():
        tree.delete(row)
    for row in rows:
        tree.insert("", END, values=row)

def limpiar_campos():
    id_entry.delete(0,  END)
    nom_entry.delete(0, END)
    val_entry.delete(0, END)
    mar_entry.delete(0, END)
    can_entry.delete(0, END)
    des_entry.delete(0, END)
    proveedor_combo.set('')

# FUNCION PARA INTEGRAR ESTA PESTAÑA EN main.py
def view_prod(parent):
    frame = ttk.Frame(parent, padding=10)
    
    # Campos de entrada
    campos = [
        ("ID Producto (solo para modificar/eliminar):", "id_entry"),
        ("Nombre", "nom_entry"),
        ("Valor", "val_entry"),
        ("Marca", "mar_entry"),
        ("Cantidad", "can_entry"),
        ("Descripción", "des_entry")
    ]

    entry_widgets = {}
    for i, (label_text, var_name) in enumerate(campos):
        ttk.Label(frame, text=label_text).grid(row=i, column=0, sticky="e", pady=2, padx=5)
        entry = ttk.Entry(frame)
        entry.grid(row=i, column=1, sticky="ew", pady=2, padx=5)
        entry_widgets[var_name] = entry

    global id_entry, nom_entry, val_entry, mar_entry, can_entry, des_entry
    id_entry = entry_widgets["id_entry"]
    nom_entry = entry_widgets["nom_entry"]
    val_entry = entry_widgets["val_entry"]
    mar_entry = entry_widgets["mar_entry"]
    can_entry = entry_widgets["can_entry"]
    des_entry = entry_widgets["des_entry"]

    # Combobox para proveedor
    ttk.Label(frame, text="Proveedor").grid(row=6, column=0, sticky="e", pady=2, padx=5)
    global proveedor_combo
    proveedor_combo = ttk.Combobox(frame, state="readonly", width=38)
    proveedor_combo.grid(row=6, column=1, sticky="w", pady=2, padx=5)
    actualizar_proveedores()

    # Botones
    btn_frame = ttk.Frame(frame)
    btn_frame.grid(row=7, column=0, columnspan=2, pady=10)

    ttk.Button(btn_frame, text="Agregar", command=agregar_producto).grid(row=0, column=0, padx=5)
    ttk.Button(btn_frame, text="Modificar", command=modificar_producto).grid(row=0, column=1, padx=5)
    ttk.Button(btn_frame, text="Eliminar", command=eliminar_producto).grid(row=0, column=2, padx=5)
    ttk.Button(btn_frame, text="Ver Productos", command=ver_productos).grid(row=0, column=3, padx=5)

    # Frame contenedor de la tabla y scrollbar
    table_frame = ttk.Frame(frame)
    table_frame.grid(row=8, column=0, columnspan=3, sticky="nsew", padx=6, pady=5)

    # Tabla
    global tree
    tree = ttk.Treeview(table_frame, columns=("ID", "Nombre", "Valor", "Marca", "Cantidad", "Descripción", "Proveedor"), show="headings")
    tree.pack(side="left", fill="both", expand=True)

    # Scrollbar vertical
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    # Configurar encabezados y columnas
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", stretch=True)

    # Permitir expansión dinámica del contenido
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(2, weight=0)  # Scrollbar no se expande
    frame.rowconfigure(8, weight=1)


    ver_productos()

    return frame
