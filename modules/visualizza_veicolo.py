from io import BytesIO
from tkinter import *
from tkinter.ttk import *

from src.Veicolo import Veicolo
from src.common import import_pil

import_pil('')
import PIL.Image
import PIL.ImageTk


class VisualizzaVeicolo:
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
        self.__root = f
        fr = Frame(f)
        fr.pack()
        imm = self.scale_image(veicolo.foto, 250)
        etc1 = Label(f, image=imm)
        etc2 = Label(f, text="Questo veicolo, della marca {}, possiede {} cavalli. Il nome del modello è {} ed è stata "
                             "costruita nel {}. La categoria a cui questo veicolo appartiene è {}. Il prezzo della vettura"
                             " è {} mentre in concessionaria sono disponibili {} esemplare/i ".format(veicolo.marca,
                                                                                                      veicolo.cavalli,
                                                                                                      veicolo.modello,
                                                                                                      veicolo.anno_costruzione,
                                                                                                      veicolo.categoria,
                                                                                                      veicolo.prezzo,
                                                                                                      veicolo.qta))
        etc1.grid(row=1, column=1)
        etc2.grid(row=1, column=3)

        puls = Button(f, text="Modifica veicolo", command=self.modificaVeicolo).grid(row=6, column=8)
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

    def scale_image(self, path, basewidth):
        """
        Ridimensiona l'immagine passata come parametro ad una larghezza definita (secondo parametro) ed altezza
        variabile, scalata in base a quella vecchia e alla larghezza desiderata

        :param path str
        :param basewidth int
        :return:
        """
        try:
            data = path.decode
            img = PIL.Image.open(BytesIO(path))
        except (UnicodeDecodeError, AttributeError):
            img = PIL.Image.open(path)
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        photo = PIL.ImageTk.PhotoImage(img)
        return photo
