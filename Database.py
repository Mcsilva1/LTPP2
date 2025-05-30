import sqlite3

class Database:
    def __init__(self, db_name="escola.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                idade INTEGER NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Matriculas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_id INTEGER NOT NULL,
                curso TEXT NOT NULL,
                FOREIGN KEY (aluno_id) REFERENCES Alunos(id)
            )
        ''')
        self.conn.commit()

    def inserir_aluno(self, nome, idade):
        try:
            self.cursor.execute("INSERT INTO Alunos (nome, idade) VALUES (?, ?)", (nome, idade))
            self.conn.commit()
            return True
        except sqlite3.Error:
            return False

    def inserir_matricula(self, aluno_id, curso):
        try:
            self.cursor.execute("INSERT INTO Matriculas (aluno_id, curso) VALUES (?, ?)", (aluno_id, curso))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def carregar_alunos(self):
        self.cursor.execute("SELECT * FROM Alunos")
        return self.cursor.fetchall()

    def carregar_matriculas(self):
        self.cursor.execute("SELECT Matriculas.id, Alunos.nome, Matriculas.curso FROM Matriculas JOIN Alunos ON Matriculas.aluno_id = Alunos.id")
        return self.cursor.fetchall()

    def deletar_aluno(self, aluno_id):
        try:
            self.cursor.execute("DELETE FROM Matriculas WHERE aluno_id = ?", (aluno_id,))
            self.cursor.execute("DELETE FROM Alunos WHERE id = ?", (aluno_id,))
            self.conn.commit()
            return True
        except sqlite3.Error:
            return False

    def deletar_matricula(self, matricula_id):
        try:
            self.cursor.execute("DELETE FROM Matriculas WHERE id = ?", (matricula_id,))
            self.conn.commit()
            return True
        except sqlite3.Error:
            return False

    def close(self):
        self.conn.close()