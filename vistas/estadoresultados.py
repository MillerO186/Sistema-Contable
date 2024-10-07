import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class EstadoResultados(ttk.Frame):
    def __init__(self, parent, connection):
        super().__init__(parent)
        self.connection = connection
        self.scrollable_frame = None
        self.contador_ordenar = 1
        image = Image.open("imagenes_diseño/concepto_estado.png")
        image = image.resize((200, 35), Image.ANTIALIAS)
        self.verde= ImageTk.PhotoImage(image)
        image = Image.open("imagenes_diseño/concepto_estado_resta.png")
        image = image.resize((200, 35), Image.ANTIALIAS)
        self.rojo = ImageTk.PhotoImage(image)
        image = Image.open("imagenes_diseño/boton_revisar_cuentas.png")
        image = image.resize((150, 35), Image.ANTIALIAS)
        self.revisar = ImageTk.PhotoImage(image)
        image = Image.open("imagenes_diseño/boton_mostrar_mayores.png")
        image = image.resize((140, 35), Image.ANTIALIAS)
        self.foto11 = ImageTk.PhotoImage(image)


        # Crear el canvas y el frame
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        frame_titulo_boton = tk.Frame(self.scrollable_frame)
        frame_titulo_boton.grid(row=0, column=0, columnspan=2)

        # Título centrado
        tk.Label(frame_titulo_boton, text="Estado de Resultados", font=("Rockwell", 16, "bold"), bg="#F7F7F7").grid(
            row=0,
            column=0)
        boton_actualizar = tk.Button(frame_titulo_boton, text="Actualizar", image=self.foto11, borderwidth=0,
                                     font=("Rockwell", 12), compound="center",
                                     command=self.mostrar_estado)
        boton_actualizar.grid(row=0, column=1, columnspan=4, pady=10)

        # Mostrar el estado de resultados inicial
        self.mostrar_estado()
    def mostrar_estado(self):

        triframe= tk.Frame(self.scrollable_frame)
        triframe.grid(row=2, column=0, sticky="nsew")

        tk.Label(triframe, text="Ventas", image=self.verde, compound="center", font=("Rockwell", 12)).grid(
            row=0, column=0, sticky="nsew")
        tk.Label(triframe, text="-Costo de ventas", image=self.rojo, compound="center", font=("Rockwell", 12)).grid(
            row=1, column=0, sticky="nsew")
        tk.Label(triframe, text="Utilidad Bruta", image=self.verde, compound="center", font=("Rockwell", 12)).grid(
            row=2, column=0, sticky="nsew")
        tk.Label(triframe, text="-Gastos Operativos", image=self.rojo, compound="center", font=("Rockwell", 12)).grid(
            row=3, column=0, sticky="nsew")
        tk.Label(triframe, text="Utilidad Operativa", image=self.verde, compound="center", font=("Rockwell", 12)).grid(
            row=4, column=0, sticky="nsew")
        tk.Label(triframe, text="+Otros Ingresos", image=self.verde, compound="center", font=("Rockwell", 12)).grid(
            row=5, column=0, sticky="nsew")
        tk.Label(triframe, text="-Otros Gastos", image=self.rojo, compound="center", font=("Rockwell", 12)).grid(
            row=6, column=0, sticky="nsew")
        tk.Label(triframe, text="Utilidad sin impuestos", image=self.verde, compound="center", font=("Rockwell", 12)).grid(
            row=7, column=0, sticky="nsew")
        tk.Label(triframe, text="-Impuestos", image=self.rojo, compound="center", font=("Rockwell", 12)).grid(
            row=8, column=0, sticky="nsew")
        tk.Label(triframe, text="Utilidad neta", image=self.verde, compound="center",
                 font=("Rockwell", 12)).grid(row=9, column=0, sticky="nsew")
        Ventas = [70]
        Costo_de_ventas = [69]
        Gastos_Operativos = [62,63,68]
        Otros_Ingresos = [75,77]
        Otros_Gastos = [65,66,67]
        Impuestos = [64]
        ventas = tk.IntVar()
        ventas.set(self.total_cat(Ventas))
        costo_de_ventas = tk.IntVar()
        costo_de_ventas.set((self.total_cat(Costo_de_ventas)))
        utilidad_bruta = tk.IntVar()
        utilidad_bruta.set(self.total_cat(Ventas) - self.total_cat(Costo_de_ventas))
        gastos_operativos = tk.IntVar()
        gastos_operativos.set(self.total_cat(Gastos_Operativos))
        utilidad_operativas = tk.IntVar()
        utilidad_operativas.set(self.total_cat(Ventas) - self.total_cat(Costo_de_ventas)-self.total_cat(Gastos_Operativos))
        otros_ingresos = tk.IntVar()
        otros_ingresos.set(self.total_cat(Otros_Ingresos))
        otros_gastos = tk.IntVar()
        otros_gastos.set(self.total_cat(Otros_Gastos))
        utilidad_antes_impuestos = tk.IntVar()
        utilidad_antes_impuestos.set(self.total_cat(Ventas) - self.total_cat(Costo_de_ventas)-self.total_cat(Gastos_Operativos)+self.total_cat(Otros_Ingresos)-self.total_cat(Otros_Gastos))
        impuestos = tk.IntVar()
        impuestos.set(self.total_cat(Impuestos))
        utilidad_neta = tk.IntVar()
        utilidad_neta.set(self.total_cat(Ventas) - self.total_cat(Costo_de_ventas)-self.total_cat(Gastos_Operativos)+self.total_cat(Otros_Ingresos)-self.total_cat(Otros_Gastos)-self.total_cat(Impuestos))

        tk.Entry(triframe, textvariable=ventas, width=22, state="readonly", font=("Rockwell", 12), bd=5, relief="sunken").grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        tk.Entry(triframe, textvariable=costo_de_ventas, width=22, state="readonly", font=("Rockwell", 12), bd=5, relief="sunken").grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        tk.Entry(triframe, textvariable=utilidad_bruta, width=22, state="readonly", font=("Rockwell", 12), bd=5, relief="sunken").grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        tk.Entry(triframe, textvariable=gastos_operativos, width=22, state="readonly", font=("Rockwell", 12), bd=5, relief="sunken").grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
        tk.Entry(triframe, textvariable=utilidad_operativas, width=22, state="readonly", font=("Rockwell", 12), bd=5, relief="sunken").grid(row=4, column=1, padx=10, pady=10, sticky="nsew")
        tk.Entry(triframe, textvariable=otros_ingresos, width=22, state="readonly", font=("Rockwell", 12), bd=5, relief="sunken").grid(row=5, column=1, padx=10, pady=10, sticky="nsew")
        tk.Entry(triframe, textvariable=otros_gastos, width=22, state="readonly", font=("Rockwell", 12), bd=5, relief="sunken").grid(row=6, column=1, padx=10, pady=10, sticky="nsew")
        tk.Entry(triframe, textvariable=utilidad_antes_impuestos, width=22, state="readonly", font=("Rockwell", 12), bd=5, relief="sunken").grid(row=7, column=1, padx=10, pady=10, sticky="nsew")
        tk.Entry(triframe, textvariable=impuestos, width=22, state="readonly", font=("Rockwell", 12), bd=5, relief="sunken").grid(row=8, column=1, padx=10, pady=10, sticky="nsew")
        tk.Entry(triframe, textvariable=utilidad_neta, width=22, state="readonly", font=("Rockwell", 12), bd=5, relief="sunken").grid(row=9, column=1, padx=10, pady=10, sticky="nsew")

        tk.Button(triframe, text="Mostrar Cuentas", image=self.revisar, borderwidth=0, compound="center",
                  font=("Rockwell", 9), command=lambda: self.detalle_categoria(Ventas)).grid(row=0, column=2, columnspan=1, padx=10, pady=10,sticky="nsew")
        tk.Button(triframe, text="Mostrar Cuentas", image=self.revisar, borderwidth=0, compound="center",
                  font=("Rockwell", 9), command=lambda: self.detalle_categoria(Costo_de_ventas)).grid(row=1, column=2,columnspan=1, padx=10,pady=10, sticky="nsew")
        tk.Button(triframe, text="Mostrar Cuentas", image=self.revisar, borderwidth=0, compound="center",
                  font=("Rockwell", 9), command=lambda: self.detalle_categoria(Gastos_Operativos)).grid(row=3, column=2,columnspan=1, padx=10,pady=10, sticky="nsew")
        tk.Button(triframe, text="Mostrar Cuentas", image=self.revisar, borderwidth=0, compound="center",
                  font=("Rockwell", 9), command=lambda: self.detalle_categoria(Otros_Ingresos)).grid(row=5, column=2,columnspan=1, padx=10,pady=10, sticky="nsew")
        tk.Button(triframe, text="Mostrar Cuentas", image=self.revisar, borderwidth=0, compound="center",
                  font=("Rockwell", 9), command=lambda: self.detalle_categoria(Otros_Gastos)).grid(row=6, column=2,columnspan=1, padx=10,pady=10, sticky="nsew")
        tk.Button(triframe, text="Mostrar Cuentas", image=self.revisar, borderwidth=0, compound="center",
                  font=("Rockwell", 9), command=lambda: self.detalle_categoria(Impuestos)).grid(row=8, column=2,columnspan=1, padx=10,pady=10, sticky="nsew")

    def total_cat(self, cuentasreal):
        tot_categoria = 0

        cuentas = []
        cursor = self.connection.cursor()
        for cuenta in cuentasreal:
            cursor.execute("SELECT id_cuenta, nombre FROM catalogo_cuentas WHERE id_cuenta = %s", (cuenta,))
            cuentas = cuentas + cursor.fetchall()

        for cuenta in cuentas:
            id_cuenta = cuenta[0]
            nombre_cuenta = cuenta[1]

            # Obtener totales de los mayores
            cursor.execute("SELECT SUM(debe), SUM(haber) FROM libros_diarios WHERE id_cuenta = %s", (id_cuenta,))
            total_debe, total_haber = cursor.fetchone()

            total_debe = total_debe if total_debe is not None else 0
            total_haber = total_haber if total_haber is not None else 0

            # Determinar el saldo
            saldo_debe = total_debe - total_haber if total_debe > total_haber else 0
            saldo_haber = total_haber - total_debe if total_haber > total_debe else 0

            # Solo insertar en la tabla si hay saldo

            saldoreal = saldo_debe if saldo_debe > 0 else saldo_haber

            tot_categoria= tot_categoria + saldoreal
        return tot_categoria

    def detalle_categoria(self, cuentasreal):
        ventana_detalle = tk.Toplevel(self.master)
        ventana_detalle.title("Cuentas relacionadas a esta categoria")
        ventana_detalle.geometry("800x400")

        tabla_frame = tk.Frame(ventana_detalle)
        tabla_frame.grid(row=0, column=0, columnspan=2)
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
        for cuenta in cuentas:
            id_cuenta = cuenta[0]
            nombre_cuenta = cuenta[1]
            nombre_formateado = str(id_cuenta) + "-" + str(nombre_cuenta)

            # Obtener totales de los mayores
            cursor.execute("SELECT SUM(debe), SUM(haber) FROM libros_diarios WHERE id_cuenta = %s", (id_cuenta,))
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
            tabla_in.insert("", "end", values=(nombre_formateado, saldoreal), tags=tag)


