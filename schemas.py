from pydantic import BaseModel, Field
from decimal import Decimal

#Serve para como os dados vão ser classificados no banco de dados
#usuários:
class UsuarioBase(BaseModel):
    nome_usuario: str

class Usuario_create(UsuarioBase):
    senha: str
    email: str

class Usuario(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

#avaliação:
class AvaliacaoBase(BaseModel):
    nota: Decimal = Field(ge=0, le=5, decimal_places=1)

class Avaliacao_create(AvaliacaoBase):
    usuario_id: int

class Avaliacao(AvaliacaoBase):
    id: int
    usuario_id: int
    filme_id: int

    class Config:
        from_attributes = True

#Filme:
class FilmeBase(BaseModel):
    nome: str
    ano_lancamento: int
    diretor: str

class Filme_create(FilmeBase):
    pass

class Filme(FilmeBase):
    id: int
    avaliacao: list[Avaliacao] = []

    class Config:
        from_attributes = True