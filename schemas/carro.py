from pydantic import BaseModel
from typing import Optional, List
from model.carro import Carro

from schemas import ComentarioSchema


class CarroSchema(BaseModel):
    """ Define como um novo Carro a ser inserido deve ser representado
    """
    modelo: str = "Opala"
    ano: Optional[int] = 12
    valor: float = 12.50


class CarroBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do Carro.
    """
    modelo: str = "Fusca"


class ListagemCarrosSchema(BaseModel):
    """ Define como uma listagem de Carros será retornada.
    """
    Carros: List[CarroSchema]


def apresenta_Carros(Carros: List[Carro]):
    """ Retorna uma representação do Carro seguindo o schema definido em
        CarroViewSchema.
    """
    result = []
    for Carro in Carros:
        result.append({
            "modelo": Carro.modelo,
            "ano": Carro.ano,
            "valor": Carro.valor,
        })

    return {"Carros": result}


class CarroViewSchema(BaseModel):
    """ Define como um Carro será retornado: Carro + comentários.
    """
    id: int = 1
    modelo: str = "Fusca"
    ano: Optional[int] = 79
    valor: float = 32000.00
    total_cometarios: int = 1
    comentarios: List[ComentarioSchema]


class CarroDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str


def apresenta_Carro(Carro: Carro):
    """ Retorna uma representação do Carro seguindo o schema definido em
        CarroViewSchema.
    """
    return {
        "id": Carro.id,
        "modelo": Carro.modelo,
        "ano": Carro.ano,
        "valor": Carro.valor,
        "total_comentarios": len(Carro.comentarios),
        "comentarios": [{"texto": c.texto} for c in Carro.comentarios]
    }
