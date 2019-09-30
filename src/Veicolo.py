class Veicolo:
    """
    Classe che gestisce un veicolo
    """
    __table = "veicoli"

    def __init__(self, db, id):
        self.__db = db
        self.__id = id
        self.__find()

    def __find(self):
        res = self.__db.select(self.__table, where={"id": 1})
        for key in dir(res):
            setattr(self, key, res.key)
        self.__id = id

    def save(self):
        self.__db.update(self.__table, vars(self), where={"id": self.__id})
