from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base, Comentario


class Carro(Base):
    __tablename__ = 'Carro'

    id = Column("pk_Carro", Integer, primary_key=True)
    modelo = Column(String(140), unique=True)
    ano = Column(Integer)
    valor = Column(Float)
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o Carro e o comentário.
    # Essa relação é implicita, não está salva na tabela 'Carro',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comentarios = relationship("Comentario")

    def __init__(self, modelo: str, ano: int, valor: float,
                 data_insercao: Union[DateTime, None] = None):
        """
        Cria um Carro

        Arguments:
            nome: nome do Carro.
            quantidade: quantidade que se espera comprar daquele Carro
            valor: valor esperado para o Carro
            data_insercao: data de quando o Carro foi inserido à base
        """
        self.modelo = modelo
        self.ano = ano
        self.valor = valor

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_comentario(self, comentario: Comentario):
        """ Adiciona um novo comentário ao Carro
        """
        self.comentarios.append(comentario)
