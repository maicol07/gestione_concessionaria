from lib.ttkthemes import ThemedStyle


class Style:
    def __init__(self, db):
        """
        Inizializzazione dello stile Tkinter personalizzato (libreria ttkthemes)
        :param db:
        """
        self.style = ThemedStyle()
        self.color = self.style.lookup("TButton", "background", default="white")
        font = db.select("impostazioni", where={"setting": 'font'})
        if font:
            self.style.configure('.', font=font.value)
        theme = db.select("impostazioni", where={"setting": "theme"})
        if theme:
            self.theme_name = theme
            self.update_style(theme.value)

    def update_style(self, theme):
        """
        Cambia tema

        :param theme:
        :return:
        """
        self.style.set_theme(theme)
        self.color = self.style.lookup("TButton", "background", default="white")
        if self.color == "SystemButtonFace":
            self.color = "white"
        self.style.configure("TFrame", background=self.color)
        self.style.configure("TButton", height=100)
        self.style.configure("TLabel", background=self.color)
        self.style.configure("TPhotoimage", background=self.color)
        self.style.configure("TLabelframe", background=self.color)
        self.style.configure("TLabelframe.Label", background=self.color)
        self.style.configure("TScale", background=self.color)
        self.style.configure("TCheckbutton", background=self.color)

    def getThemesList(self):
        """
        Ritorna la lista dei temi disponibili
        :return:
        """
        return self.style.theme_names()

    def getCurrentThemeName(self):
        """
        Ritorna il nome del tema attualmente impostato
        :return:
        """
        return self.style.theme_use()
