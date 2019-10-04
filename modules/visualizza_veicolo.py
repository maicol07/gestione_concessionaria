from tkinter import *
from tkinter.ttk import *

from src import Veicolo


class visualizzaVeicolo:
    def __init__(self, veicolo):
        """
           Visualizza nel dettaglio il veicolo. È possibile anche aumentare e diminuire le quantità disponibili.

           :param Veicolo veicolo:
           :return:
           """
        self.veicolo=veicolo
        f = Toplevel()
        f.title("Info Veicolo")
        f.iconphoto(True, PhotoImage(file="img/icon.png"))
        fr = Frame(f)
        fr.pack()
        imm = veicolo.foto
        etc1 = Label(f, image=imm)
        etc2 = Label(f, text="Questo veicolo, della marca {}, possiede {} cavalli. Il nome del modello è {} ed è stata "
                             "costruita nel {}. La categoria a cui questo veicolo appartiene è {}. Il prezzo della vettura"
                             " è {} mentre in concessionaria sono disponibili {} esemplare/i ".format(veicolo.marca,
                                                                                                      veicolo.cavalli,
                                                                                                      veicolo.modello,
                                                                                                      veicolo.anno_costruzione,
                                                                                                      veicolo.categoria,
                                                                                                      veicolo.prezzo,
                                                                                                      veicolo.qta)
        etc1.grid(row=1, column=1)
        etc2.grid(row=1, column=3)

        puls = Button(f, text="Modifica veicolo", command=self.modificaVeicolo)).grid(row=6, column=8)
        piu = Button(f, text="+", command=self.aumenta).grid(row=4,column=1)
        meno= Button(f, text="-", command=self.diminuisci).grid(row=4,column=3)
        quant=Label(f,text="{}".format(self.veicolo.qta)).grid(row=4, column=2)
        f.mainloop()

    def aumenta(self):
        self.veicolo.qta=self.veicolo.qta+1
        self. veicolo.save()
    def diminuisci (self):
        if self.veicolo.qta !=0:
            self.veicolo.qta=self.veicolo.qta-1
            self.veicolo.save()
        else:
            pass
    def modificaVeicolo(self):
        g = Toplevel()
        g.title("Modifica veicolo")
        g.iconphoto(True, PhotoImage(file="img/icon.png"))
        fr = Frame(g)
        fr.pack()

        for i in vars(self.veicolo).keys():
            etic = Label(g, text="Immetti {}: ".format(i))
            self.i = StringVar(value=self.veicolo.i)
            ent = Entry(g, textvariable=self.i)

        foto=PhotoImage(file="img/save.png")
        sal= Button(g, text="Salva", image=foto, compound=LEFT, command=self.salva).pack()

    def salva (self):
        for i in vars(self.veicolo).keys():
            self.veicolo.i=self.i
        self.veicolo.save()
