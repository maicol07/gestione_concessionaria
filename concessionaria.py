# ==================================== #
#       Gestione Concessionaria        #
#   by maicol07, RichiMassa1, Alecoma  #
# ==================================== #

import os.path
# Aggiungendo il percorso assoluto delle librerie incluse nel progetto, è possibile importarle anche se queste ultime
# non sono installate nel sistema Python
import sys

sys.path.insert(0, os.path.abspath("lib"))

# ========== LIBRERIE INTERNE ========== #
from tkinter import *
from tkinter.ttk import *

# ========== LIBRERIE ESTERNE ========== #
from lib.medoo import Medoo  #per non scrivere i comandi SQL

# ========== MODULI DEL PROGETTO ========== #
from modules.settings import Impostazioni

# ========== CLASSI ========== #
from src.Style import Style

# Apertura database (viene creato se non esiste il file) e creazione tabelle se non esistono già
db = Medoo('sqlite', '~/Documents/Gestione Concessionaria/db.db')
query = open("tables.sql")
db.cursor.executescript(query.read())


def listaVeicoli(marca):
    """
    Mostra all'utente una lista di veicoli di una determinata marca tra cui scegliere

    :param marca:
    :return:
    """
    w = Toplevel()
    w.title("Lista veicoli")
    w.iconbitmap("img/logo.ico")

    f = Labelframe(w, text="Filtra")
    f.pack()
    search = StringVar()
    e = Entry(f, textvariable=search)
    e.grid(row=0, column=0, padx=10)
    filter_icon = PhotoImage(file="img/search.png")
    btn_filter = Button(f, text="Filtra", compound=LEFT, image=filter_icon)
    btn_filter.grid(row=0, column=1)





# Massa
def visualizzaVeicolo(veicolo):
    """
    Visualizza nel dettaglio il veicolo. È possibile anche aumentare e diminuire le quantità disponibili.

    :param veicolo:
    :return:
    """
    pass
    f = Toplevel()
    f.title("Info Veicolo")
    f.iconbitmap("img/icon.ico")
    fr = Frame(f)
    fr.pack()
    veicoli = db.select("veicoli", where={"id": veicolo})

    f.mainloop()


# ========== MAIN ========== #
tk = Tk()
tk.title("Gestione Concessionaria")  # Impostazione titolo
tk.iconbitmap("img/icon.ico")  # Impostazione icona

logo = PhotoImage(file="img/logo.png")  # Creazione variabile immagine
l = Label(tk, image=logo)  # Creazione etichetta immagine
l.pack()  # Impacchettamento etichetta (alla finestra)

# ===== FRAME PULSANTI ===== #
bf = Frame(tk)
bf.pack(pady=20)
btn = Button(bf, text="Selettore marche".upper(), command=selettoreMarche)  # Creazione pulsante
btn.grid(row=0, column=0, padx=10)  # Impacchettamento pulsante (alla finestra)

settings_image = PhotoImage(file="img/settings.png")
btn_settings = Button(bf, text="Impostazioni".upper(), compound=LEFT, image=settings_image,
                      command=lambda: Impostazioni(db, s))
btn_settings.grid(row=0, column=1, padx=10)

# ===== IMPOSTAZIONE STILE ===== #
s = Style(db)
tk.configure(background=s.color)

tk.mainloop()  # Inizio ciclo eventi
db.close()  # Chiusura database
