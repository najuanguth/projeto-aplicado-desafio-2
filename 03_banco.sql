PRAGMA foreign_keys = ON;

CREATE TABLE tecnico (
    id_tecnico INTEGER PRIMARY KEY,
    nome TEXT NOT NULL
);

CREATE TABLE equipamento (
    id_equipamento INTEGER PRIMARY KEY,
    codigo TEXT NOT NULL UNIQUE,
    descricao TEXT NOT NULL,
    fabricante TEXT
);

CREATE TABLE medicao (
    id_medicao INTEGER PRIMARY KEY,
    id_tecnico INTEGER NOT NULL,
    id_equipamento INTEGER NOT NULL,
    referencia_calibracao TEXT NOT NULL,
    data_calibracao TEXT NOT NULL,
    solicitante TEXT NOT NULL,
    parametro TEXT NOT NULL,
    unidade TEXT NOT NULL,
    valor_nominal REAL NOT NULL,
    tolerancia_mais REAL NOT NULL,
    tolerancia_menos REAL NOT NULL,
    medida_1 REAL NOT NULL,
    medida_2 REAL NOT NULL,
    valor_obtido REAL NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (id_tecnico) REFERENCES tecnico(id_tecnico),
    FOREIGN KEY (id_equipamento) REFERENCES equipamento(id_equipamento)
);
