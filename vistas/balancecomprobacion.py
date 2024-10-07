import tkinter as tk
from tkinter import *
from tkinter import ttk

from PIL import Image,ImageTk


class BalanceComprobacion(tk.Frame):
    def __init__(self, parent, connection):
        super().__init__(parent)
        self.connection = connection

        # Frame principal
        self.frame_principal = tk.Frame(self, bg="#F7F7F7")
        self.frame_principal.pack(expand=True, fill='both')

        # Título
        frame_titulo_boton = tk.Frame(self.frame_principal)
        frame_titulo_boton.grid(row=0, column=0, columnspan=4)
        # Título centrado
        tk.Label(frame_titulo_boton, text="Balance de Comprobación", font=("Rockwell", 16, "bold"), bg="#F7F7F7").grid(row=0,
                                                                                                              column=0)
        image = Image.open("imagenes_diseño/boton_mostrar_mayores.png")
        image = image.resize((140, 35), Image.ANTIALIAS)
        self.foto11 = ImageTk.PhotoImage(image)

        image = Image.open("imagenes_diseño/saldo_total_por_cuenta.png")
        image = image.resize((140, 35), Image.ANTIALIAS)
        self.foto9 = ImageTk.PhotoImage(image)
        # Tabla para mostrar el balance general
        self.tabla_balance = ttk.Treeview(self.frame_principal, columns=("Cuenta", "Saldo Debe", "Saldo Haber"),
                                          show="headings")
        self.tabla_balance.heading("Cuenta", text="Cuenta")
        self.tabla_balance.heading("Saldo Debe", text="Saldo Debe")
        self.tabla_balance.heading("Saldo Haber", text="Saldo Haber")
        self.tabla_balance.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(self.frame_principal, orient="vertical", command=self.tabla_balance.yview)
        self.tabla_balance.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=4, sticky='ns')
        # Totales
        self.total_debe = tk.StringVar(value="0")
        self.total_haber = tk.StringVar(value="0")
        # Cargar balance general
        self.cargar_balance()

        tk.Label(self.frame_principal, text="Total Saldo Debe:", image=self.foto9, font=("Rockwell", 13),compound="center").grid(row=2, column=2, padx=5, pady=10,
                                                                                    sticky="e")
        tk.Entry(self.frame_principal, textvariable=self.total_debe, state="readonly",width=22, font=("Rockwell", 12), bd=5,
                 relief="sunken").grid(row=2, column=3, padx=10, pady=10)

        tk.Label(self.frame_principal, text="Total Saldo Haber:", image=self.foto9, font=("Rockwell", 13),compound="center").grid(row=3, column=2, padx=5, pady=10,
                                                                                     sticky="e")
        tk.Entry(self.frame_principal, textvariable=self.total_haber, state="readonly",width=22, font=("Rockwell", 12), bd=5,
                 relief="sunken").grid(row=3, column=3, padx=10,pady=10)

        tk.Button(frame_titulo_boton, text="Cargar Balance",image=self.foto11, font=("Rockwell", 12),borderwidth=0,command=self.cargar_balance,compound="center").grid(row=0, column=1, padx=10,
                                                                                             pady=10)

    def cargar_balance(self):
        for item in self.tabla_balance.get_children():
            self.tabla_balance.delete(item)
        cursor = self.connection.cursor()
        cursor.execute("SELECT id_cuenta, nombre FROM catalogo_cuentas")
        cuentas = cursor.fetchall()

        total_saldo_debe = 0
        total_saldo_haber = 0
        conta = 0
        for cuenta in cuentas:
            id_cuenta = cuenta[0]
            nombre_cuenta = cuenta[1]
            nombre_formateado = str(id_cuenta)+"-"+str(nombre_cuenta)

            # Obtener totales de los mayores
            cursor.execute("SELECT SUM(debe), SUM(haber) FROM libros_diarios WHERE id_cuenta = %s", (id_cuenta,))
            total_debe, total_haber = cursor.fetchone()

            total_debe = total_debe if total_debe is not None else 0
            total_haber = total_haber if total_haber is not None else 0

            # Determinar el saldo
            saldo_debe = total_debe - total_haber if total_debe > total_haber else 0
            saldo_haber = total_haber - total_debe if total_haber > total_debe else 0
            self.tabla_balance.tag_configure('evenrow', background="#F0F0F0")
            self.tabla_balance.tag_configure('oddrow', background="white")

            # Solo insertar en la tabla si hay saldo
            if saldo_debe > 0 or saldo_haber > 0:
                if conta % 2 == 0:
                    tag = 'evenrow'
                else:
                    tag = 'oddrow'
                conta = conta + 1
                self.tabla_balance.insert("", "end", values=(nombre_formateado, saldo_debe, saldo_haber),tags=tag)
                total_saldo_debe += saldo_debe
                total_saldo_haber += saldo_haber

        # Mostrar totales
        self.total_debe.set(str(total_saldo_debe))
        self.total_haber.set(str(total_saldo_haber))

