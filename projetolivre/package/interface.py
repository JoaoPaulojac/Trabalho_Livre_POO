import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from .modelos import *
from .servicos import Biblioteca
from .serializador import BancoDadosBiblioteca

class InterfaceBiblioteca:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Biblioteca")
        self.root.geometry("800x600")
        
        self.banco_dados = BancoDadosBiblioteca()
        self.biblioteca = self.banco_dados.biblioteca
        
        self.criar_widgets()
        self.carregar_dados_iniciais()
    
    def criar_widgets(self):
        # Notebook (abas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)
        
        # Aba de Livros
        self.aba_livros = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_livros, text="Livros")
        self.criar_aba_livros()
        
        # Aba de Usuários
        self.aba_usuarios = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_usuarios, text="Usuários")
        self.criar_aba_usuarios()
        
        # Aba de Empréstimos
        self.aba_emprestimos = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_emprestimos, text="Empréstimos")
        self.criar_aba_emprestimos()
        
        # Botão de salvar
        self.btn_salvar = ttk.Button(self.root, text="Salvar Dados", command=self.salvar_dados)
        self.btn_salvar.pack(side='bottom', pady=10)
    
    def criar_aba_livros(self):
        # Frame de pesquisa
        frame_pesquisa = ttk.Frame(self.aba_livros)
        frame_pesquisa.pack(fill='x', padx=10, pady=10)
        
        self.entry_pesquisa = ttk.Entry(frame_pesquisa)
        self.entry_pesquisa.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        btn_pesquisar = ttk.Button(frame_pesquisa, text="Pesquisar", command=self.pesquisar_livros)
        btn_pesquisar.pack(side='left')
        
        # Treeview de livros
        self.tree_livros = ttk.Treeview(self.aba_livros, columns=('titulo', 'autor', 'isbn', 'disponivel'), show='headings')
        self.tree_livros.heading('titulo', text='Título')
        self.tree_livros.heading('autor', text='Autor')
        self.tree_livros.heading('isbn', text='ISBN')
        self.tree_livros.heading('disponivel', text='Disponível')
        self.tree_livros.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Frame de botões
        frame_botoes = ttk.Frame(self.aba_livros)
        frame_botoes.pack(fill='x', padx=10, pady=10)
        
        btn_adicionar = ttk.Button(frame_botoes, text="Adicionar Livro", command=self.abrir_formulario_livro)
        btn_adicionar.pack(side='left', padx=(0, 5))
        
        btn_remover = ttk.Button(frame_botoes, text="Remover Livro", command=self.remover_livro)
        btn_remover.pack(side='left')
    
    def criar_aba_usuarios(self):
        # Treeview de usuários
        self.tree_usuarios = ttk.Treeview(self.aba_usuarios, columns=('nome', 'cpf', 'matricula'), show='headings')
        self.tree_usuarios.heading('nome', text='Nome')
        self.tree_usuarios.heading('cpf', text='CPF')
        self.tree_usuarios.heading('matricula', text='Matrícula')
        self.tree_usuarios.pack(fill='both', expand=True, padx=10, pady=(10, 0))
        
        # Frame de botões
        frame_botoes = ttk.Frame(self.aba_usuarios)
        frame_botoes.pack(fill='x', padx=10, pady=10)
        
        btn_adicionar = ttk.Button(frame_botoes, text="Adicionar Usuário", command=self.abrir_formulario_usuario)
        btn_adicionar.pack(side='left', padx=(0, 5))
        
        btn_remover = ttk.Button(frame_botoes, text="Remover Usuário", command=self.remover_usuario)
        btn_remover.pack(side='left')
    
    def criar_aba_emprestimos(self):
        # Frame de pesquisa
        frame_pesquisa = ttk.Frame(self.aba_emprestimos)
        frame_pesquisa.pack(fill='x', padx=10, pady=10)
        
        self.entry_pesquisa_emprestimo = ttk.Entry(frame_pesquisa)
        self.entry_pesquisa_emprestimo.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        btn_pesquisar = ttk.Button(frame_pesquisa, text="Pesquisar", command=self.pesquisar_emprestimos)
        btn_pesquisar.pack(side='left')
        
        # Treeview de empréstimos
        self.tree_emprestimos = ttk.Treeview(self.aba_emprestimos, columns=('livro', 'usuario', 'data_emprestimo', 'data_devolucao', 'status'), show='headings')
        self.tree_emprestimos.heading('livro', text='Livro')
        self.tree_emprestimos.heading('usuario', text='Usuário')
        self.tree_emprestimos.heading('data_emprestimo', text='Data Empréstimo')
        self.tree_emprestimos.heading('data_devolucao', text='Data Devolução')
        self.tree_emprestimos.heading('status', text='Status')
        self.tree_emprestimos.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Frame de botões
        frame_botoes = ttk.Frame(self.aba_emprestimos)
        frame_botoes.pack(fill='x', padx=10, pady=10)
        
        btn_novo = ttk.Button(frame_botoes, text="Novo Empréstimo", command=self.abrir_formulario_emprestimo)
        btn_novo.pack(side='left', padx=(0, 5))
        
        btn_devolver = ttk.Button(frame_botoes, text="Registrar Devolução", command=self.registrar_devolucao)
        btn_devolver.pack(side='left')
    
    def carregar_dados_iniciais(self):
        self.atualizar_lista_livros()
        self.atualizar_lista_usuarios()
        self.atualizar_lista_emprestimos()
    
    def atualizar_lista_livros(self):
        for item in self.tree_livros.get_children():
            self.tree_livros.delete(item)
        
        for livro in self.biblioteca.livros:
            self.tree_livros.insert('', 'end', values=(
                livro.titulo,
                livro.autor,
                livro.isbn,
                'Sim' if livro.disponivel else 'Não'
            ))
    
    def atualizar_lista_usuarios(self):
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)
        
        for usuario in self.biblioteca.usuarios:
            self.tree_usuarios.insert('', 'end', values=(
                usuario.nome,
                usuario.cpf,
                usuario.matricula
            ))
    
    def atualizar_lista_emprestimos(self):
        for item in self.tree_emprestimos.get_children():
            self.tree_emprestimos.delete(item)
        
        for emprestimo in self.biblioteca.emprestimos:
            self.tree_emprestimos.insert('', 'end', values=(
                emprestimo.livro.titulo,
                emprestimo.usuario.nome,
                emprestimo.data_emprestimo.strftime('%d/%m/%Y'),
                emprestimo.data_devolucao.strftime('%d/%m/%Y'),
                emprestimo.status
            ))
    
    def pesquisar_livros(self):
        termo = self.entry_pesquisa.get()
        resultados = self.biblioteca.buscar_livro(termo)
        
        for item in self.tree_livros.get_children():
            self.tree_livros.delete(item)
        
        for livro in resultados:
            self.tree_livros.insert('', 'end', values=(
                livro.titulo,
                livro.autor,
                livro.isbn,
                'Sim' if livro.disponivel else 'Não'
            ))
    
    def pesquisar_emprestimos(self):
        termo = self.entry_pesquisa_emprestimo.get()
        
        for item in self.tree_emprestimos.get_children():
            self.tree_emprestimos.delete(item)
        
        for emprestimo in self.biblioteca.emprestimos:
            if (termo.lower() in emprestimo.livro.titulo.lower() or 
                termo.lower() in emprestimo.usuario.nome.lower()):
                self.tree_emprestimos.insert('', 'end', values=(
                    emprestimo.livro.titulo,
                    emprestimo.usuario.nome,
                    emprestimo.data_emprestimo.strftime('%d/%m/%Y'),
                    emprestimo.data_devolucao.strftime('%d/%m/%Y'),
                    emprestimo.status
                ))
    
    def abrir_formulario_livro(self):
        formulario = tk.Toplevel(self.root)
        formulario.title("Adicionar Livro")
        
        # Widgets do formulário
        ttk.Label(formulario, text="Título:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        entry_titulo = ttk.Entry(formulario)
        entry_titulo.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(formulario, text="Autor:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        entry_autor = ttk.Entry(formulario)
        entry_autor.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(formulario, text="ISBN:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        entry_isbn = ttk.Entry(formulario)
        entry_isbn.grid(row=2, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(formulario, text="Gênero:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        entry_genero = ttk.Entry(formulario)
        entry_genero.grid(row=3, column=1, padx=5, pady=5, sticky='we')
        
        tipo_livro = tk.StringVar(value='fisico')
        ttk.Radiobutton(formulario, text="Físico", variable=tipo_livro, value='fisico').grid(row=4, column=0, columnspan=2)
        ttk.Radiobutton(formulario, text="Digital", variable=tipo_livro, value='digital').grid(row=5, column=0, columnspan=2)
        
        # Frame para campos específicos
        frame_especifico = ttk.Frame(formulario)
        frame_especifico.grid(row=6, column=0, columnspan=2, pady=5)
        
        ttk.Label(frame_especifico, text="Edição:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        entry_edicao = ttk.Entry(frame_especifico)
        entry_edicao.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(frame_especifico, text="Páginas:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        entry_paginas = ttk.Entry(frame_especifico)
        entry_paginas.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        
        def alternar_campos():
            if tipo_livro.get() == 'fisico':
                for widget in frame_especifico.winfo_children():
                    widget.grid()
                ttk.Label(frame_especifico, text="Edição:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
                entry_edicao.grid(row=0, column=1, padx=5, pady=5, sticky='we')
                ttk.Label(frame_especifico, text="Páginas:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
                entry_paginas.grid(row=1, column=1, padx=5, pady=5, sticky='we')
            else:
                for widget in frame_especifico.winfo_children():
                    widget.grid_remove()
                ttk.Label(frame_especifico, text="Formato:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
                entry_edicao.grid(row=0, column=1, padx=5, pady=5, sticky='we')
                ttk.Label(frame_especifico, text="Tamanho (MB):").grid(row=1, column=0, padx=5, pady=5, sticky='e')
                entry_paginas.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        
        tipo_livro.trace('w', lambda *args: alternar_campos())
        alternar_campos()
        
        def salvar_livro():
            titulo = entry_titulo.get()
            autor = entry_autor.get()
            isbn = entry_isbn.get()
            genero = entry_genero.get()
            
            if not all([titulo, autor, isbn, genero]):
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                return
            
            if tipo_livro.get() == 'fisico':
                edicao = entry_edicao.get()
                paginas = entry_paginas.get()
                
                if not edicao or not paginas:
                    messagebox.showerror("Erro", "Edição e páginas são obrigatórios para livros físicos!")
                    return
                
                livro = LivroFisico(titulo, autor, isbn, genero, edicao, int(paginas))
            else:
                formato = entry_edicao.get()
                tamanho = entry_paginas.get()
                
                if not formato or not tamanho:
                    messagebox.showerror("Erro", "Formato e tamanho são obrigatórios para livros digitais!")
                    return
                
                livro = LivroDigital(titulo, autor, isbn, genero, formato, float(tamanho))
            
            self.biblioteca.adicionar_livro(livro)
            self.atualizar_lista_livros()
            formulario.destroy()
            messagebox.showinfo("Sucesso", "Livro adicionado com sucesso!")
        
        btn_salvar = ttk.Button(formulario, text="Salvar", command=salvar_livro)
        btn_salvar.grid(row=7, column=0, columnspan=2, pady=10)
    
    def abrir_formulario_usuario(self):
        formulario = tk.Toplevel(self.root)
        formulario.title("Adicionar Usuário")
        
        # Widgets do formulário
        ttk.Label(formulario, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        entry_nome = ttk.Entry(formulario)
        entry_nome.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(formulario, text="CPF:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        entry_cpf = ttk.Entry(formulario)
        entry_cpf.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(formulario, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        entry_email = ttk.Entry(formulario)
        entry_email.grid(row=2, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(formulario, text="Matrícula:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        entry_matricula = ttk.Entry(formulario)
        entry_matricula.grid(row=3, column=1, padx=5, pady=5, sticky='we')
        
        def salvar_usuario():
            nome = entry_nome.get()
            cpf = entry_cpf.get()
            email = entry_email.get()
            matricula = entry_matricula.get()
            
            if not all([nome, cpf, email, matricula]):
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                return
            
            usuario = Usuario(nome, cpf, email, matricula)
            self.biblioteca.adicionar_usuario(usuario)
            self.atualizar_lista_usuarios()
            formulario.destroy()
            messagebox.showinfo("Sucesso", "Usuário adicionado com sucesso!")
        
        btn_salvar = ttk.Button(formulario, text="Salvar", command=salvar_usuario)
        btn_salvar.grid(row=4, column=0, columnspan=2, pady=10)
    
    def abrir_formulario_emprestimo(self):
        # Verificar se há livros e usuários cadastrados
        if not self.biblioteca.livros:
            messagebox.showerror("Erro", "Não há livros cadastrados!")
            return
        
        if not self.biblioteca.usuarios:
            messagebox.showerror("Erro", "Não há usuários cadastrados!")
            return
        
        formulario = tk.Toplevel(self.root)
        formulario.title("Novo Empréstimo")
        
        # Widgets do formulário
        ttk.Label(formulario, text="Livro:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        
        livros_disponiveis = [livro for livro in self.biblioteca.livros if livro.disponivel]
        if not livros_disponiveis:
            messagebox.showerror("Erro", "Não há livros disponíveis para empréstimo!")
            formulario.destroy()
            return
        
        combo_livros = ttk.Combobox(formulario, values=[livro.titulo for livro in livros_disponiveis])
        combo_livros.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(formulario, text="Usuário:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        combo_usuarios = ttk.Combobox(formulario, values=[usuario.nome for usuario in self.biblioteca.usuarios])
        combo_usuarios.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        
        ttk.Label(formulario, text="Dias para devolução:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        entry_dias = ttk.Entry(formulario)
        entry_dias.insert(0, "7")
        entry_dias.grid(row=2, column=1, padx=5, pady=5, sticky='we')
        
        def realizar_emprestimo():
            livro_selecionado = combo_livros.get()
            usuario_selecionado = combo_usuarios.get()
            dias = entry_dias.get()
            
            if not livro_selecionado or not usuario_selecionado or not dias:
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                return
            
            try:
                dias = int(dias)
            except ValueError:
                messagebox.showerror("Erro", "Dias deve ser um número inteiro!")
                return
            
            livro = next((livro for livro in livros_disponiveis if livro.titulo == livro_selecionado), None)
            usuario = next((usuario for usuario in self.biblioteca.usuarios if usuario.nome == usuario_selecionado), None)
            
            if livro and usuario:
                emprestimo = self.biblioteca.realizar_emprestimo(livro, usuario, dias)
                if emprestimo:
                    self.atualizar_lista_emprestimos()
                    self.atualizar_lista_livros()
                    formulario.destroy()
                    messagebox.showinfo("Sucesso", "Empréstimo realizado com sucesso!")
                else:
                    messagebox.showerror("Erro", "Não foi possível realizar o empréstimo!")
            else:
                messagebox.showerror("Erro", "Livro ou usuário não encontrado!")
        
        btn_emprestar = ttk.Button(formulario, text="Realizar Empréstimo", command=realizar_emprestimo)
        btn_emprestar.grid(row=3, column=0, columnspan=2, pady=10)
    
    def registrar_devolucao(self):
        selecionado = self.tree_emprestimos.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Nenhum empréstimo selecionado!")
            return
        
        item = self.tree_emprestimos.item(selecionado[0])
        livro_titulo = item['values'][0]
        usuario_nome = item['values'][1]
        
        emprestimo = next(
            (emp for emp in self.biblioteca.emprestimos 
             if emp.livro.titulo == livro_titulo and emp.usuario.nome == usuario_nome and emp.status == "ativo"),
            None
        )
        
        if not emprestimo:
            messagebox.showerror("Erro", "Empréstimo não encontrado ou já finalizado!")
            return
        
        multa = self.biblioteca.registrar_devolucao(emprestimo)
        if multa > 0:
            messagebox.showwarning("Multa", f"Empréstimo finalizado com multa de R${multa:.2f}!")
        else:
            messagebox.showinfo("Sucesso", "Empréstimo finalizado sem multa!")
        
        self.atualizar_lista_emprestimos()
        self.atualizar_lista_livros()
    
    def remover_livro(self):
        selecionado = self.tree_livros.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Nenhum livro selecionado!")
            return
        
        item = self.tree_livros.item(selecionado[0])
        titulo = item['values'][0]
        
        livro = next((livro for livro in self.biblioteca.livros if livro.titulo == titulo), None)
        if livro:
            # Verificar se o livro está emprestado
            emprestimos_ativos = [emp for emp in self.biblioteca.emprestimos 
                                if emp.livro == livro and emp.status == "ativo"]
            
            if emprestimos_ativos:
                messagebox.showerror("Erro", "Não é possível remover um livro que está emprestado!")
                return
            
            self.biblioteca.livros.remove(livro)
            self.atualizar_lista_livros()
            messagebox.showinfo("Sucesso", "Livro removido com sucesso!")
    
    def remover_usuario(self):
        selecionado = self.tree_usuarios.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Nenhum usuário selecionado!")
            return
        
        item = self.tree_usuarios.item(selecionado[0])
        cpf = item['values'][1]
        
        usuario = next((usuario for usuario in self.biblioteca.usuarios if usuario.cpf == cpf), None)
        if usuario:
            # Verificar se o usuário tem empréstimos ativos
            emprestimos_ativos = [emp for emp in self.biblioteca.emprestimos 
                                if emp.usuario == usuario and emp.status == "ativo"]
            
            if emprestimos_ativos:
                messagebox.showerror("Erro", "Não é possível remover um usuário com empréstimos ativos!")
                return
            
            self.biblioteca.usuarios.remove(usuario)
            self.atualizar_lista_usuarios()
            messagebox.showinfo("Sucesso", "Usuário removido com sucesso!")
    
    def salvar_dados(self):
        self.banco_dados.salvar()
        messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")