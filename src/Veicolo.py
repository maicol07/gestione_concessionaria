from lib.medoo.database.sqlite import Sqlite

class Veicolo:
    """
    Classe che gestisce un veicolo
    """
    __table = "veicoli"

    def __init__(self, db, id):
        """

        :param Sqlite db:
        :param id:
        """
        self.__db = db
        self.__id = id
        self.__find()

    def __find(self):
        res = self.__db.select(self.__table, where={"id": 1})
        for key in dir(res):
            if key == "marca":
                setattr(self, "marca", self.__db.get("marche", "nome", where={"id": res.key}))
                setattr(self, "__marca_id", res.key)
                continue
            setattr(self, key, res.key)
        self.__id = id

    def save(self):
        self.__db.update(self.__table, vars(self), where={"id": self.__id})
