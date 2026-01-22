from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_password_hash, verify_password
from app.db.session import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import Token, UsuarioCreate, UsuarioResponse

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/signup", response_model=UsuarioResponse, status_code=201)
async def criar_usuario(usuario: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    """Cria um novo usuário no sistema"""
    # 1. Verifica se já existe alguém com esse nome
    result = await db.execute(select(Usuario).where(Usuario.username == usuario.username))
    existing_user = result.scalars().first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Nome de usuário já está em uso")
    
    # 2. Cria o usuário com a senha criptografada (Nunca salvamos senha pura!)
    novo_usuario = Usuario(
        username=usuario.username,
        password_hash=get_password_hash(usuario.password)
    )
    
    db.add(novo_usuario)
    await db.commit()
    await db.refresh(novo_usuario)
    
    return novo_usuario

@router.post("/login", response_model=Token)
async def login_para_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    db: AsyncSession = Depends(get_db)
):
    """Recebe usuário e senha, valida e devolve o Token JWT"""
    # 1. Busca o usuário
    result = await db.execute(select(Usuario).where(Usuario.username == form_data.username))
    user = result.scalars().first()
    
    # 2. Verifica se usuário existe e se a senha bate
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Gera o Token com validade
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}