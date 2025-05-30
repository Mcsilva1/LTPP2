import tkinter as tk
from tkinter import ttk, messagebox
from Database import Database

class Interface:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.title("Sistema Escolar Ceub")
        self.setup_ui()
        self.carregar_dados()

    def setup_ui(self):
        # Aluno Section
        tk.Label(self.root, text="Nome:").grid(row=0, column=0)
        self.entry_nome = tk.Entry(self.root)
        self.entry_nome.grid(row=0, column=1)

        tk.Label(self.root, text="Idade:").grid(row=1, column=0)
        self.entry_idade = tk.Entry(self.root)
        self.entry_idade.grid(row=1, column=1)

        tk.Button(self.root, text="Inserir Aluno", command=self.inserir_aluno).grid(row=2, column=0, columnspan=2)

        self.tree_alunos = ttk.Treeview(self.root, columns=("ID", "Nome", "Idade"), show="headings")
        for col in ("ID", "Nome", "Idade"):
            self.tree_alunos.heading(col, text=col)
        self.tree_alunos.grid(row=3, column=0, columnspan=2)

        tk.Button(self.root, text="Deletar Aluno", command=self.deletar_aluno).grid(row=4, column=0, columnspan=2)

        # Matricula Section
        tk.Label(self.root, text="ID Aluno:").grid(row=0, column=2)
        self.entry_aluno_id = tk.Entry(self.root)
        self.entry_aluno_id.grid(row=0, column=3)

        tk.Label(self.root, text="Curso:").grid(row=1, column=2)
        self.entry_curso = tk.Entry(self.root)
        self.entry_curso.grid(row=1, column=3)

        tk.Button(self.root, text="Inserir Matrícula", command=self.inserir_matricula).grid(row=2, column=2, columnspan=2)

        self.tree_matriculas = ttk.Treeview(self.root, columns=("ID", "Aluno", "Curso"), show="headings")
        for col in ("ID", "Aluno", "Curso"):
            self.tree_matriculas.heading(col, text=col)
        self.tree_matriculas.grid(row=3, column=2, columnspan=2)

        tk.Button(self.root, text="Deletar Matrícula", command=self.deletar_matricula).grid(row=4, column=2, columnspan=2)

    def inserir_aluno(self):
        try:
            nome = self.entry_nome.get()
            idade = int(self.entry_idade.get())
            if self.db.inserir_aluno(nome, idade):
                self.carregar_dados()
                self.entry_nome.delete(0, tk.END)
                self.entry_idade.delete(0, tk.END)
            else:
                messagebox.showerror("Erro", "Erro ao inserir aluno")
        except ValueError:
            messagebox.showerror("Erro", "Idade deve ser um número inteiro")

    def inserir_matricula(self):
        try:
            aluno_id = int(self.entry_aluno_id.get())
            curso = self.entry_curso.get()
            if self.db.inserir_matricula(aluno_id, curso):
                self.carregar_dados()
                self.entry_aluno_id.delete(0, tk.END)
                self.entry_curso.delete(0, tk.END)
            else:
                messagebox.showerror("Erro", "ID do aluno inválido")
        except ValueError:
            messagebox.showerror("Erro", "ID do aluno deve ser um número inteiro")

    def carregar_dados(self):
        # Load Alunos
        for row in self.tree_alunos.get_children():
            self.tree_alunos.delete(row)
        for row in self.db.carregar_alunos():
            self.tree_alunos.insert("", "end", values=row)

        # Load Matriculas
        for row in self.tree_matriculas.get_children():
            self.tree_matriculas.delete(row)
        for row in self.db.carregar_matriculas():
            self.tree_matriculas.insert("", "end", values=row)

    def deletar_aluno(self):
        selected = self.tree_alunos.selection()
        if selected:
            aluno_id = self.tree_alunos.item(selected[0])['values'][0]
            if self.db.deletar_aluno(aluno_id):
                self.carregar_dados()
            else:
                messagebox.showerror("Erro", "Erro ao deletar aluno")

    def deletar_matricula(self):
        selected = self.tree_matriculas.selection()
        if selected:
            matricula_id = self.tree_matriculas.item(selected[0])['values'][0]
            if self.db.deletar_matricula(matricula_id):
                self.carregar_dados()
            else:
                messagebox.showerror("Erro", "Erro ao deletar matrícula")

    def run(self):
        self.root.mainloop()
        self.db.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    app.run()