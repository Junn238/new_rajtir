from tkinter import *
from tkinter import ttk, messagebox
from mysqlconn import init_conn  

DARK_BG = "#2b2b2b"
DARK_FG = "#ffffff"
TABLE_BG = "#3c3f41"
ACCENT_COLOR = "#ff5757"

def registrar_apartado(nombre_cliente, nombre_empleado, total_monto):
    cursor = None
    try:
        cursor = init_conn()

        comision = total_monto * 0.05

        query_comision = """
        INSERT INTO comision (Can_pa, Clie_pa, Empl_pa)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query_comision, (comision, nombre_cliente, nombre_empleado))
        cursor.connection.commit()

        messagebox.showinfo("Comisión Generada", f"Comisión generada: {comision} para el apartado.")

    except Exception as e:
        messagebox.showerror("Error al registrar apartado", f"Hubo un error al registrar el apartado: {str(e)}")
    finally:
        if cursor:
            cursor.close()

def view_com(parent):
    frame = Frame(parent, bg=DARK_BG)

    titulo = Label(frame, text="Comisiones", font=('Arial', 25, 'bold'),
                   bg=ACCENT_COLOR, fg="white", pady=10)
    titulo.pack(fill=X)

    columnas = ("ID", "Cliente", "Empleado", "Pago (5%)")
    tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=20)

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor=CENTER)

    tabla.pack(fill=BOTH, expand=True, padx=20, pady=20)

    def cargar_datos():
        cursor = None
        try:
            tabla.delete(*tabla.get_children())
            cursor = init_conn()

            query = """
            SELECT Id_pa, Clie_pa, Empl_pa, Can_pa FROM comision
            """
            cursor.execute(query)
            datos = cursor.fetchall()

            if not datos:
                messagebox.showinfo("Sin resultados", "No se encontraron comisiones.")
                return

            for fila in datos:
                tabla.insert("", END, values=fila)

        except Exception as e:
            messagebox.showerror("Error al cargar comisiones", f"Hubo un error al cargar las comisiones: {str(e)}")
        finally:
            if cursor:
                cursor.close()

    boton_actualizar = Button(frame, text="Actualizar", command=cargar_datos,
                              bg=ACCENT_COLOR, fg="white", font=("Arial", 12, "bold"))
    boton_actualizar.pack(pady=10)

    cargar_datos()

    return frame
