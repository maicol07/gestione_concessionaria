# ========== LIBRERIE INTERNE ========== #
import tkinter.messagebox as tkmb
from io import BytesIO
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *

import src.Style
from src.common import import_pil

# ===== IMPORT PIL ===== #
import_pil('')
import PIL.Image
import PIL.ImageTk
from modules.listaveicoli import ListaVeicoli


class SelettoreMarche:
    def __init__(self, db):
        """
            Permette all'utente di selezionare una marca
           """
        self.__db = db
        w = Toplevel()
        self.__root = w
        w.title("Seleziona marca")
        w.iconphoto(True, PhotoImage(file="img/icon.png"))
        src.Style.s.change_window_bg(w)
        f = Frame(w)
        f.pack()
        self.__image=""
        marche = db.select("marche")  # seleziona tutto dalla tabella marche, ritorna un oggetto
        contr = 0  # contatore righe
        contc = 0  # contatore colonne
        for marca in marche:
            var = self.scale_image(marca.logo, 50)  # ottengo l'oggetto " logo" (il percorso del logo)
            btn = Button(f, text=marca.nome, image=var, compound=TOP, command=lambda: ListaVeicoli(marca.id, self.__db))
            btn.grid(row=contr, column=contc)
            contc += 1
            if contc == 2:
                contr += 1
        vari = PhotoImage(file="img/add.png")
        f1 = Frame(w)
        f1.pack()
        btn = Button(f1, text="Aggiungi", image=vari, compound=LEFT, command=lambda: self.aggiungi())
        btn.grid(row=0, column=0)
        vari1 = PhotoImage(file="img/delete.png")
        btn2 = Button(f1, text="Elimina", image=vari1, compound=LEFT,command= lambda :self.schermataElimina())
        btn2.grid(row=0, column=1)
        w.mainloop()

    def aggiungi(self):
        w = Toplevel()
        w.title("Aggiungi marca")
        w.iconphoto(True, PhotoImage(file="img/icon.png"))

        f = Frame(w)
        f.pack()
        e = Label(f, text="Marca")
        e.grid(row=0, column=0)
        s = StringVar()
        ctext = Entry(f, textvariable=s)
        ctext.grid(row=0, column=1)
        f2 = Frame(w)
        f2.pack()
        simm = Label(f2, text="Immagine")
        immagine = PhotoImage(file="img/pick_file.png")
        btn = Button(f2, text="Seleziona immagine", image=immagine, compound=LEFT,
                     command=lambda: self.selImmagine(btn, w))
        immagine2 = PhotoImage(file="img/save.png")
        btns = Button(w, text="Salva", image=immagine2, compound=LEFT,
                      command=lambda: self.Salva(ctext.get(), self.__image, w))
        btn.grid(row=0, column=1)
        btns.pack()
        simm.grid(row=0, column=0)
        w.mainloop()

    def selImmagine(self, bi, window):
        """
            Apre il file picker per selezionare una immagine

            Parametri
            ----------
            :param Button bi : (Tkinter Button)
                Pulsante Immagine Tkinter
            :param window : (string)
                Stringa che riporta il nome della finestra.

            Ritorna
            -------
            Niente
            """
        fImage = askopenfilename(
            filetypes=[
                ("File Immagini", "*.jpg *.jpeg *.png *.bmp *.gif *.psd *.tif *.tiff *.xbm *.xpm *.pgm *.ppm")])
        if not (fImage == ""):
            self.__image = fImage
            bi["text"] = ""
        else:
            bi["text"] = "Seleziona immagine"
            return
        img = self.scale_image(fImage, 100)
        bi["image"] = img
        bi.image = img
        window.focus()

    def Salva(self, nome, immagine, wadd):
        if nome=="":
            tkmb.showerror(parent=wadd, title="Errore",
            message="Non è stato  inserito il nome della marca!")
        self.__db.insert("marche", "nome, logo", (nome, immagine))
        tkmb.showinfo(title="Marca aggiunta con successo!",
                      message="La marca è stata aggiunta con successo!")
        wadd.destroy() #elimina la scermata "Aggiungi"
        self.__root.destroy() #elimina la finestra iniziale
        SelettoreMarche(self.__db) #ricrea la finestra iniziale con gli elementi aggiunti

    def scale_image(self, path, basewidth):
        """
        Ridimensiona l'immagine passata come parametro ad una larghezza definita (secondo parametro) ed altezza
        variabile, scalata in base a quella vecchia e alla larghezza desiderata

        :param path str
        :param basewidth int
        :return:
        """
        try:
            data=path.decode
            img=PIL.Image.open(BytesIO(path))
        except (UnicodeDecodeError, AttributeError):
            img = PIL.Image.open(path)
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        photo = PIL.ImageTk.PhotoImage(img)
        return photo

    def schermataElimina(self):
        w = Toplevel()
        w.title("Elimina marca")
        w.iconphoto(True, PhotoImage(file="img/icon.png"))
        f = Frame(w)
        f.pack()
        s = StringVar()
        nmarche=self.__db.select("marche")
        diz={}
        for i in nmarche:
            diz[i.id]=i.nome
        ctext = Combobox(f, textvariable=s, values=list(diz.values())) #crea il menù a tendina
        ctext.grid(row=0, column=1)
        vari1 = PhotoImage(file="img/delete.png")
        btn = Button(f, text="Elimina", image=vari1, compound=LEFT, command=lambda: self.elimina(ctext.get(),diz,w))
        btn.grid(row=0, column=2)
        w.mainloop()

    def elimina(self, nome, marche, w):
        values=list(marche.values())
        n=values.index(nome)
        keys=list(marche.keys())
        self.__db.delete("marche", where={"id":keys[n]})
        tkmb.showinfo(parent=w, title="Info", message="La marca è stata elliminata con successo")
        w.destroy()
        self.__root.destroy()
        SelettoreMarche(self.__db)
