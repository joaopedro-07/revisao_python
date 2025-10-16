# João Pedro da Cunha Machado

import tkinter as tk 
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import os

class SistemaAlunos:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Cadastro de Alunos")
        self.root.geometry("700x500")

        # DataFrame inicial
        self.df = pd.DataFrame(columns=["Nome", "Idade", "Curso", "Nota Final"])

        # === CAMPOS DE CADASTRO ===
        frame_cadastro = tk.LabelFrame(root, text="Cadastro de Alunos", padx=10, pady=10)
        frame_cadastro.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_cadastro, text="Nome:").grid(row=0, column=0)
        tk.Label(frame_cadastro, text="Idade:").grid(row=0, column=2)
        tk.Label(frame_cadastro, text="Curso:").grid(row=1, column=0)
        tk.Label(frame_cadastro, text="Nota Final:").grid(row=1, column=2)

        self.entry_nome = tk.Entry(frame_cadastro)
        self.entry_idade = tk.Entry(frame_cadastro)
        self.entry_curso = tk.Entry(frame_cadastro)
        self.entry_nota = tk.Entry(frame_cadastro)

        self.entry_nome.grid(row=0, column=1, padx=5, pady=2)
        self.entry_idade.grid(row=0, column=3, padx=5, pady=2)
        self.entry_curso.grid(row=1, column=1, padx=5, pady=2)
        self.entry_nota.grid(row=1, column=3, padx=5, pady=2)

        tk.Button(frame_cadastro, text="Cadastrar", command=self.cadastrar).grid(row=2, column=0, columnspan=4, pady=5)

        # === TABELA DE ALUNOS ===
        frame_tabela = tk.LabelFrame(root, text="Tabela de Alunos", padx=10, pady=10)
        frame_tabela.pack(fill="both", expand=True, padx=10, pady=10)

        colunas = ["Nome", "Idade", "Curso", "Nota Final"]
        self.tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
        for col in colunas:
            self.tabela.heading(col, text=col)
            self.tabela.column(col, width=150)
        self.tabela.pack(fill="both", expand=True)

        # === FILTRO E ARQUIVOS ===
        frame_botoes = tk.Frame(root)
        frame_botoes.pack(pady=10)

        tk.Label(frame_botoes, text="Filtrar notas acima de:").grid(row=0, column=0, padx=5)
        self.entry_media = tk.Entry(frame_botoes, width=10)
        self.entry_media.grid(row=0, column=1, padx=5)

        tk.Button(frame_botoes, text="Filtrar", command=self.filtrar).grid(row=0, column=2, padx=5)
        tk.Button(frame_botoes, text="Exportar CSV (Filtrados)", command=self.exportar_csv).grid(row=0, column=3, padx=5)
        tk.Button(frame_botoes, text="Salvar CSV", command=self.salvar_csv).grid(row=0, column=4, padx=5)
        tk.Button(frame_botoes, text="Carregar CSV", command=self.carregar_csv).grid(row=0, column=5, padx=5)

    # === FUNÇÕES ===
    def cadastrar(self):
        nome = self.entry_nome.get().strip()
        idade = self.entry_idade.get().strip()
        curso = self.entry_curso.get().strip()
        nota = self.entry_nota.get().strip()

        if not nome or not idade or not curso or not nota:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        try:
            idade = int(idade)
            nota = float(nota)
        except ValueError:
            messagebox.showerror("Erro", "Idade deve ser número inteiro e nota deve ser número!")
            return

        # ✅ Validações de faixa
        if idade < 13 or idade > 50:
            messagebox.showerror("Erro", "A idade deve estar entre 13 e 50 anos!")
            return

        if nota < 0 or nota > 100:
            messagebox.showerror("Erro", "A nota deve estar entre 0 e 100!")
            return

        novo = pd.DataFrame([[nome, idade, curso, nota]], columns=self.df.columns)
        self.df = pd.concat([self.df, novo], ignore_index=True)
        self.atualizar_tabela()
        self.limpar_campos()

    def atualizar_tabela(self, dados=None):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        dados = dados if dados is not None else self.df
        for _, row in dados.iterrows():
            self.tabela.insert("", "end", values=list(row))

    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_idade.delete(0, tk.END)
        self.entry_curso.delete(0, tk.END)
        self.entry_nota.delete(0, tk.END)

    def filtrar(self):
        media = self.entry_media.get().strip()
        if not media:
            messagebox.showwarning("Aviso", "Informe uma média para filtrar!")
            return

        try:
            media = float(media)
        except ValueError:
            messagebox.showerror("Erro", "Informe um número válido para a média!")
            return

        filtrados = self.df[self.df["Nota Final"] > media]
        if filtrados.empty:
            messagebox.showinfo("Resultado", "Nenhum aluno com nota acima dessa média.")
        self.atualizar_tabela(filtrados)
        self.df_filtrado = filtrados

    def salvar_csv(self):
        caminho = filedialog.asksaveasfilename(defaultextension=".csv",
                                               filetypes=[("Arquivos CSV", "*.csv")])
        if caminho:
            self.df.to_csv(caminho, index=False)
            messagebox.showinfo("Sucesso", f"Dados salvos em:\n{caminho}")

    def carregar_csv(self):
        caminho = filedialog.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])
        if caminho and os.path.exists(caminho):
            self.df = pd.read_csv(caminho)
            self.atualizar_tabela()
            messagebox.showinfo("Sucesso", "Arquivo carregado com sucesso!")

    def exportar_csv(self):
        if not hasattr(self, "df_filtrado") or self.df_filtrado.empty:
            messagebox.showwarning("Aviso", "Nenhum dado filtrado para exportar!")
            return

        caminho = filedialog.asksaveasfilename(defaultextension=".csv",
                                               filetypes=[("Arquivos CSV", "*.csv")])
        if caminho:
            self.df_filtrado.to_csv(caminho, index=False)
            messagebox.showinfo("Sucesso", f"Relatório exportado para:\n{caminho}")


# === EXECUÇÃO ===
if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaAlunos(root)
    root.mainloop()