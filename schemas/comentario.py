from pydantic import BaseModel


class ComentarioSchema(BaseModel):
    """ Define como um novo comentário a ser inserido deve ser representado
    """
    carro_id: int = 1
    texto: str = "Verificar motor, caixa de transmisao!!"
