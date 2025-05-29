from .modelos import *
from datetime import datetime

class Biblioteca:
    def __init__(self):
        self._livros = []
        self._usuarios = []
        self._emprestimos = []
        self._bibliotecarios = []
    
    def adicionar_livro(self, livro):
        self._livros.append(livro)
    
    def adicionar_usuario(self, usuario):
        self._usuarios.append(usuario)
    
    def adicionar_bibliotecario(self, bibliotecario):
        self._bibliotecarios.append(bibliotecario)
    
    def buscar_livro(self, termo):
        resultados = []
        for livro in self._livros:
            if (termo.lower() in livro.titulo.lower() or 
                termo.lower() in livro.autor.lower() or 
                termo.lower() in livro.genero.lower()):
                resultados.append(livro)
        return resultados
    
    def buscar_usuario(self, cpf):
        for usuario in self._usuarios:
            if usuario.cpf == cpf:
                return usuario
        return None
    
    def buscar_bibliotecario(self, cracha):
        for bibliotecario in self._bibliotecarios:
            if bibliotecario.cracha == cracha:
                return bibliotecario
        return None
    
    def realizar_emprestimo(self, livro, usuario, dias_emprestimo=7):
        if not livro.disponivel:
            return None
        
        emprestimo = Emprestimo(livro, usuario, dias_emprestimo)
        self._emprestimos.append(emprestimo)
        usuario.adicionar_emprestimo(emprestimo)
        return emprestimo
    
    def registrar_devolucao(self, emprestimo):
        emprestimo.finalizar()
        return emprestimo.calcular_multa()
    
    def listar_livros_disponiveis(self):
        return [livro for livro in self._livros if livro.disponivel]
    
    def listar_emprestimos_ativos(self):
        return [emp for emp in self._emprestimos if emp.status == "ativo"]
    
    @property
    def livros(self):
        return self._livros
    
    @property
    def usuarios(self):
        return self._usuarios
    
    @property
    def emprestimos(self):
        return self._emprestimos
    
    @property
    def bibliotecarios(self):
        return self._bibliotecarios