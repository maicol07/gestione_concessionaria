# ========== LIBRERIE INTERNE ========== #
from tkinter import *
from tkinter.ttk import *

import src.Style


class SelettoreMarche:
    def __init__(self, db):
        """
            Permette all'utente di selezionare una marca
            """
        w = Toplevel()
        w.title("Seleziona marca")
        w.iconbitmap("img/icon.ico")
        src.Style.s.change_window_bg(w)
        f = Frame(w)
        f.pack()
        marche = db.select("marche")  # seleziona tutto dalla tabella marche, ritorna un oggetto
        contr=0  # contatore righe
        contc=0  # contatore colonne
        for marca in marche:
            var = PhotoImage(file=marca.logo)  # ottengo l'oggetto " logo" (il percorso del logo)
            btn = Button(f, text=marca.name, image=var, compound=TOP)
            btn.grid(row=contr, column=contc)
            contc+=1
            if contc==2:
                contr+=1
        vari= PhotoImage(file="img/add.png")
        f1 = Frame(w)
        f1.pack()
        btn= Button(f1, text="Aggiungi", image=vari, compound=LEFT)
        btn.grid(row=0, column=0)
        vari1= PhotoImage(file="img/delete.png")
        btn2= Button(f1, text="Elimina", image=vari1, compound=LEFT)
        btn2.grid(row=0, column=1)
        w.mainloop()

    def aggiungi(self):
        w = Toplevel()
        w.title("Aggiungi marca")
        w.iconbitmap("img/icon.ico")

        f= Frame(w)
        f.pack()
        e=Label(f, text="Marca")
        e.grid(row=0, column=0)
        s = StringVar()
        ctext= Entry(w, textvariable=s)
        ctext.grid()
        f2=Frame(w)
        f2.pack()
        e1=Label()






