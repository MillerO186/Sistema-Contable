import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar

from conex_posgres import crear_conexion
from vistas.balancecomprobacion import BalanceComprobacion
from vistas.balancegeneral import BalanceGeneral
from vistas.estadoresultados import EstadoResultados
from vistas.librosdiarioshub import DiariosHub
from vistas.mayores import MayoresHub


class AplicacionPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Grupo 5 Sistema Contable')
        self.geometry("1600x800")
        self.connection = crear_conexion()

        # La barra de navegación de arriba
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)  # Cambiado para que el Notebook ocupe tudo el espacio

        self.crear_vistas()

    def crear_vistas(self):
        hubdiario_frame = DiariosHub(self.notebook, self.connection)
        self.notebook.add(hubdiario_frame, text='Libros Diarios')

        hubmayor_frame = MayoresHub(self.notebook, self.connection)
        self.notebook.add(hubmayor_frame, text='Mayores')

        hubbalance_frame = BalanceComprobacion(self.notebook, self.connection)
        self.notebook.add(hubbalance_frame, text='Balance de Comprobación')

        hubbalancegeneral_frame = BalanceGeneral(self.notebook, self.connection)
        self.notebook.add(hubbalancegeneral_frame, text="Balance General")

        hubestadoresultados_frame = EstadoResultados(self.notebook, self.connection)
        self.notebook.add(hubestadoresultados_frame, text="Estado de resultados")

if __name__ == '__main__':
    app = AplicacionPrincipal()
    app.mainloop()
