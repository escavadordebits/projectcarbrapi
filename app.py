from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Carro, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="API Cadastro de Carros Antigos", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação",
               description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
carro_tag = Tag(
    name="Carro", description="Adição, visualização e remoção de carros à base")
comentario_tag = Tag(
    name="Comentario", description="Adição de um comentário à um carros cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/carro', tags=[carro_tag],
          responses={"200": CarroViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_carro(form: CarroSchema):
    """Adiciona um novo Carro à base de dados

    Retorna uma representação dos carros e comentários associados.
    """
    carro = Carro(
        modelo=form.modelo,
        ano=form.ano,
        valor=form.valor)
    logger.debug(f"Adicionando carro de nome: '{carro.modelo}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando carro
        session.add(carro)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado carro de nome: '{carro.modelo}'")
        return apresenta_Carro(carro), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Carro de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar carro '{carro.modelo}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar carro '{carro.modelo}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/carros', tags=[carro_tag],
         responses={"200": ListagemCarrosSchema, "404": ErrorSchema})
def get_carros():
    """Faz a busca por todos os Carro cadastrados

    Retorna uma representação da listagem de carros.
    """
    logger.debug(f"Coletando carros ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    carros = session.query(Carro).all()

    if not carros:
        # se não há carros cadastrados
        return {"carros": []}, 200
    else:
        logger.debug(f"%d  econtrados" % len(carros))
        # retorna a representação de carro
        print(carros)
        return apresenta_Carros(carros), 200


@app.get('/carro', tags=[carro_tag],
         responses={"200": CarroViewSchema, "404": ErrorSchema})
def get_carro(query: CarroBuscaSchema):
    """Faz a busca por um Carro a partir do id do carro

    Retorna uma representação dos carros e comentários associados.
    """
    carro_model = query.modelo
    logger.debug(f"Coletando dados sobre carro #{carro_model}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    carro = session.query(Carro).filter(Carro.modelo == carro_model).first()

    if not carro:
        # se o carro não foi encontrado
        error_msg = "Carro não encontrado na base :/"
        logger.warning(f"Erro ao buscar carro '{carro.modelo}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Carro econtrado: '{carro.modelo}'")
        # retorna a representação de carro
        return apresenta_Carro(carro), 200


@app.delete('/carro', tags=[carro_tag],
            responses={"200": CarroDelSchema, "404": ErrorSchema})
def del_carro(query: CarroBuscaSchema):
    """Deleta um Carro a partir do nome de carro informado

    Retorna uma mensagem de confirmação da remoção.
    """
    carro_modelo = unquote(unquote(query.modelo))
    print(carro_modelo)
    logger.debug(f"Deletando dados sobre carro #{carro_modelo}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Carro).filter(Carro.modelo == carro_modelo).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado carro #{carro_modelo}")
        return {"mesage": "Carro removido", "id": carro_modelo}
    else:
        # se o carro não foi encontrado
        error_msg = "Carro não encontrado na base :/"
        logger.warning(f"Erro ao deletar carro #'{carro_nome}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/comentario', tags=[comentario_tag],
          responses={"200": CarroViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """Adiciona de um novo comentário à um carros cadastrado na base identificado pelo id

    Retorna uma representação dos carros e comentários associados.
    """
    carro_id = form.carro_id
    logger.debug(f"Adicionando comentários ao carro #{carro_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo carro
    carro = session.query(Carro).filter(Carro.id == carro_id).first()

    if not carro:
        # se carro não encontrado
        error_msg = "Carro não encontrado na base :/"
        logger.warning(
            f"Erro ao adicionar comentário ao carro '{carro_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o comentário
    texto = form.texto
    comentario = Comentario(texto)

    # adicionando o comentário ao carro
    carro.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário ao carro #{carro_id}")

    # retorna a representação de carro
    return apresenta_Carro(carro), 200
