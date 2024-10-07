import tkinter as tk
from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk


class MayoresHub(tk.Frame):
    def __init__(self, parent, connection):
        super().__init__(parent)
        self.connection = connection

        # Frame principal con scrollbar general
        self.canvas = tk.Canvas(self)
        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar_y.pack(side="right", fill="y")

        # Scrollbar horizontal
        self.scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.scrollbar_x.pack(side="bottom", fill="x")

        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        self.total_debe_general = 0
        self.total_haber_general = 0
        self.x = 0
        self.y = 0
        self.frame_principal = tk.Frame(self.canvas, bg="#F7F7F7")
        self.canvas.create_window((0, 0), window=self.frame_principal, anchor="nw")

        image = Image.open("imagenes_diseño/total_mayor_por_cuenta.png")
        image = image.resize((140, 35), Image.ANTIALIAS)
        self.foto8 = ImageTk.PhotoImage(image)
        image = Image.open("imagenes_diseño/saldo_total_por_cuenta.png")
        image = image.resize((140, 35), Image.ANTIALIAS)
        self.foto9 = ImageTk.PhotoImage(image)
        image = Image.open("imagenes_diseño/total_debe_haber_general.png")
        image = image.resize((140, 35), Image.ANTIALIAS)
        self.foto10 = ImageTk.PhotoImage(image)
        image = Image.open("imagenes_diseño/boton_mostrar_mayores.png")
        image = image.resize((140, 35), Image.ANTIALIAS)
        self.foto11 = ImageTk.PhotoImage(image)
        self.frame_principal.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        frame_titulo_boton = tk.Frame(self.frame_principal)
        frame_titulo_boton.grid(row=0, column=0, columnspan=2)
        # Título centrado
        tk.Label(frame_titulo_boton, text="Libros Mayores", font=("Rockwell", 16, "bold"), bg="#F7F7F7").grid(row=0,
                                                                                                              column=0)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Rockwell", 12, "bold"), foreground="black")
        style.configure("Treeview", font=("Rockwell", 12))  # Cambia la fuente de los registros

        def mostrar_mayores():
            self.x = 0
            self.y = 0
            # Frame donde se colocarán los mayores
            self.frame_tablas = tk.Frame(self.frame_principal)
            self.frame_tablas.grid(row=1, column=0, columnspan=3)
            # Limpiar las tablas anteriores
            for widget in self.frame_tablas.winfo_children():
                widget.destroy()

            cursorcuentas = self.connection.cursor()
            cursorcuentas.execute("""
                        SELECT DISTINCT c.id_cuenta, c.nombre 
                        FROM catalogo_cuentas c
                        JOIN libros_diarios ld ON c.id_cuenta = ld.id_cuenta
                    """)
            cuentas_con_movimientos = cursorcuentas.fetchall()
            for id_cuenta, nombre in cuentas_con_movimientos:
                self.mostrar_mayor(self.frame_tablas, id_cuenta, nombre, self.y,self.x )
                if self.x // 2 >= 1:
                    self.y = self.y + 1
                    self.x = 0
                else:
                    self.x = self.x + 1
            frame_debe_general = tk.Frame(self.frame_principal)
            frame_debe_general.grid(row=2, column=0)
            tk.Label(frame_debe_general, text="Debe General", image=self.foto10, font=("Rockwell", 13),
                     compound="center").grid(
                row=0, column=0)
            total_debe_general_var = tk.IntVar(value=self.total_debe_general)

            tk.Entry(frame_debe_general, textvariable=total_debe_general_var, width=22, font=("Rockwell", 12), bd=5,
                     relief="sunken").grid(row=0, column=1)

            frame_haber_general = tk.Frame(self.frame_principal)
            frame_haber_general.grid(row=2, column=1)
            tk.Label(frame_haber_general, text="Haber General", image=self.foto10, font=("Rockwell", 13),
                     compound="center").grid(row=0, column=0)
            total_haber_general_var = tk.IntVar(value=self.total_haber_general)

            tk.Entry(frame_haber_general, textvariable=total_haber_general_var, width=22, font=("Rockwell", 12), bd=5,
                     relief="sunken").grid(row=0, column=1)

        # Botón para cargar todos los mayores centrado
        tk.Button(frame_titulo_boton, text="Mostrar Mayores", image=self.foto11, borderwidth=0, font=("Rockwell", 12),
                  compound="center", command=mostrar_mayores).grid(row=0, column=1)
        mostrar_mayores()



    def mostrar_mayor(self, frame, id_cuenta, nombre, row, column):

        frame_mayor = tk.Frame(frame, bd=2, relief="solid")
        frame_mayor.grid(row=row, column=column, sticky="nsew")

        # Configurar la columna del grid para que el nombre de la cuenta esté a la izquierda y la tabla a la derecha
        frame_mayor.grid_columnconfigure(0, weight=1)  # Columna 0 para el nombre
        frame_mayor.grid_columnconfigure(1, weight=1)  # Columna 1 para la tabla

        # Etiqueta para el nombre de la cuenta
        tk.Label(frame_mayor, text=f"Cuenta: {nombre}", font=("Rockwell", 20), bg="#F7F7F7").grid(row=0, column=0,
                                                                                                  sticky="w", padx=10)

        total_debe_cuenta = 0
        total_haber_cuenta = 0

        frame_debe_haber = tk.Frame(frame_mayor)
        frame_debe_haber.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)

        # Frame para la tabla "debe" (a la izquierda)
        frame_tabla_debe = tk.Frame(frame_debe_haber)
        frame_tabla_debe.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

        # Configurar para que la tabla se extienda en el frame
        tabla_debe = ttk.Treeview(frame_tabla_debe, columns=("Fecha", "Debe"), show="headings")
        tabla_debe.heading("Fecha", text="Fecha")
        tabla_debe.heading("Debe", text="Debe")
        tabla_debe.pack(side="right", fill="both", expand=True)

        # Scrollbar para la tabla "debe"
        scrollbar_tabla_debe = ttk.Scrollbar(frame_tabla_debe, orient="vertical", command=tabla_debe.yview)
        tabla_debe.configure(yscrollcommand=scrollbar_tabla_debe.set)
        scrollbar_tabla_debe.pack(side="right", fill="y")

        # Consultar los registros de "debe"
        cargarcursor = self.connection.cursor()
        cargarcursor.execute("""
            SELECT fecha, debe FROM libros_diarios WHERE id_cuenta = %s AND debe != 0 ORDER BY fecha
        """, (id_cuenta,))
        diarios_debe = cargarcursor.fetchall()

        tabla_debe.tag_configure('evenrow', background="#F0F0F0")
        tabla_debe.tag_configure('oddrow', background="white")
        cont = 0
        for diario in diarios_debe:
            if cont % 2 == 0:
                tag = 'evenrow'
            else:
                tag = 'oddrow'
            cont = cont + 1
            fecha = diario[0].strftime("%d/%m/%Y")
            debe = diario[1]
            tabla_debe.insert("", "end", values=(fecha, debe), tags=tag)
            total_debe_cuenta += debe

        # Frame para la tabla "haber" (a la derecha)
        frame_tabla_haber = tk.Frame(frame_debe_haber)
        frame_tabla_haber.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

        # Configurar para que la tabla se extienda en el frame
        tabla_haber = ttk.Treeview(frame_tabla_haber, columns=("Haber", "Fecha"), show="headings")
        tabla_haber.heading("Haber", text="Haber")
        tabla_haber.heading("Fecha", text="Fecha")
        tabla_haber.pack(side="right", fill="both", expand=True)

        # Scrollbar para la tabla "haber"
        scrollbar_tabla_haber = ttk.Scrollbar(frame_tabla_haber, orient="vertical", command=tabla_haber.yview)
        tabla_haber.configure(yscrollcommand=scrollbar_tabla_haber.set)
        scrollbar_tabla_haber.pack(side="right", fill="y")

        # Consultar los registros de "haber"
        cargarcursor.execute("""
            SELECT fecha, haber FROM libros_diarios WHERE id_cuenta = %s AND haber != 0 ORDER BY fecha
        """, (id_cuenta,))
        diarios_haber = cargarcursor.fetchall()

        cont = 0
        tabla_haber.tag_configure('evenrow', background="#F0F0F0")
        tabla_haber.tag_configure('oddrow', background="white")

        for diario in diarios_haber:
            if cont % 2 == 0:
                tag = 'evenrow'
            else:
                tag = 'oddrow'
            cont = cont + 1
            fecha = diario[0].strftime("%d/%m/%Y")
            haber = diario[1]
            tabla_haber.insert("", "end", values=(haber, fecha), tags=tag)
            total_haber_cuenta += haber

        # Calcular saldo total como el valor absoluto de la diferencia
        saldo_total = abs(total_debe_cuenta - total_haber_cuenta)

        # Mostrar total debe, total haber y saldo debajo de cada tabla

        fram_total_debe=tk.Label(frame_debe_haber)
        fram_total_debe.grid(row=1, column=0,sticky="we")
        tk.Label(fram_total_debe, text="Total Debe", image=self.foto8, font=("Rockwell", 13),compound="center").grid(row=1, column=0,
                                                                                                    sticky="we")
        total_debe_cuenta_var = tk.IntVar(value=total_debe_cuenta)
        tk.Entry(fram_total_debe, textvariable=total_debe_cuenta_var, width=22,state="readonly",font=("Rockwell",12),bd=5, relief="sunken").grid(row=1, column=1, padx=10, pady=10)

        fram_total_haber = tk.Label(frame_debe_haber)
        fram_total_haber.grid(row=1, column=1, sticky="we")
        tk.Label(fram_total_haber, text="Total Haber", image=self.foto8, font=("Rockwell", 13),compound="center").grid(row=1, column=0,
                                                                                                     sticky="we")
        total_haber_cuenta_var = tk.IntVar(value=total_haber_cuenta)

        tk.Entry(fram_total_haber, state="readonly",textvariable=total_haber_cuenta_var, width=22,font=("Rockwell",12),bd=5, relief="sunken").grid(row=1, column=1, padx=10, pady=10)

        tk.Label(frame_mayor, text="Saldo Total", image=self.foto9, font=("Rockwell", 13), compound="center").grid(row=3,  padx=300,column=0, sticky="w",columnspan=2)
        total_saldo_var = tk.IntVar(value=saldo_total)

        tk.Entry(frame_mayor, state="readonly",textvariable=total_saldo_var, width=22, font=("Rockwell", 12), bd=5,
                 relief="sunken").grid(row=3, column=0, columnspan=2, padx=230, pady=10,sticky="e")



        # Actualizar el total general
        self.total_debe_general += total_debe_cuenta
        self.total_haber_general += total_haber_cuenta

