import json
import logging
from pydantic import BaseModel
from passlib.hash import bcrypt
from ...database import crud
from fastapi import (
    APIRouter,
    HTTPException,
    status,
)

router = APIRouter()

class LoginRequest(BaseModel):
    senha: str
    telefone: str


@router.post("/login/", status_code=status.HTTP_200_OK)
def login(data: LoginRequest):
    """
    Autenticação de usuário.

    Este endpoint permite que usuários autentiquem-se fornecendo telefone e senha.

    Exemplo de entrada:

    ```
    {
        "senha": "senha_abashla",
        "telefone": "123456789"
    }
    ```

    """
    try:
        logging.info("Receiving data")
        logging.info("Data received")
        logging.info("Getting user")
        user = crud.get_usuario(telefone=data.telefone)
        if user is None:
            logging.error("User not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        logging.info("User found")
        logging.info("Verifying password")
        if user and bcrypt.verify(data.senha, user.senha):
            logging.info("Login successful")
            return {"message": "Login bem-sucedido"}
        else:
            logging.warning("Login failed: Invalid email or password")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
            )
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao realizar login: " + str(e),
        )

class CreateUserRequest(BaseModel):
    email: str
    senha: str
    nome: str
    dataNascimento: str
    cpf: str
    endereco: str
    telefone: str
    cargo: str

@router.post("/create_user/", status_code=status.HTTP_201_CREATED)
def create_user(data: CreateUserRequest):
    """
    Criação de usuário.
    exemplo de entrada:
    
        {
            "email": "usuario@test2.com",
            "senha": "senha_abashla",
            "nome": "Nome do Usuário",
            "dataNascimento": "1990-01-01",
            "cpf": "12345678301",
            "endereco": "Rua Exemplo, 123",
            "telefone": "123456789",
            "cargo": "Admin"
        }
    """
    try:
        # Gerar hash da senha usando passlib
        hashed_password = bcrypt.using(rounds=12).hash(data.senha)

        logging.info("Creating user")
        user = crud.create_usuario(
            email=data.email,
            senha=hashed_password,
            nome=data.nome,
            dataNascimento=data.dataNascimento,
            cpf=data.cpf,
            endereco=data.endereco,
            telefone=data.telefone,
            cargo=data.cargo
        )
        
        logging.info("User created")
        return {"Usuario": "Criado com sucesso"}
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario não criado " + str(e)
        )
    
@router.get("/get_user/{telefone}", status_code=status.HTTP_200_OK)
def get_user(telefone: str):
    try:
        logging.info("Getting user")
        user = crud.get_usuario(telefone=telefone)
        if user is None:
            logging.error("User not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        logging.info("User found")
        return {
            "idUsuario": str(user.idUsuario),
            "email": user.email,
            "nome": user.nome,
            "dataNascimento": user.dataNascimento.isoformat(),
            "cpf": user.cpf,
            "endereco": user.endereco,
            "telefone": user.telefone,
            "cargo": user.cargo
        }
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    
@router.get("/get_all_users/", status_code=status.HTTP_200_OK)
def get_all_users():
    try:
        logging.info("Getting all users")
        users = crud.get_all_users()
        if users is None:
            logging.error("Users not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Users not found"
            )
        logging.info("Users found")
        return users
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )