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
        print(self.id)
        res = self.__db.select("veicoli", where={"id": self.id}).first()
        for key in res.keys():
            if not (key in columns):
                continue
            if key == "marca":
                name = self.__db.get("marche", "nome", where={"id": res[key]})
                setattr(self, "marca", res[key])
                setattr(self, "marca_name", name)
                continue
            setattr(self, key, res[key])

    def save(self):
        attributes = self.get_attributes(only_table_columns=True)
        if hasattr(self, "id"):
            self.__db.update(self.__table, attributes, where={"id": self.id})
        else:
            self.__db.insert(self.__table, attributes)

    def get_attributes(self, only_table_columns=False):
        attributes = vars(self).copy()
        for i in list(attributes.keys()):
            if "_Veicolo" in i:
                del attributes[i]
        if only_table_columns:
            columns = ['marca', 'serie', 'modello', 'cavalli', 'anno_costruzione', 'categoria', 'prezzo', 'qta']
            for i in list(attributes.keys()):
                if i not in columns:
                    del attributes[i]
        return attributes

    def __del__(self):
        if hasattr(self, "id"):
            self.__db.delete(self.__table, where={"id": self.id})
