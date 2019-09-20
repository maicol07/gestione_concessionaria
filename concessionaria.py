# Import tkinter, ttk e sqlite3
from tkinter import *
from tkinter.ttk import *
import sqlite3 as sql

# Apertura database (viene creato se non esiste il file) e creazione tabelle se non esistono già
db = sql.connect("db.db", isolation_level=None)
query = open("tables.sql")
db.executescript(query.read())


# Maicol
def visualizzaMarca(marca):
    pass


# Ale
def selettoreMarche():
    w = Toplevel()
    w.title("Gestione Concessionaria")
    f = Frame(w)
    f.pack()

    w.mainloop()


# Massa
def visualizzaVeicolo(veicolo):
    pass
    f = Toplevel()
    f.title("Info Veicolo")
    fr = Frame(f)

    f.mainloop()


### MAIN (Finestra principale)
tk = Tk()
# Impostazione titolo
tk.title("Gestione Concessionaria")
# Creazione variabile immagine
logo = PhotoImage(file="logo.png")
# Creazione etichetta immagine
l = Label(tk, image=logo)
# Impacchettamento etichetta (alla finestra)
l.pack()
# Creazione pulsante
btn = Button(tk, text="VAI AL SELETTORE DELLE MARCHE", command=selettoreMarche)
# Impacchettamento pulsante (alla finestra)
btn.pack(pady=20)
# Inizio ciclo eventi
tk.mainloop()