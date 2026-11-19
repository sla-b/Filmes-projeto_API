from database import Base, engine, _sessao_
from fastapi import FastAPI, Depends, HTTPException
import schemas, models
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import bcrypt
#Depois colocar um JWT para tornar o projeto mais profissional

Base.metadata.create_all(bind=engine)

def get_db():
    db = _sessao_()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

#API organização:
'''
-POST usuário
-GET usuário
-POST filme
-GET do filme
-POST para a avaliação do filme
-PUT para mudar alguma informação do filme
-DELETE para deletar algum filme
-GET para olhar os usuários que avaliaram
'''
#É criada a senha_hash, para impedir de ver as senhas, o hash transforma a senha em uma hash, o senha.encode() trandorma em bytes a senha, pq o hash só aceita em byte, o gensalt() gera um salt, e depois o decode() transforma a senha transformada em byte para uma senha normal de volta
@app.post('/usuario/', response_model=schemas.Usuario)
def criar_usuario(usuario :schemas.Usuario_create,  db: Session = Depends(get_db)):
    senha_hash = bcrypt.hashpw(usuario.senha.encode(), bcrypt.gensalt()).decode() 
    
    novo = models.Usuario(nome_usuario=usuario.nome_usuario, senha_hash=senha_hash)
    db.add(novo)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail='O nome do usuário já existe')
    db.refresh(novo)
    return novo

@app.get('/usuario/', response_model=list[schemas.Usuario])
def usuario_buscar(db: Session = Depends(get_db)):
    return db.query(models.Usuario).all()

@app.post('/filme/', response_model=schemas.Filme)
def registrar_filme(filme : schemas.Filme_create, db: Session = Depends(get_db)):
    filme = models.Filme(**filme.model_dump())
    db.add(filme)
    db.commit()
    db.refresh(filme)
    return filme

@app.get('/filme/', response_model=list[schemas.Filme])
def filme_buscar(db: Session = Depends(get_db)):
    return db.query(models.Filme).all()

@app.post('/filme/{filme_id}/avaliacao', response_model=schemas.Avaliacao)
def avaliar(filme_id: int, dados: schemas.Avaliacao_create, db: Session = Depends(get_db)):
    if db.get(models.Filme, filme_id) is None:
        raise HTTPException(status_code=404, detail='Filme não encontrado')

    if db.get(models.Usuario, dados.usuario_id) is None:
        raise HTTPException(status_code=404, detail='O usuário não foi encontrado')

    nova_avaliacao = models.Avaliacao(usuario_id=dados.usuario_id, filme_id=filme_id,nota= dados.nota)

    db.add(nova_avaliacao)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail='O usuário já avaliou esse filme')

    db.refresh(nova_avaliacao)
    return nova_avaliacao

@app.put('/filme/{filme_id}/', response_model=schemas.Filme)
def upload_filme(filme_id: int, dados: schemas.Filme_create, db: Session = Depends(get_db)):
    filme_PUT = db.get(models.Filme, filme_id)

    for campo, valor in dados.model_dump().items():
        setattr(filme_PUT, campo, valor)

    if filme_PUT is None:
        raise HTTPException(status_code=404, detail='O filme não foi encontrado')
    
    try:
        db.commit()
        db.refresh(filme_PUT)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail='Já existe um filme com esse nome')

    db.refresh(filme_PUT)
    return filme_PUT

@app.delete('/filme/{filme_id}/', response_model=schemas.Filme)
def deletar_filme(filme_id: int, dados: schemas.Filme,db: Session = Depends(get_db)):
    filme_delete = db.get(models.Filme, filme_id)

    if db.get(models.Filme, dados.id) is None:
        raise HTTPException(status_code=404, detail='O filme não foi encontrado')

    db.delete(filme_delete)
    try:
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=404, detail='O filme não existe')
    
    return filme_delete

