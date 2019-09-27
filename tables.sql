CREATE TABLE IF NOT EXISTS "marche" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"nome"	TEXT NOT NULL,
	"logo"	TEXT
);

CREATE TABLE IF NOT EXISTS "veicoli" (
                                         "id"               INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                         "marca"            INTEGER,
                                         "serie"            TEXT,
                                         "modello"          TEXT,
                                         "cavalli"          TEXT,
                                         "anno_costruzione" TEXT,
                                         "categoria"        TEXT,
                                         "prezzo"           REAL,
                                         "qta"              INTEGER,
                                         "foto"             TEXT
);

CREATE TABLE IF NOT EXISTS "impostazioni"
(
    "id"      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "setting" TEXT    NOT NULL,
    "value"   TEXT    NOT NULL
);