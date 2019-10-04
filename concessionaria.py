# ==================================== #
#       Gestione Concessionaria        #
#   by maicol07, RichiMassa1, Alecoma  #
# ==================================== #

# ========== LIBRERIE INTERNE (NECESSARIE PER INCORPORARE LIBRERIE ESTERNE SENZA USARE PIP) ========== #
import os.path
# ========== LIBRERIE INTERNE ========== #
from tkinter import *
from tkinter.ttk import *

# ========== LIBRERIE ESTERNE ========== #
from lib.medoo import Medoo  # per non scrivere i comandi SQL
from modules.selettoremarche import SelettoreMarche
# ========== MODULI DEL PROGETTO ========== #
from modules.settings import Impostazioni
# ========== CLASSI ========== #
from src.common import import_pil

import_pil()
from src.Style import Style

# Apertura database (viene creato se non esiste già il file) e creazione tabelle se non esistono già
if not (os.path.exists(os.path.expanduser('~/Documents/Gestione Concessionaria'))):
    os.makedirs(os.path.expanduser('~/Documents/Gestione Concessionaria'))
    open(os.path.expanduser('~/Documents/Gestione Concessionaria/db.db'), "w").close()  # Creazione file database
db = Medoo('sqlite', database=os.path.expanduser('~/Documents/Gestione Concessionaria/db.db'))
query = open("tables.sql")
db.connection.executescript(query.read())
query.close()


# ========== MAIN ========== #
tk = Tk()
tk.title("Gestione Concessionaria")  # Impostazione titolo
tk.iconphoto(True, PhotoImage(file="img/icon.png"))  # Impostazione icona


logo = PhotoImage(file="img/logo.png")  # Creazione variabile immagine
l = Label(tk, image=logo)  # Creazione etichetta immagine
l.pack()  # Impacchettamento etichetta (alla finestra)

# ===== FRAME PULSANTI ===== #
bf = Frame(tk)
bf.pack(pady=20)
btn = Button(bf, text="Selettore marche".upper(), command=lambda: SelettoreMarche(db))  # Creazione pulsante
btn.grid(row=0, column=0, padx=10, ipadx=5)  # Impacchettamento pulsante (alla finestra)

settings_image = PhotoImage(file="img/settings.png")
btn_settings = Button(bf, text="Impostazioni".upper(), compound=LEFT, image=settings_image,
                      command=lambda: Impostazioni(db, s))
btn_settings.grid(row=0, column=1, padx=10, ipadx=5)

# ===== IMPOSTAZIONE STILE ===== #
s = Style(db, tk)

tk.mainloop()  # Inizio ciclo eventi
db.close()  # Chiusura database
