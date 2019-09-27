# ========== LIBRERIE INTERNE ========== #
from tkinter import *
from tkinter.ttk import *

# ========== CLASSI ========== #
from src.Style import Style


class Impostazioni:
    def __init__(self, db, style):
        """

        :param db:
        :param Style style:
        """
        self.__db = db
        self.__style = style
        w = Toplevel()
        w.title("Impostazioni")
        w.iconbitmap("img/icon.ico")

        ft = Labelframe(w, text="Cambia tema")
        ft.pack(pady=10)
        menut = Combobox(ft, postcommand=lambda: setattr(menut, "values", sorted(self.__style.getThemesList())))
        menut.set(self.__style.getCurrentThemeName())
        menut.grid(row=0, column=1, padx=10)
        # bts = Button(ft, text="SALVA", image=isave, compound=LEFT,
        #            command=lambda: salvaImpostazioni(par, menut.get()))
