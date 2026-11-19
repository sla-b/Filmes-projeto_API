from database import Base
from sqlalchemy import (
    Integer, String, Column, CheckConstraint, UniqueConstraint, ForeignKey, Numeric
    )
from sqlalchemy.orm import relationship


class Filme(Base):
    __tablename__ = 'filme'

    id = Column(Integer, primary_key=True)
    nome = Column(String(120), unique=True)
    ano_lancamento = Column(Integer())
    diretor = Column(String(50))

    avaliacoes = relationship('Avaliacao', back_populates='filme')

class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True)
    nome_usuario = Column(String(20), unique=True)
    emial = Column(String(40), nullable=False)
    senha_hash = Column(String, nullable=False)

    avaliacoes = relationship('Avaliacao', back_populates='usuario')

class Avaliacao(Base):
    __tablename__ = 'avaliacao'

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    filme_id = Column(Integer, ForeignKey('filme.id'))
    nota = Column(Numeric(2, 1), nullable=False)

    usuario = relationship('Usuario', back_populates='avaliacoes')
    filme = relationship('Filme', back_populates='avaliacoes')

    __table_args__ = (
        CheckConstraint('nota >= 0 AND nota <= 5', name='ck_nota_entre_0_e_5'),
        UniqueConstraint('usuario_id', 'filme_id', name='uq_usuario_filme'),
    )

