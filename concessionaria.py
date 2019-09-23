# Import tkinter, ttk e sqlite3
import sqlite3 as sql
from tkinter import *
from tkinter.ttk import *

# Apertura database (viene creato se non esiste il file) e creazione tabelle se non esistono già
db = sql.connect("db.db", isolation_level=None)
query = open("tables.sql")
db.executescript(query.read())
c = db.cursor()


# Maicol
def visualizzaMarca(marca):
    pass


# Ale
def selettoreMarche():
    w = Toplevel()
    w.title("Gestione Concessionaria")
    f = Frame(w)
    f.pack()
    c.execute("SELECT * FROM marche")
    marche = c.fetchall()
    for marca in marche:
        var = PhotoImage(file=marca[2])
        btn = Button(f, text=marca[1], image=var, compound=TOP)
    w.mainloop()


# Massa
def visualizzaVeicolo(veicolo):
    pass
    f = Toplevel()
    f.title("Info Veicolo")
    fr = Frame(f)
    fr.pack()
    c.execute("SELECT * FROM veicoli WHERE id=?", (veicolo))

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