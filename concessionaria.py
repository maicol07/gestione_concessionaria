from tkinter import *
from tkinter.ttk import *
import sqlite3 as sql

# Maicol
def visualizzaMarca(marca):
    pass

# Ale
def selettoreMarche():
    pass

# Massa
def visualizzaVeicolo(veicolo):
    pass
tk = Tk()
tk.title("Gestione Concessionaria")
logo = PhotoImage(file="logo.png")
l = Label(tk, image=logo)
l.pack()
btn = Button(tk, text="VAI AL SELETTORE DELLE MARCHE")
btn.pack(pady=10)
tk.mainloop()