# ========== LIBRERIE INTERNE ========== #
from tkinter import *
from tkinter.ttk import *

# ========== CLASSI ========== #
import src.Style


class Impostazioni:
    def __init__(self, db, style):
        """
        Inizializza l'oggetto Impostazioni

        :param db:
        :param src.Style style:
        """
        self.__db = db
        self.__style = style
        w = Toplevel()
        w.title("Impostazioni")
        w.iconbitmap("img/icon.ico")
        src.Style.s.change_window_bg(w)
        ft = Labelframe(w, text="Cambia tema")
        ft.pack(pady=10)
        menut = Combobox(ft, postcommand=lambda: menut.configure(values=sorted(self.__style.get_themes_list())))
        menut.set(self.__style.get_current_theme_name())
        menut.grid(row=0, column=0, padx=10)
        isave = PhotoImage(file="img/save.png")
        bts = Button(ft, text="SALVA", image=isave, compound=LEFT, command=lambda: self.__style.save_theme(menut.get()))
        bts.grid(row=0, column=1, padx=10)
        w.mainloop()
