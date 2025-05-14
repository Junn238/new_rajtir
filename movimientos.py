from tkinter import *
from tkinter import ttk, messagebox
from mysqlconn import *
import datetime

cursor = init_conn()

def view_movs(root):
    movimientos = Frame(root, bg="#d9d9d9")
    movimientos.pack(fill="both", expand=True)

    carrito = []

    def actualizar_total():
        total = sum(item["subtotal"] for item in carrito)
        total_label.config(text=f"Total: ${total:.2f}")
        return total

    def actualizar_empleados():
        cursor.execute("SELECT Nom_emp FROM empleado")
        empleados = [row[0] for row in cursor.fetchall()]
        empleado_cb['values'] = empleados
        if empleados:
            empleado_cb.set(empleados[0])

    def actualizar_productos():
        cursor.execute("SELECT Nom_pro FROM producto")
        productos = [row[0] for row in cursor.fetchall()]
        producto_cb['values'] = productos
        if productos:
            producto_cb.set(productos[0])

    def agregar_producto_a_carrito():
        try:
            nombre = producto_cb.get()
            cantidad = int(cantidad_entry.get())
            cursor.execute("SELECT Id_pro, Val_pro, Can_pro FROM producto WHERE Nom_pro = %s", (nombre,))
            result = cursor.fetchone()
            if result:
                prod_id, precio, stock = result
                if cantidad > stock:
                    messagebox.showwarning("Stock insuficiente", f"Solo hay {stock} unidades disponibles.")
                    return
                subtotal = cantidad * float(precio)
                carrito.append({
                    "id": prod_id,
                    "nombre": nombre,
                    "cantidad": cantidad,
                    "precio": precio,
                    "subtotal": subtotal
                })
                carrito_tree.insert("", END, values=(prod_id, nombre, cantidad, f"${subtotal:.2f}"))
                actualizar_total()
                cantidad_entry.delete(0, END)
            else:
                messagebox.showerror("Error", "Producto no encontrado.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_producto_carrito():
        selected_item = carrito_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selecciona un producto", "Debes seleccionar un producto para eliminar.")
            return
        index = carrito_tree.index(selected_item[0])
        carrito_tree.delete(selected_item)
        del carrito[index]
        actualizar_total()

    def calcular_faltante_sobrante():
        total = actualizar_total()
        try:
            pago = float(pago_entry.get())
        except ValueError:
            messagebox.showwarning("Pago inválido", "Introduce un número válido.")
            return
        if tipo_mov.get() == "Movimiento":
            cambio = max(0, pago - total)
            cam_label.config(text=f"Cambio: ${cambio:.2f}")
            fal_label.config(text="")
        else:
            falta = max(0, total - pago)
            fal_label.config(text=f"Faltante: ${falta:.2f}")
            cam_label.config(text="")

    def guardar_movimiento():
        try:
            tipo = tipo_mov.get()
            cliente_nombre = cliente_entry.get().strip() if tipo == "Apartado" else "NA"
            empleado = empleado_cb.get()
            pago = float(pago_entry.get())
            total_carrito = float(actualizar_total())
            fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            fecha_fin = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")

            cliente_id = None
            if tipo == "Apartado":
                if not cliente_nombre:
                    messagebox.showerror("Error", "Debes ingresar un nombre de cliente para un apartado.")
                    return
                cursor.execute("SELECT Id_cli FROM cliente WHERE Nom_cli = %s", (cliente_nombre,))
                result = cursor.fetchone()
                if result:
                    cliente_id = result[0]
                else:
                    cursor.execute("INSERT INTO cliente (Nom_cli, Tip_cli) VALUES (%s, %s)", (cliente_nombre, "Apartado"))
                    conexion.commit()
                    cliente_id = cursor.lastrowid
            else:
                cursor.execute("SELECT Id_cli FROM cliente WHERE Nom_cli = %s", ("NA",))
                result = cursor.fetchone()
                if result:
                    cliente_id = result[0]
                else:
                    cursor.execute("INSERT INTO cliente (Nom_cli, Tip_cli) VALUES (%s, %s)", ("NA", "Normal"))
                    conexion.commit()
                    cliente_id = cursor.lastrowid

            for item in carrito:
                if tipo == "Apartado":
                    cursor.execute("""
                        SELECT Id_mov, Pag_mov, Fal_mov, Tot_mov
                        FROM movimiento
                        WHERE Cliente_Id = %s AND Id_pr = %s AND Fal_mov > 0
                        ORDER BY Id_mov DESC LIMIT 1
                    """, (cliente_id, item["id"]))
                    mov = cursor.fetchone()
                    if mov:
                        mov_id, pago_anterior, falta_anterior, total_anterior = mov
                        nuevo_pago = pago_anterior + pago
                        nuevo_falta = max(0, total_anterior - nuevo_pago)
                        nuevo_cambio = max(0, nuevo_pago - total_anterior)
                        cursor.execute("""
                            UPDATE movimiento
                            SET Pag_mov = %s, Cam_mov = %s, Fal_mov = %s
                            WHERE Id_mov = %s
                        """, (nuevo_pago, nuevo_cambio, nuevo_falta, mov_id))
                    else:
                        subtotal = float(item["subtotal"])
                        cambio = max(0, pago - subtotal)
                        falta = max(0, subtotal - pago)
                        cursor.execute("""
                            INSERT INTO movimiento (Cliente_Id, Id_pr, Pag_mov, Cam_mov, Fal_mov, Fec_mov, Fin_mov, Tot_mov)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, (cliente_id, item["id"], pago, cambio, falta, fecha_actual, fecha_fin, subtotal))
                else:
                    cambio = max(0, pago - item["subtotal"])
                    falta = max(0, item["subtotal"] - pago)
                    cursor.execute("""
                        INSERT INTO movimiento (Cliente_Id, Id_pr, Pag_mov, Cam_mov, Fal_mov, Fec_mov, Fin_mov, Tot_mov)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (cliente_id, item["id"], pago, cambio, falta, fecha_actual, fecha_fin, float(item["subtotal"])))

                cursor.execute("""
                    UPDATE producto
                    SET Can_pro = Can_pro - %s
                    WHERE Id_pro = %s AND Can_pro >= %s
                """, (item["cantidad"], item["id"], item["cantidad"]))

            conexion.commit()
            messagebox.showinfo("Éxito", "Movimiento(s) guardado(s) correctamente.")
            carrito.clear()
            carrito_tree.delete(*carrito_tree.get_children())
            actualizar_total()
            ver_movs()
        except Exception as e:
            messagebox.showerror("Error al guardar", str(e))

    def ver_movs():
        tree.delete(*tree.get_children())
        try:
            cursor.execute("""
                SELECT m.Id_mov, c.Nom_cli, p.Nom_pro, m.Pag_mov, m.Cam_mov, m.Fal_mov, m.Fec_mov, m.Fin_mov, m.Tot_mov
                FROM movimiento m
                JOIN cliente c ON m.Cliente_Id = c.Id_cli
                JOIN producto p ON m.Id_pr = p.Id_pro
                ORDER BY m.Id_mov DESC
            """)
            for row in cursor.fetchall():
                tree.insert("", END, values=row)
        except Exception as e:
            messagebox.showerror("Error al cargar movimientos", str(e))

    def abonar_a_apartado():
        pago = 0
        nombre = cliente_entry.get().strip()
        if not nombre:
            messagebox.showerror("Error", "Ingresa el nombre del cliente.")
            return
        try:
            pago = float(pago_entry.get())
            cursor.execute("SELECT Id_cli FROM cliente WHERE Nom_cli = %s", (nombre,))
            cli = cursor.fetchone()
            if not cli:
                messagebox.showerror("Error", "Cliente no encontrado.")
                return

            cliente_id = cli[0]

            cursor.execute("""
                SELECT Id_mov, Pag_mov, Fal_mov, Tot_mov
                FROM movimiento
                WHERE Cliente_Id = %s AND Fal_mov > 0
                ORDER BY Id_mov DESC LIMIT 1
            """, (cliente_id,))
            mov = cursor.fetchone()

            if not mov:
                messagebox.showinfo("Info", "No hay apartados pendientes.")
                return

            mov_id = mov[0]
            pago_anterior = float(mov[1]) 
            falta_anterior = float(mov[2]) 
            total = float(mov[3])
            nuevo_pago = pago_anterior + pago
            nuevo_falta = max(0, (total - nuevo_pago))
            
            nuevo_cambio = max(0, (nuevo_pago - total))

            cursor.execute("""
                UPDATE movimiento
                SET Pag_mov = %s, Cam_mov = %s, Fal_mov = %s
                WHERE Id_mov = %s
            """, (nuevo_pago, nuevo_cambio, nuevo_falta, mov_id))
            conexion.commit()
            messagebox.showinfo("Éxito", "Abono registrado.")
            ver_movs()
        except:
            messagebox.showerror("Error", "Pago inválido.")
            return

        

    def toggle_cliente_entry(*args):
        if tipo_mov.get() == "Apartado":
            cliente_entry.config(state=NORMAL)
            cliente_entry.delete(0, END)
        else:
            cliente_entry.delete(0, END)
            cliente_entry.insert(0, "NA")
            cliente_entry.config(state=DISABLED)

    tipo_mov = StringVar(value="Movimiento")
    tipo_mov.trace("w", toggle_cliente_entry)

    form = Frame(movimientos, bg="#d9d9d9")
    form.pack(padx=10, pady=10, anchor=W)

    Label(form, text="Tipo:", bg="#d9d9d9").grid(row=0, column=0, sticky=W)
    Radiobutton(form, text="Movimiento", variable=tipo_mov, value="Movimiento", bg="#d9d9d9").grid(row=0, column=1)
    Radiobutton(form, text="Apartado", variable=tipo_mov, value="Apartado", bg="#d9d9d9").grid(row=0, column=2)

    Label(form, text="Cliente:", bg="#d9d9d9").grid(row=1, column=0, sticky=W)
    cliente_entry = Entry(form, width=40)
    cliente_entry.grid(row=1, column=1, columnspan=2, sticky=W)

    Label(form, text="Empleado:", bg="#d9d9d9").grid(row=2, column=0, sticky=W)
    empleado_cb = ttk.Combobox(form, width=37)
    empleado_cb.grid(row=2, column=1, columnspan=2, sticky=W)
    actualizar_empleados()

    Label(form, text="Producto:", bg="#d9d9d9").grid(row=3, column=0, sticky=W)
    producto_cb = ttk.Combobox(form, width=30)
    producto_cb.grid(row=3, column=1, sticky=W)
    actualizar_productos()

    Button(form, text="Actualizar productos", command=actualizar_productos).grid(row=3, column=2, sticky=W)

    Label(form, text="Cantidad:", bg="#d9d9d9").grid(row=3, column=3, sticky=W)
    cantidad_entry = Entry(form, width=10)
    cantidad_entry.grid(row=3, column=4, sticky=W)

    Button(form, text="Agregar al carrito", command=agregar_producto_a_carrito).grid(row=4, column=1, pady=5, sticky=W)
    Button(form, text="Eliminar del carrito", command=eliminar_producto_carrito).grid(row=4, column=2, pady=5, sticky=W)

    carrito_frame = Frame(movimientos, bg="#d9d9d9")
    carrito_frame.pack(padx=10, pady=10)

    carrito_cols = ("ID", "Nombre", "Cantidad", "Subtotal")
    carrito_tree = ttk.Treeview(carrito_frame, columns=carrito_cols, show="headings", height=6)
    for col in carrito_cols:
        carrito_tree.heading(col, text=col)
        carrito_tree.column(col, anchor=W, width=100)
    carrito_tree.pack()

    pago_frame = Frame(movimientos, bg="#d9d9d9")
    pago_frame.pack(padx=10, pady=5, anchor=W)

    total_label = Label(pago_frame, text="Total: $0.00", bg="#d9d9d9", font=("Arial", 10, "bold"))
    total_label.grid(row=0, column=0, padx=5)

    Label(pago_frame, text="Pago:", bg="#d9d9d9").grid(row=1, column=0, sticky=W)
    pago_entry = Entry(pago_frame, width=10)
    pago_entry.grid(row=1, column=1, sticky=W)

    Button(pago_frame, text="Calcular", command=calcular_faltante_sobrante).grid(row=1, column=2, padx=10)

    cam_label = Label(pago_frame, text="", bg="#d9d9d9", fg="green")
    cam_label.grid(row=2, column=0, columnspan=2, sticky=W)

    fal_label = Label(pago_frame, text="", bg="#d9d9d9", fg="red")
    fal_label.grid(row=3, column=0, columnspan=2, sticky=W)

    Button(pago_frame, text="Guardar Movimiento", command=guardar_movimiento).grid(row=4, column=0, columnspan=2, pady=10)
    Button(pago_frame, text="Abonar a apartado", command=abonar_a_apartado).grid(row=4, column=2, pady=10)

    tabla_frame = Frame(movimientos, bg="#d9d9d9")
    tabla_frame.pack(padx=10, pady=10)

    cols = ("ID", "Cliente", "Producto", "Pagado", "Cambio", "Falta", "Fecha Inicio", "Fecha Fin", "Total")
    tree = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=6)
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, width=100, anchor=W)
    tree.pack(side=LEFT, fill=X, expand=True)

    scrollbar = Scrollbar(tabla_frame, orient=VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)

    ver_movs()
    toggle_cliente_entry()

    return movimientos
