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
            self.__id = id
            self.__find()

    def __find(self):
        res = self.__db.select(self.__table, where={"id": self.__id})
        for key in dir(res):
            if key == "marca":
                setattr(self, "marca", self.__db.get("marche", "nome", where={"id": res.key}))
                setattr(self, "__marca_id", res.key)
                continue
            setattr(self, key, res.key)
        self.__id = id

    def save(self):
        attributes = vars(self).copy()
        for i in list(attributes.keys()):
            if "_Veicolo" in i:
                del attributes[i]
        if hasattr(self, "__id"):
            self.__db.update(self.__table, attributes, where={"id": self.__id})
        else:
            self.__db.insert(self.__table, attributes)

    def __del__(self):
        if hasattr(self, "__id"):
            self.__db.delete(self.__table, where={"id": self.__id})
