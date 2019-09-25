# Import tkinter, ttk e Medoo (helper sqlite3)
from tkinter import *
from tkinter.ttk import *

try:
    import medoo
except ImportError:
    from lib import medoo
# Import classi Veicolo

# Apertura database (viene creato se non esiste il file) e creazione tabelle se non esistono già
db = medoo.Medoo('sqlite', 'db.db')
query = open("tables.sql")
db.cursor.executescript(query.read())


# Maicol
def listaVeicoli(marca):
    """
    Mostra all'utente una lista di veicoli di una determinata marca tra cui scegliere

    :param marca:
    :return:
    """
    pass


# Ale
def selettoreMarche():
    """
    Permette all'utente di selezionare una marca
    """
    w = Toplevel()
    w.title("Seleziona marca")
    w.iconbitmap("img/icon.ico")
    f = Frame(w)
    f.pack()
    marche = db.select("marche")
    for marca in marche:
        var = PhotoImage(file=marca.logo)
        btn = Button(f, text=marca.name, image=var, compound=TOP)
    w.mainloop()


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


### MAIN (Finestra principale)
tk = Tk()
# Impostazione titolo
tk.title("Gestione Concessionaria")
# Impostazione icona
tk.iconbitmap("img/icon.ico")
# Creazione variabile immagine
logo = PhotoImage(file="img/logo.png")
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
# Chiusura database
db.close()
