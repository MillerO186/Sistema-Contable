import tkinter as tk
from tkinter import *
from tkinter import ttk

from tkcalendar import Calendar
from datetime import datetime
from PIL import Image, ImageTk


class DiariosHub(tk.Frame):
    def __init__(self, parent, connection):
        super().__init__(parent)
        # Diccionario con los tipos de elementos
        self.dicdiasfrec = {}
        # Variables especiables de tkinter
        self.connection = connection
        self.fecha_seleccionada = tk.StringVar()
        self.elemento_seleccionado = tk.StringVar()
        self.cuenta_seleccionada = tk.StringVar()
        self.monto = tk.StringVar()
        self.tipo_cuenta = ""
        self.movimiento = tk.StringVar()  # Para seleccionar entre 'aumento' o 'disminucion'
        # El Frame
        self.frame_principal = tk.Frame(self, bg="#ECF2FF")
        self.frame_principal.pack(expand=True, fill='both')
        self.mostrar_vista_agregar()
        self.grid(row=0, column=0, sticky="nsew")    # Implementamos la lógica de elegir una fecha
    def elegir_fecha(self):
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
            calendario_window.destroy()

        # Botón para confirmar la selección de fecha
        tk.Button(calendario_window, text="Seleccionar", command=lambda: cerrar_calendario(calendario)).pack(pady=10)

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
            self.cargar_tabla(self.fecha_seleccionada.get())
            calendario_window.destroy()

        # Botón para confirmar la selección de fecha
        tk.Button(calendario_window, text="Seleccionar", command=lambda: cerrar_calendario(calendario)).pack(pady=10)

    def mostrar_vista_agregar(self):
        # Olvidamos el Frame principal
        self.frame_principal.pack_forget()
        # Creamos el frame de agregar asiento contable

        frame_vista_agregar = tk.Frame(self, bg="#ECF2FF")
        frame_vista_agregar.pack(expand=True, fill='both')
        # Campo de Fecha
        image = Image.open("imagenes_diseño/lab_campo.png")
        image = image.resize((170, 35), Image.ANTIALIAS)
        self.foto4 = ImageTk.PhotoImage(image)

        image = Image.open("imagenes_diseño/boton_cargar_cuentas.png")
        image = image.resize((140, 35), Image.ANTIALIAS)
        self.foto5 = ImageTk.PhotoImage(image)

        frame_diseño_diario = tk.Frame(frame_vista_agregar,bg="#F7FAFF")

        tk.Entry(frame_diseño_diario, width=22, bd=5, relief="sunken", font=("Rockwell", 12),
                 textvariable=self.fecha_seleccionada, state="readonly").grid(row=0, column=2,
                                                                              padx=10, pady=10, sticky="w")
        tk.Button(frame_diseño_diario, image=self.foto5, borderwidth=0, compound="center",bg="#F7FAFF", font=("Rockwell", 12),
                  text="Seleccionar Fecha", command=lambda: self.elegir_fecha()).grid(row=0,
                                                                                      column=3,
                                                                                      padx=10,
                                                                                      pady=10, sticky="w")
        tk.Label(frame_diseño_diario,bg="#F7FAFF", text="Fecha", image=self.foto4, compound="center", font=("Rockwell", 15)).grid(
            row=0, column=1, padx=10, pady=10, sticky="e")

        # Elegir elemento para filtrar cuenta

        tk.Label(frame_diseño_diario, text="Elemento", image=self.foto4, bg="#F7FAFF",compound="center", font=("Rockwell", 15)).grid(
            row=1, column=1, padx=10, pady=10, sticky="e")
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM catalogo_elementos")
        elementos = cursor.fetchall()
        elemento = [str(element[0]) + "-" + str(element[1]) for element in elementos]
        elemento_menu = ttk.Combobox(frame_diseño_diario, textvariable=self.elemento_seleccionado, values=elemento,
                                     state="readonly", font=("Rockwell", 12))
        elemento_menu.grid(row=1, column=2, padx=10, pady=10)

        # Elegir cuenta filtrada segun elemento
        def cargar_cuentas():
            if elemento_menu.get():  # Verificar que hay un elemento seleccionado
                # Extraer el id del elemento del string seleccionado
                id_elemento = int(elemento_menu.get().split('-')[0])
                cuentacursor = self.connection.cursor()
                cuentacursor.execute("SELECT * FROM catalogo_cuentas WHERE id_elemento = %s", (id_elemento,))
                cuentas = cuentacursor.fetchall()

                cuenta = [str(cuenta[0]) + "-" + str(cuenta[2]) for cuenta in cuentas]
                cuenta_menu['values'] = cuenta  # Actualizar las opciones del menú de cuentas
            else:
                # Aquí puedes manejar el caso donde no hay un elemento seleccionado
                print("Por favor, selecciona un elemento primero.")

        tk.Button(frame_diseño_diario, text="Cargar Cuentas",bg="#F7FAFF", image=self.foto5, borderwidth=0, compound="center",
                  font=("Rockwell", 12), command=cargar_cuentas).grid(row=1, column=3, padx=10,
                                                                      pady=10)

        # Elegir cuenta filtrada según elemento
        tk.Label(frame_diseño_diario, text="Cuenta", bg="#F7FAFF",image=self.foto4, compound="center", font=("Rockwell", 15)).grid(
            row=2, column=1, padx=10, pady=10, sticky="e")
        cuenta_menu = ttk.Combobox(frame_diseño_diario, textvariable=self.cuenta_seleccionada, state="readonly",
                                   font=("Rockwell", 12))
        cuenta_menu.grid(row=2, column=2, padx=10, pady=10)

        # Escribir monto
        tk.Label(frame_diseño_diario, text="Monto", image=self.foto4, bg="#F7FAFF",compound="center", font=("Rockwell", 15)).grid(
            row=3, column=1, padx=10, pady=10, sticky="e")
        tk.Entry(frame_diseño_diario, textvariable=self.monto, width=22, font=("Rockwell", 12), bd=5,
                 relief="sunken").grid(row=3, column=2, padx=10, pady=10)

        # Botones de opción para Aumento o disminución
        tk.Radiobutton(frame_diseño_diario, text="Aumenta", variable=self.movimiento, value="Aumenta",
                       font=("Rockwell", 10),
                       bg="#F7FAFF").grid(row=4, column=2,
                                          sticky="w")
        tk.Radiobutton(frame_diseño_diario, text="Disminuye", variable=self.movimiento, value="Disminuye",
                       font=("Rockwell", 10),
                       bg="#F7FAFF").grid(row=4, column=3,
                                          sticky="w")
        frame_diseño_diario.grid(row=1, column=0, padx=1, pady=10, sticky="w")

        frame_diseño_botones = tk.Frame(frame_vista_agregar,bg="#ECF2FF")
        image = Image.open("imagenes_diseño/boton_guardar_diario.png")
        image = image.resize((200, 50), Image.ANTIALIAS)
        self.foto = ImageTk.PhotoImage(image)
        # Añadimos botones y decoracion
        tk.Button(frame_diseño_botones, bg="#ECF2FF",text="Guardar", image=self.foto, borderwidth=0, command=self.guardar_registro,
                  compound="center", font=("Rockwell", 15)).grid(
            row=1, column=0,
            padx=10, pady=20)
        image = Image.open("imagenes_diseño/boton_actualizar_diario.png")
        image = image.resize((200, 50), Image.ANTIALIAS)
        self.foto1 = ImageTk.PhotoImage(image)
        tk.Button(frame_diseño_botones,bg="#ECF2FF", text="Modificar", image=self.foto1, borderwidth=0, compound="center",
                  font=("Rockwell", 15), command=self.mostrar_ventana_modificar).grid(row=1, column=1,
                                                                                      padx=10, pady=20)
        image = Image.open("imagenes_diseño/boton_eliminar_diario.png")
        image = image.resize((200, 50), Image.ANTIALIAS)
        self.foto2 = ImageTk.PhotoImage(image)
        tk.Button(frame_diseño_botones, bg="#ECF2FF",text="Eliminar", image=self.foto2, borderwidth=0, compound="center",
                  font=("Rockwell", 15), command=self.borra_registro_seleccionado).grid(row=2, column=0,
                                                                                        padx=10, pady=20)
        image = Image.open("imagenes_diseño/boton_cargar_diarios.png")
        image = image.resize((200, 50), Image.ANTIALIAS)
        self.foto6 = ImageTk.PhotoImage(image)
        tk.Button(frame_diseño_botones,bg="#ECF2FF", text="Cargar Tabla", image=self.foto6, borderwidth=0, compound="center",
                  font=("Rockwell", 15), command=self.elegir_fecha_para_tabla).grid(row=2, column=1,
                                                                                    padx=10, pady=20)
        image = Image.open("imagenes_diseño/boton_dias_no_cuadran.png")
        image = image.resize((200, 50), Image.ANTIALIAS)
        self.foto7 = ImageTk.PhotoImage(image)
        tk.Button(frame_diseño_botones,bg="#ECF2FF", text="Cuadrar dias", image=self.foto7, borderwidth=0, compound="center",
                  font=("Rockwell", 15), command=self.mostrar_dias_no_cuadran).grid(row=3, column=0,
                                                                                    padx=10, pady=20)

        frame_diseño_botones.grid(row=1, column=1, padx=1, pady=10, sticky="w")

        global tabla
        tabla = ttk.Treeview(frame_vista_agregar, columns=("ID", "Fecha", "Cuenta", "Debe", "Haber"), show="headings")
        tabla.heading("ID", text="ID", )
        tabla.column("ID", width=0, stretch=tk.NO)
        tabla.heading("Fecha", text="Fecha")
        tabla.heading("Cuenta", text="Cuenta")
        tabla.heading("Debe", text="Debe")
        tabla.heading("Haber", text="Haber")
        tabla.grid(row=8, column=0, columnspan=2, padx=10, pady=10)
        tabla.column("Fecha", width=250)
        tabla.column("Cuenta", width=250)
        tabla.column("Debe", width=250)
        tabla.column("Haber", width=250)
        # Barra de desplazamiento
        scrollbar = ttk.Scrollbar(frame_vista_agregar, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=8, column=2, sticky='ns')
        # Para realizar la carga inicial de la tabla
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Rockwell", 12, "bold"), foreground="black")
        style.configure("Treeview", font=("Rockwell", 12))  # Cambia la fuente de los registros

    def cargar_tabla(self, fecha_elegida):
        self.dicdiasfrec = {}
        cursorcargainicial = self.connection.cursor()
        cursorcargainicial.execute("SELECT * FROM libros_diarios WHERE fecha=%s ORDER BY fecha DESC", (fecha_elegida,))

        tabla_diarios = cursorcargainicial.fetchall()
        dias = []

        tabla.tag_configure('evenrow', background="#F0F0F0")
        tabla.tag_configure('oddrow', background="white")

        for fila_id in tabla.get_children():
            tabla.delete(fila_id)
        cont = 0
        for diario in tabla_diarios:
            if cont % 2 == 0:
                tag = 'evenrow'
            else:
                tag = 'oddrow'
            cursordecuenta = self.connection.cursor()
            cursordecuenta.execute("SELECT nombre FROM catalogo_cuentas WHERE id_cuenta = %s", (diario[2],))
            cuenta = cursordecuenta.fetchone()
            cuenta = str(cuenta).split("'")[1]
            cuenta_compuesta = str(diario[2]) + "-" + str(cuenta)
            cont = cont + 1
            fecha_formateada = diario[1].strftime("%d/%m/%y")
            dias.append(fecha_formateada)
            tabla.insert("", "end", values=(diario[0], diario[1], cuenta_compuesta, diario[3], diario[4]), tags=tag)

        for dia in dias:
            if dia not in self.dicdiasfrec.keys():
                self.dicdiasfrec[dia] = 1
            else:
                self.dicdiasfrec[dia] = self.dicdiasfrec[dia] + 1

    def guardar_registro(self):
        self.cargar_tabla(self.fecha_seleccionada.get())
        diccionariotipos = {
            "Activo": [1, 2, 3],
            "Pasivo": [4],
            "Capital": [5],
            "Gasto": [6],
            "Ingreso": [7],
            "Costo": [8]
        }
        # funcion que guarda un registro en la tabla que se muestra y tmb en la base de datos
        fecha = self.fecha_seleccionada.get()
        cuenta = self.cuenta_seleccionada.get()
        numero_elemento = int(self.elemento_seleccionado.get()[0])
        for tipo, elementos in diccionariotipos.items():
            if numero_elemento in elementos:
                tipo_elemento = tipo
                break
        print(tipo_elemento)
        debe = ""
        haber = ""

        def obtenerID():
            ids = []
            for item in tabla.get_children():
                valores = tabla.item(item, "values")
                if fecha == valores[1][8:10] + "/" + valores[1][5:7] + "/" + valores[1][2:4]:
                    ids.append(valores[0].split("/")[-1])
            if len(ids) != 0:
                ID = max(int(i) for i in ids)
            else:
                ID = 1
            return str(ID)

        ID = fecha + "/" + str(int(obtenerID()) + 1)

        if self.movimiento.get() == "Aumenta" and (
                tipo_elemento == "Ingreso" or tipo_elemento == "Pasivo" or tipo_elemento == "Capital"):
            haber = self.monto.get()
            debe = ""
        if self.movimiento.get() == "Aumenta" and (
                tipo_elemento == "Activo" or tipo_elemento == "Costo" or tipo_elemento == "Gasto"):
            debe = self.monto.get()
            haber = ""
        if self.movimiento.get() == "Disminuye" and (
                tipo_elemento == "Ingreso" or tipo_elemento == "Pasivo" or tipo_elemento == "Capital"):
            haber = ""
            debe = self.monto.get()
        if self.movimiento.get() == "Disminuye" and (
                tipo_elemento == "Activo" or tipo_elemento == "Costo" or tipo_elemento == "Gasto"):
            debe = ""
            haber = self.monto.get()

        insertarcursor = self.connection.cursor()
        numero_cuenta = int(cuenta.split("-")[0])
        if debe != "":
            debe = int(debe)
        if haber != "":
            haber = int(haber)
        insertarcursor.execute(
            'INSERT INTO libros_diarios(id_libro,fecha, id_cuenta, debe, haber) VALUES (%s,%s, %s, %s, %s);', (
                ID, fecha, numero_cuenta, debe if type(debe) is int else 0, haber if type(haber) is int else 0))

        self.cargar_tabla(fecha)
        self.connection.commit()

    def cuadrar(self):
        cuadracursor = self.connection.cursor()
        cuadracursor.execute(
            "SELECT fecha , SUM(debe) as debe_acum, SUM(haber) as haber_acum FROM public.libros_diarios GROUP BY fecha")

        fechas_sumas = cuadracursor.fetchall()

        fechas_no_cuadran = []

        for fecha, sum_debe, sum_haber in fechas_sumas:
            if sum_debe != sum_haber:
                fechas_no_cuadran.append(fecha)
        return fechas_no_cuadran

    def borra_registro_seleccionado(self):
        seleccion = tabla.selection()
        if not seleccion:
            print("No se ha seleccionado ningún registro")
        # Obtenemos el ID (invisible)
        registro_id = seleccion[0]
        valores = tabla.item(registro_id, "values")
        borrarcursor = self.connection.cursor()
        borrarcursor.execute("DELETE FROM libros_diarios WHERE id_libro =%s;", (valores[0],))
        self.cargar_tabla(valores[1])
        self.connection.commit()

    def mostrar_dias_no_cuadran(self):
        # Crear una nueva ventana
        ventana_no_cuadran = tk.Toplevel(self.master)
        ventana_no_cuadran.title("Días que no Cuadran")
        ventana_no_cuadran.geometry("800x400")

        # Crear el Treeview con una columna identificada como "dias_no_cuadran"
        tabladias = ttk.Treeview(ventana_no_cuadran, columns=("dias_no_cuadran"), show="headings")
        tabladias.heading("dias_no_cuadran", text="Días que no Cuadran")
        tabladias.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Ajustar la expansión de la tabla dentro de la ventana
        ventana_no_cuadran.grid_rowconfigure(0, weight=1)
        ventana_no_cuadran.grid_columnconfigure(0, weight=1)

        # Barra de desplazamiento
        scrollbar = ttk.Scrollbar(ventana_no_cuadran, orient="vertical", command=tabladias.yview)
        tabladias.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=2, sticky='ns')

        # Aplicar el estilo al encabezado
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Rockwell", 12, "bold"), foreground="black")
        style.configure("Treeview", font=("Rockwell", 12))
        # Cargar los datos en la tabla
        fechas_no_cuadran = self.cuadrar()  # Asegúrate de que esta función devuelva datos correctos
        tabladias.tag_configure('evenrow', background="#F0F0F0")
        tabladias.tag_configure('oddrow', background="white")
        cont=0
        for fecha in fechas_no_cuadran:
            if cont % 2 == 0:
                tag = 'evenrow'
            else:
                tag = 'oddrow'
            cont=cont+1
            tabladias.insert("", "end", values=(fecha,),tags=tag)

        # Función para mostrar el diario cuando se selecciona una fila
        def mostrar_diario():
            seleccion = tabladias.selection()
            if not seleccion:
                print("No se ha seleccionado ningún registro")
                return  # Salir si no hay ninguna selección
            registro_id = seleccion[0]
            valores = tabladias.item(registro_id, "values")
            self.cargar_tabla(valores)  # Asegúrate de que esta función esté definida correctamente
            ventana_no_cuadran.destroy()

        # Botón para mostrar el diario
        tk.Button(ventana_no_cuadran, text="Mostrar Diarios", image=self.foto5, borderwidth=0, compound="center",
                  font=("Rockwell", 12), command=mostrar_diario).grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def mostrar_ventana_modificar(self):
        seleccion = tabla.selection()
        if not seleccion:
            print("No se ha seleccionado ningún registro")
            return  # Salir si no hay ninguna selección

        # Obtenemos el ID (invisible)
        registro_id = seleccion[0]
        valores = tabla.item(registro_id, "values")

        # Creamos una ventana emergente
        ventana_modificar = tk.Toplevel(self.master)
        ventana_modificar.title("Modificar o Eliminar Registro")
        ventana_modificar.geometry("800x400")

        # Campo de monto (editable)
        tk.Label(ventana_modificar, text="Monto", image=self.foto4, compound="center", font=("Rockwell", 15)).grid(
            row=0, column=0, padx=10, pady=10, sticky="e")
        tk.Entry(ventana_modificar, textvariable=self.monto, width=22, font=("Rockwell", 12), bd=5,
                 relief="sunken").grid(row=0, column=1, padx=10, pady=10)
        self.monto.set(valores[3] if valores[3] != '0' else valores[4])  # Mostrar el monto actual

        # Selección de "Aumenta" o "Disminuye" (editable)
        tk.Label(ventana_modificar, text="Movimiento").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        tk.Radiobutton(ventana_modificar, text="Aumenta", variable=self.movimiento, value="Aumenta").grid(row=2,
                                                                                                          column=1,
                                                                                                          sticky="w")
        tk.Radiobutton(ventana_modificar, text="Disminuye", variable=self.movimiento, value="Disminuye").grid(row=2,
                                                                                                              column=2,
                                                                                                              sticky="w")

        diccionariotipos = {
            "Activo": [1, 2, 3],
            "Pasivo": [4],
            "Capital": [5],
            "Gasto": [6],
            "Ingreso": [7],
            "Costo": [8]
        }

        # función para guardar el registro modificado
        def modificar():
            # Obtenemos el tipo de elemento según el número
            numero_elemento = int(valores[2][0])
            tipo_elemento = ""
            for tipo, elementos in diccionariotipos.items():
                if numero_elemento in elementos:
                    tipo_elemento = tipo
                    break

            debe = ""
            haber = ""

            # Obtenemos el valor seleccionado de 'movimiento' en el momento adecuado
            movimiento_actual = self.movimiento.get()

            if movimiento_actual == "Aumenta" and (
                    tipo_elemento == "Ingreso" or tipo_elemento == "Pasivo" or tipo_elemento == "Capital"):
                haber = self.monto.get()
                debe = ""
            elif movimiento_actual == "Aumenta" and (
                    tipo_elemento == "Activo" or tipo_elemento == "Costo" or tipo_elemento == "Gasto"):
                debe = self.monto.get()
                haber = ""
            elif movimiento_actual == "Disminuye" and (
                    tipo_elemento == "Ingreso" or tipo_elemento == "Pasivo" or tipo_elemento == "Capital"):
                haber = ""
                debe = self.monto.get()
            elif movimiento_actual == "Disminuye" and (
                    tipo_elemento == "Activo" or tipo_elemento == "Costo" or tipo_elemento == "Gasto"):
                debe = ""
                haber = self.monto.get()
            if debe != "":
                debe = int(debe)
            if haber != "":
                haber = int(haber)
            numero_cuenta = int(valores[2].split("-")[0])

            actucursor = self.connection.cursor()
            actucursor.execute(
                "UPDATE public.libros_diarios SET fecha=%s, id_cuenta=%s, debe=%s, haber=%s WHERE id_libro=%s;",
                (valores[1], numero_cuenta, debe if type(debe) is int else 0, haber if type(haber) is int else 0,
                 valores[0])
            )
            self.cargar_tabla(valores[1])
            self.connection.commit()
            ventana_modificar.destroy()

        tk.Button(ventana_modificar, text="Modificar", image=self.foto5, borderwidth=0, compound="center",
                  font=("Rockwell", 12), command=modificar).grid(row=3, column=0, columnspan=2, padx=10, pady=10)
