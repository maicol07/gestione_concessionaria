# ==================================== #
#       Gestione Concessionaria        #
#   by maicol07, RichiMassa1, Alecoma  #
# ==================================== #

# ========== LIBRERIE INTERNE (NECESSARIE PER INCORPORARE LIBRERIE ESTERNE SENZA USARE PIP) ========== #
import os.path
import platform
import sys
import tkinter.messagebox as tkmb

sys.path.insert(0, os.path.abspath("lib"))  # Aggiungendo il percorso assoluto delle librerie incluse nel progetto,
# è possibile importarle anche se queste ultime non sono installate nel sistema Python
py_version = sys.version_info
if py_version <= (3, 5):  # Verifico che la versione di Python installata sia superiore o uguale a 3.5 per il corretto
    # funzionamento del programma. In caso negativo, lancio un messaggio di errore ed esco
    tkmb.showerror(title="Versione di Python non supportata",
                   message="La versione di Python attualmente installata ({}.{}.{}) non è supportata. Aggiornare alla "
                           "versione 3.5 o successive".format(py_version.major, py_version.minor, py_version.micro))
    exit()

system = platform.system().lower()
if system != "linux":  # escludo linux in quanto ha già Pillow installato
    if system == "windows":
        if platform.architecture()[0] == "32bit":
            os_info = "win32"
        else:
            os_info = "win-amd64"
    else:
        if py_version <= (3, 7):  # Se la versione di Python installata è minore della 3.7 su MAC il programma non
            # funzionerà correttamente. Lancio un messaggio di errore ed esco.
            tkmb.showerror(title="Versione di Python non supportata",
                           message="È stato rilevato che il sistema in uso è MAC OS X. La versione di Python "
                                   "attualmente installata ({}.{}.{}) non è supportata su questo tipo di sistema. "
                                   "Aggiornare alla versione 3.7 o successive".format(py_version.major,
                                                                                      py_version.minor,
                                                                                      py_version.micro))
            exit()
        os_info = "macosx-10.14-x86_64"
    sys.path.insert(0, os.path.abspath("lib/PIL/Pillow-6.1.0-py{}.{}-{}.egg".format(py_version.major, py_version.minor,
                                                                                    os_info)))

# ========== LIBRERIE INTERNE ========== #
from tkinter import *
from tkinter.ttk import *

# ========== LIBRERIE ESTERNE ========== #
from lib.medoo import Medoo  #per non scrivere i comandi SQL

# ========== MODULI DEL PROGETTO ========== #
from modules.settings import Impostazioni
from modules.selettoremarche import SelettoreMarche

# ========== CLASSI ========== #
from src.Style import Style

# Apertura database (viene creato se non esiste già il file) e creazione tabelle se non esistono già
if not (os.path.exists(os.path.expanduser('~/Documents/Gestione Concessionaria'))):
    os.makedirs(os.path.expanduser('~/Documents/Gestione Concessionaria'))
open(os.path.expanduser('~/Documents/Gestione Concessionaria/db.db'), "w").close()  # Creazione file database
db = Medoo('sqlite', database=os.path.expanduser('~/Documents/Gestione Concessionaria/db.db'))
query = open("tables.sql")
db.connection.executescript(query.read())
query.close()


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
btn.grid(row=0, column=0, padx=10)  # Impacchettamento pulsante (alla finestra)

settings_image = PhotoImage(file="img/settings.png")
btn_settings = Button(bf, text="Impostazioni".upper(), compound=LEFT, image=settings_image,
                      command=lambda: Impostazioni(db, s))
btn_settings.grid(row=0, column=1, padx=10)

# ===== IMPOSTAZIONE STILE ===== #
s = Style(db, tk)

tk.mainloop()  # Inizio ciclo eventi
db.close()  # Chiusura database
