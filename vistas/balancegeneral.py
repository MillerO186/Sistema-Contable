import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkcalendar import Calendar
from datetime import datetime

class BalanceGeneral(tk.Frame):
    def __init__(self, parent, connection):
        super().__init__(parent)
        self.connection = connection
        self.fecha_seleccionada = tk.StringVar()
        cursor_ultima_fecha = self.connection.cursor()
        cursor_ultima_fecha.execute("SELECT MAX(fecha) FROM libros_diarios")
        maxfecha = cursor_ultima_fecha.fetchone()
        self.fecha_seleccionada.set(maxfecha)
        self.contador_ordenar = 1
        self.pack(expand=True, fill='both')
        self.x = 1
        self.total_categoria = 0
        # Scrollbar para la vista completa
        self.canvas = tk.Canvas(self)
        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        image = Image.open("imagenes_diseño/parte_balance_general.png")
        image = image.resize((200, 35), Image.ANTIALIAS)
        self.foto8 = ImageTk.PhotoImage(image)
        image = Image.open("imagenes_diseño/total_balances.png")
        image = image.resize((200, 35), Image.ANTIALIAS)
        self.foto9 = ImageTk.PhotoImage(image)
        image = Image.open("imagenes_diseño/boton_mostrar_mayores.png")
        image = image.resize((140, 35), Image.ANTIALIAS)
        self.foto11 = ImageTk.PhotoImage(image)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        # Cambiado para que el Canvas y el Scrollbar ocupen tudo el espacio
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar_y.pack(side="right", fill="y")


        frame_titulo_boton = tk.Frame(self.scrollable_frame)
        frame_titulo_boton.grid(row=0, column=0)
        # Título centrado
        tk.Label(frame_titulo_boton, text="Balance General", font=("Rockwell", 16, "bold"), bg="#F7F7F7").grid(row=0,
                                                                                                              column=0)
        # Botón de actualizar
        boton_actualizar = tk.Button(frame_titulo_boton, text="Actualizar",image= self.foto11,borderwidth=0,font=("Rockwell", 12),compound="center",
                                          command=lambda: self.mostrar_balance_general(self.fecha_seleccionada.get()))
        boton_actualizar.grid(row=0, column=1, pady=10)

        boton_elegir_fecha = tk.Button(frame_titulo_boton, text= "Elegir_Fecha", image = self.foto11, borderwidth=0,font=("Rockwell",12),compound="center",
                                       command=self.elegir_fecha_para_tabla)
        boton_elegir_fecha.grid(row=0,column=2,pady=10)
        # Separar las tablas para cada categoría



        self.mostrar_balance_general(self.fecha_seleccionada.get())

    def elegir_fecha_para_tabla(self):
        # Crear una ventana emergente para el calendario
        calendario_window = tk.Toplevel(self)
        calendario_window.title("Seleccionar Fecha")

        # Crear el calendario
        calendario = Calendar(calendario_window, selectmode='day')
        calendario.pack(padx=10, pady=10)

        def cerrar_calendario(calendario):
            fecha = calendario.get_date()
            fecha_formateada = datetime.strptime(fecha, '%m/%d/%y').strftime('%d/%m/%y')
            self.fecha_seleccionada.set(fecha_formateada)
            self.mostrar_balance_general(self.fecha_seleccionada.get())
            calendario_window.destroy()

        # Botón para confirmar la selección de fecha
        tk.Button(calendario_window, text="Seleccionar", command=lambda: cerrar_calendario(calendario)).pack(pady=10)
    def mostrar_balance_general(self,fecha):
        self.x=1
        # Mostrar activos corrientes
        activos_corrientes = [i for i in range(10, 19)] + [i for i in range(20, 30)]
        activos_no_corrientes = [i for i in range(30, 40)]
        pasivos = [i for i in range(40, 50)]
        patrimonio = [i for i in range(50, 53)] + [i for i in range(56, 59)]

        tk.Label(self.scrollable_frame, text="Activos Corrientes", image=self.foto8, font=("Rockwell", 13),
                 compound="center").grid(
            row=self.x, column=0,
            sticky="we")
        self.x = self.x + 1
        self.cargar_categoria(fecha,self.scrollable_frame, activos_corrientes, self.x)
        self.x = self.x + 1

        fram_total_activos_corrientes = tk.Label(self.scrollable_frame)
        fram_total_activos_corrientes.grid(row=self.x, column=0, sticky="we")
        tk.Label(fram_total_activos_corrientes, text="Total Activos Corrientes", image=self.foto9,
                 font=("Rockwell", 13), compound="center").grid(
            row=1, column=0,
            sticky="we")
        total_categoria_var = tk.IntVar(value=self.total_categoria)

        tk.Entry(fram_total_activos_corrientes, textvariable=total_categoria_var, width=22, state="readonly",
                 font=("Rockwell", 12),
                 bd=5, relief="sunken").grid(row=1, column=1, padx=10, pady=10)
        self.x = self.x + 1

        tk.Label(self.scrollable_frame, text="Activos No Corrientes", image=self.foto8, font=("Rockwell", 13),
                 compound="center").grid(
            row=self.x, column=0,
            sticky="we")
        self.x = self.x + 1
        self.cargar_categoria(fecha,self.scrollable_frame, activos_no_corrientes, self.x)
        self.x = self.x + 1

        fram_total_activos_no_corrientes = tk.Label(self.scrollable_frame)
        fram_total_activos_no_corrientes.grid(row=self.x, column=0, sticky="we")
        tk.Label(fram_total_activos_no_corrientes, text="Total Activos No Corrientes", image=self.foto9,
                 font=("Rockwell", 13), compound="center").grid(
            row=1, column=0,
            sticky="we")
        total_categoria_var = tk.IntVar(value=self.total_categoria)

        tk.Entry(fram_total_activos_no_corrientes, textvariable=total_categoria_var, width=22, state="readonly",
                 font=("Rockwell", 12),
                 bd=5, relief="sunken").grid(row=1, column=1, padx=10, pady=10)
        self.x = self.x + 1

        tk.Label(self.scrollable_frame, text="Pasivos", image=self.foto8, font=("Rockwell", 13),
                 compound="center").grid(
            row=self.x, column=0,
            sticky="we")
        self.x = self.x + 1
        self.cargar_categoria(fecha,self.scrollable_frame, pasivos, self.x)
        self.x = self.x + 1

        fram_total_pasivos = tk.Label(self.scrollable_frame)
        fram_total_pasivos.grid(row=self.x, column=0, sticky="we")
        tk.Label(fram_total_pasivos, text="Total Pasivos", image=self.foto9,
                 font=("Rockwell", 13), compound="center").grid(
            row=1, column=0,
            sticky="we")
        total_categoria_var = tk.IntVar(value=self.total_categoria)

        tk.Entry(fram_total_pasivos, textvariable=total_categoria_var, width=22, state="readonly",
                 font=("Rockwell", 12),
                 bd=5, relief="sunken").grid(row=1, column=1, padx=10, pady=10)
        self.x = self.x + 1

        tk.Label(self.scrollable_frame, text="Patrimonio", image=self.foto8, font=("Rockwell", 13),
                 compound="center").grid(
            row=self.x, column=0,
            sticky="we")
        self.x = self.x + 1
        self.cargar_categoria(fecha,self.scrollable_frame, patrimonio, self.x)
        self.x = self.x + 1

        fram_total_patrimonio = tk.Label(self.scrollable_frame)
        fram_total_patrimonio.grid(row=self.x, column=0, sticky="we")
        tk.Label(fram_total_patrimonio, text="Total Patrimonio", image=self.foto9,
                 font=("Rockwell", 13), compound="center").grid(
            row=1, column=0,
            sticky="we")
        total_categoria_var = tk.IntVar(value=self.total_categoria)

        tk.Entry(fram_total_patrimonio, textvariable=total_categoria_var, width=22, state="readonly",
                 font=("Rockwell", 12),
                 bd=5, relief="sunken").grid(row=1, column=1, padx=10, pady=10)
        self.x = self.x + 1



    def cargar_categoria(self, fecha, frame, cuentasreal, x):
        self.total_categoria = 0
        tabla_frame = tk.Frame(frame)
        tabla_frame.grid(row=x,column=0, columnspan=2)
        tabla_in = ttk.Treeview(tabla_frame, columns=("Cuenta", "Saldo"),
                                show="headings")
        tabla_in.heading("Cuenta", text="Cuenta")
        tabla_in.heading("Saldo", text="Saldo")
        tabla_in.grid(row=0, column=0)

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla_in.yview)
        tabla_in.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=2, sticky='ns')

        cuentas = []
        cursor = self.connection.cursor()
        for cuenta in cuentasreal:
            cursor.execute("SELECT id_cuenta, nombre FROM catalogo_cuentas WHERE id_cuenta = %s", (cuenta,))
            cuentas = cuentas + cursor.fetchall()

        conta = 0
        if len(fecha.split("'"))>1:
            print(fecha.split("'"))
            fecha = "07-10-2024"

        for cuenta in cuentas:
            id_cuenta = cuenta[0]
            nombre_cuenta = cuenta[1]
            nombre_formateado = str(id_cuenta) + "-" + str(nombre_cuenta)
            # Obtener totales de los mayores

            cursor.execute("SELECT SUM(debe), SUM(haber) FROM libros_diarios WHERE id_cuenta = %s  AND fecha<=%s", (id_cuenta,fecha, ))
            total_debe, total_haber = cursor.fetchone()

            total_debe = total_debe if total_debe is not None else 0
            total_haber = total_haber if total_haber is not None else 0

            # Determinar el saldo
            saldo_debe = total_debe - total_haber if total_debe > total_haber else 0
            saldo_haber = total_haber - total_debe if total_haber > total_debe else 0
            tabla_in.tag_configure('evenrow', background="#F0F0F0")
            tabla_in.tag_configure('oddrow', background="white")

            # Solo insertar en la tabla si hay saldo

            saldoreal = saldo_debe if saldo_debe > 0 else saldo_haber
            if conta % 2 == 0:
                    tag = 'evenrow'
            else:
                    tag = 'oddrow'
            conta = conta + 1
            self.total_categoria = self.total_categoria  + saldoreal
            tabla_in.insert("", "end", values=(nombre_formateado, saldoreal), tags=tag)
