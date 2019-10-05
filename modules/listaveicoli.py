import tkinter.messagebox as tkmb
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *

import lib.wckToolTips
import src.Style
from lib.medoo.database.sqlite import Sqlite
from modules.visualizza_veicolo import VisualizzaVeicolo
from src.Veicolo import Veicolo
from src.common import import_pil

import_pil()
import PIL.Image
import PIL.ImageTk


class ListaVeicoli:
    __veicolo = None  # Oggetto del veicolo creato con la funzione add

    def __init__(self, marca, db):
        """
        Mostra all'utente una lista di veicoli di una determinata marca tra cui scegliere

        :param marca:
        :param Sqlite db:
        :return:
        """
        w = Toplevel()
        w.iconphoto(True, PhotoImage(file="img/icon.png"))
        self.__root = w
        self.__style = src.Style.s
        self.__db = db
        self.__marca = marca
        self.__marca_name = self.__db.get("marche", "nome", where={"id": self.__marca})
        w.title("Lista veicoli {}".format(self.__marca_name))
        self.__style.change_window_bg(w)

        fw = Frame(w)
        fw.pack()
        # ===== FILTRO ===== #
        f = Labelframe(fw, text="Filtra")
        f.grid(row=0, column=0, pady=10)
        self.__SEARCH = StringVar()
        self.__SEARCH.trace('w', lambda i, o, v: self.search())
        search = Entry(f, textvariable=self.__SEARCH)
        search.grid(row=0, column=0, padx=10, pady=5)
        filter_icon = PhotoImage(file="img/search.png")
        btn_filter = Button(f, text="Filtra", compound=LEFT, image=filter_icon, command=self.search)
        btn_filter.grid(row=0, column=1, padx=10, pady=5)
        reset_icon = PhotoImage(file="img/restore.png")
        btn_reset = Button(f, text="Reset", compound=LEFT, image=reset_icon, command=self.reset)
        btn_reset.grid(row=0, column=2, padx=10, pady=5)

        # ===== TREEVIEW ===== #
        ft = Frame(w, height=500)
        ft.pack(padx=10)
        scrollbarx = Scrollbar(ft, orient=HORIZONTAL)
        scrollbary = Scrollbar(ft, orient=VERTICAL)
        self.__tree = Treeview(ft, columns=("marca", "serie", "modello", "cv", "anno_costruzione", "categoria",
                                            "prezzo", "qta"),
                               selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=self.__tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=self.__tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        self.__tree.heading('#0', text="ID", anchor=W)
        self.__tree.heading('marca', text="Marca", anchor=W)
        self.__tree.heading('serie', text="Serie", anchor=W)
        self.__tree.heading('modello', text="Modello", anchor=W)
        self.__tree.heading('cv', text="Cavalli", anchor=W)
        self.__tree.heading('anno_costruzione', text="Anno di costr.", anchor=W)
        self.__tree.heading('categoria', text="Categoria", anchor=W)
        self.__tree.heading('prezzo', text="Prezzo (mila €)", anchor=W)
        self.__tree.heading('qta', text="Quantità disp.", anchor=W)
        self.__tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.__tree.column('marca', stretch=NO, minwidth=0, width=80)
        self.__tree.column('serie', stretch=NO, minwidth=0, width=80)
        self.__tree.column('modello', stretch=NO, minwidth=0, width=120)
        self.__tree.column('cv', stretch=NO, minwidth=0, width=50)
        self.__tree.column('anno_costruzione', stretch=NO, minwidth=0, width=100)
        self.__tree.column('categoria', stretch=NO, minwidth=0, width=120)
        self.__tree.column('prezzo', stretch=NO, minwidth=0, width=100)
        self.__tree.column('qta', stretch=NO, minwidth=0, width=80)
        self.__tree.pack()
        self.__tree.bind("<Button-3>", self.actions)
        self.__id_list = self.__db.select("veicoli", "id", where={"marca": self.__marca}).all()
        self.__tree.bind("<Double-Button-1>", lambda e: self.visualizza_veicolo())
        for veicolo in self.__id_list:
            v = Veicolo(self.__db, veicolo.id)
            valori = v.get_attributes(only_table_columns=True)
            valori['marca'] = self.__marca_name
            self.__tree.insert('', 'end', text=v.id, values=list(valori.values()))
        li = Label(w, text="Per aggiungere un veicolo, usa il tasto destro del mouse su uno spazio vuoto della "
                           "finestra.\nPer modificare un veicolo, fai doppio click sulla riga corrispondente e poi "
                           "premi il pulsante Modifica in alto a destra.\n"
                           "Per eliminare un veicolo, selezionare una riga e poi premere il tasto destro del mouse.")
        li.pack(pady=10)
        w.bind("<Button-3>", self.actions_add)

        # ===== MODIFICA MARCA ===== #
        iedit = PhotoImage(file="img/edit.png")
        btn_edit = Button(fw, text="Modifica marca", image=iedit, compound=LEFT, command=self.modifica_marca)
        btn_edit.grid(row=0, column=1, padx=20)
        w.mainloop()

    def search(self):
        """
        Gestisce il filtraggio dei veicoli di una determinata marca in base a quello scritto dall'utente

        :return:
        """
        if self.__SEARCH.get() != "":
            self.__tree.delete(*self.__tree.get_children())
            for veicolo in self.__id_list:
                v = Veicolo(self.__db, veicolo.id)
                if self.__SEARCH.get() not in v.modello:
                    continue
                valori = v.get_attributes(only_table_columns=True)
                valori['marca'] = self.__marca_name
                self.__tree.insert('', 'end', text=v.id, values=list(valori.values()))

    def reset(self):
        """
        Resetta le opzioni di filtraggio della tabella. Vengono visualizzati tutti i veicoli di una determinata marca

        :return:
        """
        self.__tree.delete(*self.__tree.get_children())
        for veicolo in self.__id_list:
            v = Veicolo(self.__db, veicolo.id)
            valori = v.get_attributes(only_table_columns=True)
            valori['marca'] = self.__marca_name
            self.__tree.insert('', 'end', text=v.id, values=list(valori.values()))

    def actions(self, event):
        """
        Mostra un menu di opzioni quando viene cliccata una riga della tabella con il tasto destro.

        :param event : (treeview callback)
            Parametro che identifica l'evento del cliccare con il tasto destro una voce dalla tabella.
        :return:
        """
        if event.widget != self.__tree:
            return
        # display the popup menu
        try:
            if not hasattr(self, "__tree_menu"):
                self.__tree_menu = Menu(self.__root, tearoff=0)
                iadd = PhotoImage(file="img/add.png")
                self.__tree_menu.add_command(label='Aggiungi', image=iadd, compound="left",
                                             command=self.add)
                idel = PhotoImage(file="img/delete.png")
                self.__tree_menu.add_command(label='Elimina', image=idel, compound="left",
                                             command=self.delete)
            self.__tree_menu.tk_popup(event.x_root + 53, event.y_root, 0)
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            self.__tree_menu.grab_release()

    def actions_add(self, event):
        """
            Mostra un menu di opzioni (solo aggiunta) quando viene cliccato uno spazio vuoto della finestra con il
            tasto destro.

            :param event : (treeview callback)
                Parametro che identifica l'evento del cliccare con il tasto destro uno spazio vuoto della finestra.
            :return:
            """
        if event.widget != self.__root:
            return
        # display the popup menu
        try:
            if not hasattr(self, "__window_menu"):
                self.__window_menu = Menu(self.__root, tearoff=0)
                iadd = PhotoImage(file="img/add.png")
                self.__window_menu.add_command(label='Aggiungi', image=iadd, compound="left",
                                               command=self.add)
            self.__window_menu.tk_popup(event.x_root + 53, event.y_root, 0)
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            self.__window_menu.grab_release()

    def add(self):
        w = Toplevel()
        w.title("Aggiungi veicolo")
        w.iconphoto(True, PhotoImage(file="img/icon.png"))
        self.__style.change_window_bg(w)
        self.__add_window = w
        self.__veicolo = Veicolo(self.__db)
        setattr(self.__veicolo, "marca", self.__marca)
        # Creo l'etichetta e il pulsante SALVA finale prima
        save = PhotoImage(file="img/save.png")
        btn_salva = Button(w, text="Salva", image=save, compound=LEFT, state=DISABLED, command=self.salva)
        t = lib.wckToolTips.register(btn_salva, "Il pulsante si attiverà quando saranno compilati i campi Modello e "
                                                "Categoria")
        data = ['serie', 'modello', 'cavalli', 'anno_costruzione', 'categoria', 'prezzo', 'qta']
        f = Frame(w)
        f.pack()
        r = 0
        for i in data:
            e = Label(f, text="{}: ".format(i).capitalize())
            e.grid(row=r, column=0, padx=10, pady=10)
            setattr(self.__veicolo, i, StringVar(value=""))
            if i == "categoria":
                cas = Combobox(f, textvariable=getattr(self.__veicolo, i), values=sorted(["Autoveicolo", "Motociclo",
                                                                                          "Ciclomotore", "Rimorchio",
                                                                                          "Semirimorchio"]) + ['Altro'])
            else:
                cas = Entry(f, textvariable=getattr(self.__veicolo, i))
            getattr(self.__veicolo, i).trace('w', lambda i, v, o: self.__button_state(t, btn_salva))
            cas.grid(row=r, column=1, padx=10, pady=10)
            r += 1
        f2 = Frame(w)
        f2.pack()
        simm = Label(f2, text="Immagine")
        simm.grid(row=0, column=0, padx=10, pady=10)
        immagine = PhotoImage(file="img/pick_file.png")
        self.__image = ''
        btn = Button(f2, text="Seleziona immagine", image=immagine, compound=LEFT,
                     command=lambda: self.selImmagine(btn, w))
        btn.grid(row=0, column=0, padx=10, pady=10)
        btn_salva.pack(pady=10)
        w.mainloop()
        del self.__add_window

    def selImmagine(self, bi, window):
        """
        Apre il file picker per selezionare una immagine

        :param Button bi : (Tkinter Button)
            Pulsante Immagine Tkinter
        :param window : (string)
            Stringa che riporta il nome della finestra.
        :return:
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

    def __button_state(self, t, btn):
        if not (self.__veicolo.modello.get() and self.__veicolo.categoria.get()):
            lib.wckToolTips.register(btn,
                                     "Il pulsante si attiverà quando saranno compilati i campi Modello e Categoria")
            btn.configure(state=DISABLED)
        else:
            try:
                lib.wckToolTips.unregister(btn)
            except ValueError:
                return
            btn.configure(state=ACTIVE)

    def salva(self):
        for i in self.__veicolo.get_attributes(only_table_columns=True).keys():
            if i in ["marca"]:
                continue
            setattr(self.__veicolo, i, getattr(self.__veicolo, i).get())
        setattr(self.__veicolo, 'foto', self.__image)
        self.__veicolo.save()
        tkmb.showinfo(parent=self.__add_window, title="Veicolo aggiunto correttamente",
                      message="Il veicolo è stato aggiunto correttamente!")
        self.__add_window.destroy()
        self.__root.destroy()
        ListaVeicoli(self.__marca, self.__db)

    def delete(self):
        """
        Avvisa l'utente che si sta per rimuovere un veicolo. Se l'utente risponde positivamente, allora verrà effettuata
        l'eliminazione; l'azione verrà annullata altrimenti.

        :return:
        """
        vehicles = self.__tree.selection()
        if len(vehicles) == 0:
            tkmb.showwarning(parent=self.__root, title="Nessun veicolo selezionato!",
                             message="Non è stato selezionato nessun veicolo. Si prega di selezionarne uno per "
                                     "apportare modifiche.")
            return

        scelta = tkmb.askyesno(parent=self.__root, title="Conferma eliminazione",
                               message="Si è sicuri di voler eliminare i veicoli selezionati?")
        for i in vehicles:
            vehicle = self.__tree.item(self.__tree.focus())
            if scelta is True:
                v = Veicolo(self.__db, vehicle['text'])
                del v
                tkmb.showinfo(parent=self.__root, title="Veicolo eliminato correttamente!",
                              message="Il veicolo è stato eliminato correttamente")
                self.__root.destroy()
                ListaVeicoli(self.__marca, self.__db)
            else:
                return

    def visualizza_veicolo(self):
        selected = self.__tree.item(self.__tree.focus())
        if selected["text"] == "":
            tkmb.showwarning(title="Nessun veicolo selezionato!",
                             message="Non è stato selezionato nessun veicolo. Si prega di selezionarne uno per "
                                     "apportare modifiche.")
            return
        VisualizzaVeicolo(Veicolo(self.__db, selected['text']), self.__db, self.__style)

    def modifica_marca(self):
        w = Toplevel()
        w.title("Modifica marca {}".format(self.__marca_name))
        w.iconphoto(True, PhotoImage(file="img/icon.png"))
        self.__style.change_window_bg(w)

        f = Frame(w)
        f.pack()
        e = Label(f, text="Marca")
        e.grid(row=0, column=0, padx=10, pady=10)
        s = StringVar(value=self.__marca_name)
        ctext = Entry(f, textvariable=s)
        ctext.grid(row=0, column=1, padx=10, pady=10)
        f2 = Frame(w)
        f2.pack()
        simm = Label(f2, text="Immagine")
        simm.grid(row=0, column=0, padx=10, pady=10)
        imm = self.__db.get("marche", "logo", where={"id": self.__marca})
        if imm:
            immagine = self.scale_image(imm, 100)
            compound = TOP
            text = ''
        else:
            immagine = PhotoImage(file="img/pick_file.png")
            compound = LEFT
            text = 'Seleziona immagine'
        btn = Button(f2, text=text, image=immagine, compound=compound,
                     command=lambda: self.selImmagine(btn, w))
        immagine2 = PhotoImage(file="img/save.png")
        btns = Button(w, text="Salva", image=immagine2, compound=LEFT,
                      command=lambda: self.salva_marca(ctext.get(), self.__image, w))
        btn.grid(row=0, column=1, padx=10, pady=10)
        btns.pack()
        simm.grid(row=0, column=0, padx=10, pady=10)
        w.mainloop()

    def salva_marca(self, nome, immagine, wadd):
        if nome == "":
            tkmb.showerror(parent=wadd, title="Errore",
                           message="Non è stato inserito il nome della marca!")
        self.__db.update("marche", {"nome": nome, "logo": immagine}, where={"id": self.__marca})
        tkmb.showinfo(title="Marca aggiunta con successo!",
                      message="La marca è stata aggiunta con successo!")
        wadd.destroy()  # elimina la scermata "Aggiungi"
