import tkinter.messagebox as tkmb
from tkinter import *
from tkinter.ttk import *

from lib import wckToolTips
from src.Veicolo import Veicolo
from src.common import import_pil

import_pil('')
import PIL.Image
import PIL.ImageTk


class VisualizzaVeicolo:
    def __init__(self, veicolo, db, style):
        """
           Visualizza nel dettaglio il veicolo. È possibile anche aumentare e diminuire le quantità disponibili.

           :param Veicolo veicolo:
           :return:
           """
        self.__veicolo = veicolo
        self.__db = db
        self.__style = style
        f = Toplevel()
        f.title("Info Veicolo")
        f.iconphoto(True, PhotoImage(file="img/icon.png"))
        self.__root = f
        self.__style.change_window_bg(f)
        fr = Frame(f)
        fr.pack()
        if veicolo.foto:
            imm = self.scale_image(veicolo.foto, 250)
        else:
            imm = self.scale_image("img/no_image.png", 250)
        etc1 = Label(fr, image=imm)
        etc2 = Label(fr, text="Questo veicolo, della marca {}, possiede {} cavalli. Il nome del modello è {} ed è "
                              "stata costruita nel {}.\nLa categoria a cui questo veicolo appartiene è {}. Il prezzo "
                              "della vettura è {} mentre in concessionaria sono disponibili {} "
                              "esemplare/i ".format(veicolo.marca_name,
                                                    veicolo.cavalli,
                                                    veicolo.modello,
                                                    veicolo.anno_costruzione,
                                                    veicolo.categoria,
                                                    veicolo.prezzo,
                                                    veicolo.qta))
        etc1.grid(row=1, column=1)
        etc2.grid(row=1, column=3)

        iedit = PhotoImage(file="img/edit.png")
        puls = Button(fr, text="Modifica veicolo", image=iedit, compound=LEFT, command=self.modificaVeicolo).grid(
            row=6, column=8)
        quant = Label(fr, text="{}".format(self.__veicolo.qta))
        self.__quant = quant
        piu = Button(fr, text="+", command=self.aumenta)
        piu.grid(row=4, column=0)
        meno = Button(fr, text="-", command=self.diminuisci)
        meno.grid(row=4, column=2)
        quant.grid(row=4, column=1)
        f.mainloop()

    def aumenta(self):
        self.__veicolo.qta += 1
        self.__veicolo.save()
        self.__quant.configure(text=self.__veicolo.qta)

    def diminuisci(self):
        if self.__veicolo.qta != 0:
            self.__veicolo.qta -= 1
            self.__veicolo.save()
            self.__quant.configure(text=self.__veicolo.qta)
        else:
            pass

    def modificaVeicolo(self):
        w = Toplevel()
        w.title("Modifica veicolo")
        w.iconphoto(True, PhotoImage(file="img/icon.png"))
        self.__style.change_window_bg(w)
        self.__edit_window = w
        # Creo l'etichetta e il pulsante SALVA finale prima
        save = PhotoImage(file="img/save.png")
        btn_salva = Button(w, text="Salva", image=save, compound=LEFT, state=DISABLED, command=self.salva)
        t = wckToolTips.register(btn_salva, "Il pulsante si attiverà quando saranno compilati i campi Modello e "
                                            "Categoria")
        data = ['serie', 'modello', 'cavalli', 'anno_costruzione', 'categoria', 'prezzo']
        f = Frame(w)
        f.pack()
        r = 0
        for i in data:
            e = Label(f, text="{}: ".format(i).capitalize())
            e.grid(row=r, column=0, padx=10, pady=10)
            if type(getattr(self.__veicolo, i)) == "int":
                var = IntVar(value=getattr(self.__veicolo, i, IntVar(value="")))
            elif type(getattr(self.__veicolo, i)) == "float":
                var = DoubleVar(value=getattr(self.__veicolo, i, DoubleVar(value="")))
            else:
                var = StringVar(value=getattr(self.__veicolo, i, StringVar(value="")))
            setattr(self.__veicolo, i, var)
            if i == "categoria":
                cas = Combobox(f, textvariable=getattr(self.__veicolo, i),
                               values=sorted(["Autoveicolo", "Motociclo", "Ciclomotore", "Rimorchio",
                                              "Semirimorchio"]) + ['Altro'])
            else:
                cas = Entry(f, textvariable=getattr(self.__veicolo, i))
            getattr(self.__veicolo, i).trace('w', lambda i, v, o: self.__button_state(t, btn_salva))

            # setattr(self, "add_{}".format(i), cas)
            cas.grid(row=r, column=1, padx=10, pady=10)
            r += 1
        self.__button_state(t, btn_salva)
        btn_salva.pack(pady=10)
        w.mainloop()
        del self.__edit_window

    def __button_state(self, t, btn):
        if not (self.__veicolo.modello.get() and self.__veicolo.categoria.get()):
            wckToolTips.register(btn,
                                 "Il pulsante si attiverà quando saranno compilati i campi Modello e Categoria")
            btn.configure(state=DISABLED)
        else:
            try:
                wckToolTips.unregister(btn)
            except ValueError:
                pass
            btn.configure(state=ACTIVE)

    def salva(self):
        for i in self.__veicolo.get_attributes(only_table_columns=True).keys():
            if i in ["marca", "qta"]:
                continue
            setattr(self.__veicolo, i, getattr(self.__veicolo, i).get())
        self.__veicolo.save()
        tkmb.showinfo(parent=self.__edit_window, title="Veicolo modificato correttamente",
                      message="Il veicolo è stato modificato correttamente!")
        self.__edit_window.destroy()
        self.__root.destroy()
        VisualizzaVeicolo(self.__veicolo, self.__db, self.__style)

    def scale_image(self, path, basewidth):
        """
        Ridimensiona l'immagine passata come parametro ad una larghezza definita (secondo parametro) ed altezza
        variabile, scalata in base a quella vecchia e alla larghezza desiderata

        :param path str
        :param basewidth int
        :return:
        """
        img = PIL.Image.open(path)
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        photo = PIL.ImageTk.PhotoImage(img)
        return photo
