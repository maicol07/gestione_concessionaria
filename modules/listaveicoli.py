from tkinter import *
from tkinter.ttk import *

import src.Style
from lib.medoo.database.sqlite import Sqlite
from src.Veicolo import Veicolo


class ListaVeicoli():
    def __init__(self, marca, db):
        """
        Mostra all'utente una lista di veicoli di una determinata marca tra cui scegliere

        :param marca:
        :param Sqlite db:
        :return:
        """
        w = Toplevel()
        w.title("Lista veicoli")
        w.iconphoto(True, PhotoImage(file="img/icon.png"))
        self.__root = w
        self.__style = src.Style.s
        self.__db = db
        self.__marca = marca
        # ===== FILTRO ===== #
        f = Labelframe(w, text="Filtra")
        f.pack()
        self.__SEARCH = StringVar()
        search = Entry(f, textvariable=self.__SEARCH)
        search.grid(row=0, column=0, padx=10, pady=5)
        filter_icon = PhotoImage(file="img/search.png")
        btn_filter = Button(f, text="Filtra", compound=LEFT, image=filter_icon)
        btn_filter.grid(row=0, column=1, padx=10, pady=5)
        reset_icon = PhotoImage(file="img/restore.png")
        btn_reset = Button(f, text="Reset", compound=LEFT, image=reset_icon)
        btn_reset.grid(row=0, column=2, padx=10, pady=5)

        # ===== TREEVIEW ===== #
        scrollbarx = Scrollbar(w, orient=HORIZONTAL)
        scrollbary = Scrollbar(w, orient=VERTICAL)
        self.__tree = Treeview(w, columns=(
        "marca", "serie", "modello", "cv", "anno_costruzione", "categoria", "prezzo", "qta"),
                               selectmode="extended", height=400, yscrollcommand=scrollbary.set,
                               xscrollcommand=scrollbarx.set)
        scrollbary.config(command=self.__tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=self.__tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        self.__tree.heading('#0', text="ID", anchor=W)
        self.__tree.heading('marca', text="Marca", anchor=W)
        self.__tree.heading('serie', text="Serie", anchor=W)
        self.__tree.heading('modello', text="Modello", anchor=W)
        self.__tree.heading('cv', text="Cavalli", anchor=W)
        self.__tree.heading('anno_costruzione', text="Anno di costr.", anchor=W)
        self.__tree.heading('categoria', text="Categoria", anchor=W)
        self.__tree.heading('prezzo', text="Prezzo", anchor=W)
        self.__tree.heading('qta', text="Quantità disp.", anchor=W)
        self.__tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.__tree.column('marca', stretch=NO, minwidth=0, width=80)
        self.__tree.column('serie', stretch=NO, minwidth=0, width=80)
        self.__tree.column('modello', stretch=NO, minwidth=0, width=120)
        self.__tree.column('cv', stretch=NO, minwidth=0, width=50)
        self.__tree.column('anno_costruzione', stretch=NO, minwidth=0, width=100)
        self.__tree.column('categoria', stretch=NO, minwidth=0, width=120)
        self.__tree.column('prezzo', stretch=NO, minwidth=0, width=100)
        self.__tree.column('qta', stretch=NO, minwidth=0, width=80)
        self.__tree.pack()
        self.__veicoli = []
        res = self.__db.select("veicoli", "id", where={"marca": self.__marca})
        for veicolo in res:
            v = Veicolo(self.__db, veicolo.id)
            self.__tree.insert('', 'end', text=v.id, values=vars(v).values())

    def search(self):
        if self.__SEARCH.get() != "":
            self.__tree.delete(*self.__tree.get_children())
            res = self.__db.select("veicoli", "id",
                                   where={"marca": self.__marca, "modello[~]": self.__SEARCH.get() + '%'})
            for veicolo in res:
                v = Veicolo(self.__db, res.id)
                self.__tree.insert('', 'end', values=vars(v))

    def reset(self):
        self.__tree.delete(*self.__tree.get_children())
        res = self.__db.select("veicoli", "id", where={"marca": self.__marca})
        for veicolo in res:
            v = Veicolo(self.__db, res.id)
            self.__tree.insert('', 'end', text=v.id, values=vars(v).values())
