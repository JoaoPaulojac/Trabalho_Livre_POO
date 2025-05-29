import pickle
import json
from datetime import datetime
import os
from .servicos import Biblioteca 

class Serializador:
    @staticmethod
    def salvar_para_arquivo(objeto, nome_arquivo):
        with open(nome_arquivo, 'wb') as arquivo:
            pickle.dump(objeto, arquivo)
    
    @staticmethod
    def carregar_de_arquivo(nome_arquivo):
        try:
            with open(nome_arquivo, 'rb') as arquivo:
                return pickle.load(arquivo)
        except FileNotFoundError:
            return None
    
    @staticmethod
    def serializar_para_json(objeto):
        if isinstance(objeto, (list, dict, str, int, float, bool)):
            return json.dumps(objeto)
        
        if hasattr(objeto, '__dict__'):
            return json.dumps(objeto.__dict__, default=Serializador._serializar_datetime)
        
        raise ValueError("Objeto não serializável para JSON")
    
    @staticmethod
    def _serializar_datetime(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError("Tipo não serializável")

class BancoDadosBiblioteca:
    def __init__(self, nome_arquivo='biblioteca.db'):
        self.nome_arquivo = nome_arquivo
        self.biblioteca = self.carregar() or Biblioteca()
    
    def salvar(self):
        Serializador.salvar_para_arquivo(self.biblioteca, self.nome_arquivo)
    
    def carregar(self):
        return Serializador.carregar_de_arquivo(self.nome_arquivo)