from lib.medoo.database.sqlite import Sqlite

class Veicolo:
    """
    Classe che gestisce un veicolo
    """
    __table = "veicoli"

    def __init__(self, db, id=None):
        """

        :param Sqlite db:
        :param id:
        """
        self.__db = db
        if id:
            self.id = id
            self.__find()

    def __find(self):
        columns = ['marca', 'serie', 'modello', 'cavalli', 'anno_costruzione', 'categoria', 'prezzo', 'qta', 'foto']
        self.__db.cursor.execute('SELECT "marca","serie","modello","cavalli","anno_costruzione","categoria","prezzo",'
                                 '"qta", "foto" FROM "veicoli" WHERE "id" = 4')
        res = self.__db.cursor.fetchall()[0]
        for pos, key in enumerate(columns):
            if not (key in columns):
                continue
            if key == "marca":
                setattr(self, "marca", self.__db.get("marche", "nome", where={"id": res[pos]}))
                setattr(self, "marca_id", res[pos])
                continue
            setattr(self, key, res[pos])

    def save(self):
        attributes = self.get_attributes()
        if hasattr(self, "__id"):
            self.__db.update(self.__table, attributes, where={"id": self.id})
        else:
            self.__db.insert(self.__table, attributes)

    def get_attributes(self):
        attributes = vars(self).copy()
        for i in list(attributes.keys()):
            if "_Veicolo" in i:
                del attributes[i]
        return attributes
        '''columns = ['marca', 'serie', 'modello', 'cavalli', 'anno_costruzione', 'categoria', 'prezzo', 'qta']
        d = {}
        for i in columns:
            d[i] = getattr(self, i)
        return d'''

    def __del__(self):
        if hasattr(self, "id"):
            self.__db.delete(self.__table, where={"id": self.id})
