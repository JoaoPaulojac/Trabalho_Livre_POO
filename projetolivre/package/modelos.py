from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class Pessoa(ABC):
    def __init__(self, nome, cpf, email):
        self._nome = nome
        self._cpf = cpf
        self._email = email
    
    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome(self, valor):
        self._nome = valor
    
    @property
    def cpf(self):
        return self._cpf
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, valor):
        self._email = valor
    
    @abstractmethod
    def exibir_info(self):
        pass


class Usuario(Pessoa):
    def __init__(self, nome, cpf, email, matricula):
        super().__init__(nome, cpf, email)
        self._matricula = matricula
        self._emprestimos = []
    
    @property
    def matricula(self):
        return self._matricula
    
    def exibir_info(self):
        return f"Usuário: {self._nome} - Matrícula: {self._matricula}"
    
    def adicionar_emprestimo(self, emprestimo):
        self._emprestimos.append(emprestimo)
    
    def listar_emprestimos(self):
        return self._emprestimos


class Bibliotecario(Pessoa):
    def __init__(self, nome, cpf, email, cracha):
        super().__init__(nome, cpf, email)
        self._cracha = cracha
    
    @property
    def cracha(self):
        return self._cracha
    
    def exibir_info(self):
        return f"Bibliotecário: {self._nome} - Crachá: {self._cracha}"


class Livro(ABC):
    def __init__(self, titulo, autor, isbn, genero):
        self._titulo = titulo
        self._autor = autor
        self._isbn = isbn
        self._genero = genero
        self._disponivel = True
    
    @property
    def titulo(self):
        return self._titulo
    
    @property
    def autor(self):
        return self._autor
    
    @property
    def isbn(self):
        return self._isbn
    
    @property
    def genero(self):
        return self._genero
    
    @property
    def disponivel(self):
        return self._disponivel
    
    @disponivel.setter
    def disponivel(self, valor):
        self._disponivel = valor
    
    @abstractmethod
    def exibir_detalhes(self):
        pass


class LivroFisico(Livro):
    def __init__(self, titulo, autor, isbn, genero, edicao, paginas):
        super().__init__(titulo, autor, isbn, genero)
        self._edicao = edicao
        self._paginas = paginas
    
    def exibir_detalhes(self):
        return f"Livro Físico: {self._titulo} - {self._autor} (Ed. {self._edicao}, {self._paginas} páginas)"


class LivroDigital(Livro):
    def __init__(self, titulo, autor, isbn, genero, formato, tamanho):
        super().__init__(titulo, autor, isbn, genero)
        self._formato = formato
        self._tamanho = tamanho
    
    def exibir_detalhes(self):
        return f"Livro Digital: {self._titulo} - {self._autor} ({self._formato}, {self._tamanho}MB)"


class Emprestimo:
    def __init__(self, livro, usuario, dias_emprestimo=7):
        self._livro = livro
        self._usuario = usuario
        self._data_emprestimo = datetime.now()
        self._data_devolucao = self._data_emprestimo + timedelta(days=dias_emprestimo)
        self._status = "ativo"
        livro.disponivel = False
    
    @property
    def livro(self):
        return self._livro
    
    @property
    def usuario(self):
        return self._usuario
    
    @property
    def data_emprestimo(self):
        return self._data_emprestimo
    
    @property
    def data_devolucao(self):
        return self._data_devolucao
    
    @property
    def status(self):
        return self._status
    
    def finalizar(self):
        self._status = "finalizado"
        self._livro.disponivel = True
    
    def calcular_multa(self):
        if self._status == "ativo" and datetime.now() > self._data_devolucao:
            dias_atraso = (datetime.now() - self._data_devolucao).days
            return dias_atraso * 2.0  # R$2 por dia de atraso
        return 0.0