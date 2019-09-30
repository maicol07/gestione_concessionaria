# ========== LIBRERIE INTERNE ========== #
import os
import platform
import sys
import tkinter.messagebox as tkmb
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *

import src.Style

# ===== IMPORT PIL ===== #
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
    sys.path.insert(0,
                    os.path.abspath("../lib/PIL/Pillow-6.1.0-py{}.{}-{}.egg".format(py_version.major, py_version.minor,
                                                                                    os_info)))

import PIL.Image
import PIL.ImageTk

class SelettoreMarche:
    def __init__(self, db):
        """
            Permette all'utente di selezionare una marca
           """
        self.__db=db
        w = Toplevel()
        w.title("Seleziona marca")
        w.iconphoto(True, PhotoImage(file="img/icon.png"))
        src.Style.s.change_window_bg(w)
        f = Frame(w)
        f.pack()
        marche = db.select("marche")  # seleziona tutto dalla tabella marche, ritorna un oggetto
        contr=0  # contatore righe
        contc=0  # contatore colonne
        for marca in marche:
            var = PhotoImage(file=marca.logo)  # ottengo l'oggetto " logo" (il percorso del logo)
            btn = Button(f, text=marca.name, image=var, compound=TOP)
            btn.grid(row=contr, column=contc)
            contc+=1
            if contc==2:
                contr+=1
        vari= PhotoImage(file="img/add.png")
        f1 = Frame(w)
        f1.pack()
        btn= Button(f1, text="Aggiungi", image=vari, compound=LEFT, command=lambda:self.aggiungi())
        btn.grid(row=0, column=0)
        vari1= PhotoImage(file="img/delete.png")
        btn2= Button(f1, text="Elimina", image=vari1, compound=LEFT)
        btn2.grid(row=0, column=1)
        w.mainloop()

    def aggiungi(self):
        w = Toplevel()
        w.title("Aggiungi marca")
        w.iconphoto(True, PhotoImage(file="img/icon.png"))

        f= Frame(w)
        f.pack()
        e=Label(f, text="Marca")
        e.grid(row=0, column=0)
        s = StringVar()
        ctext= Entry(f, textvariable=s)
        ctext.grid(row=0, column=1 )
        f2=Frame(w)
        f2.pack()
        simm=Label(f2,text="Immagine")
        immagine=PhotoImage(file="img/pick_file.png")
        btn = Button(f2, text="Seleziona immagine", image=immagine, compound=LEFT,
                     command=lambda: self.selImmagine(btn, w))
        immagine2=PhotoImage(file="img/save.png")
        btns = Button(w, text="Salva", image=immagine2, compound=LEFT)  # NON DIMENTICARE DI FINIRE LAMBDA
        btn.grid(row=0, column=1)
        btns.pack()
        simm.grid(row=0, column=0)
        w.mainloop()

    def selImmagine(self, bi, window):
        """
            Apre il file picker per selezionare una immagine

            Parametri
            ----------
            :param bi : (Tkinter Button)
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
            bi["text"] = ""
        else:
            bi["text"] = "Seleziona immagine"
            return
        img = PIL.Image.open(fImage)
        # Ridimensionamento immagine a 100 px per larghezza, altezza variabile e scalata in base a quella vecchia e alla
        # larghezza di 100 px
        basewidth = 100
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        photo = PIL.ImageTk.PhotoImage(img)
        bi["image"] = photo
        bi.image = photo
        window.focus()

    def Salva(self, nome, immagine):
        self.__db.insert("marche", "nome, logo",(nome, immagine))
