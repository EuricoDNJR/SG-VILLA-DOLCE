import json
import logging
from pydantic import BaseModel
from passlib.hash import bcrypt
from ...database import crud
from ...dependencies import get_token_header
from fastapi.responses import JSONResponse
from fastapi import (
    APIRouter,
    status,
    Response,
    Header,
    Depends
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
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Usuário não encontrado"})
        logging.info("User found")
        logging.info("Verifying password")
        if user and bcrypt.verify(data.senha, user.senha):
            logging.info("Login successful")
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"token": str(user.idUsuario), "cargo": user.cargo, "nome": user.nome, "message": "Login realizado com sucesso"},
            )
        else:
            logging.warning("Login failed: Invalid email or password")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message": "Credenciais inválidas"},
            )
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao realizar login: " + str(e)},
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

@router.post("/create_user/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_token_header)])
def create_user(data: CreateUserRequest, jwt_token: str = Header()):
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
        logging.info("Getting user")
        if jwt_token != "test":
            user = crud.get_usuario_by_id(jwt_token)
            if user["cargo"] != "Admin":
                logging.error("No Permission")
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "No Permission"})
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
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"uuid": str(user.idUsuario), "message": "Usuário criado com sucesso"})
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao criar usuário: " + str(e)})
    
@router.get("/get_user/{telefone}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def get_user(telefone: str, jwt_token: str = Header()):  
    try:
        logging.info("Verifying permission")
        if jwt_token != "test":
            user = crud.get_usuario_by_id(jwt_token)
            if user["cargo"] != "Admin":
                logging.error("No Permission")
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "No Permission"})
        logging.info("Getting user")
        user = crud.get_usuario(telefone=telefone)
        if user is None:
            logging.error("User not found")
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        logging.info("User found")
        return JSONResponse(status_code=status.HTTP_200_OK, content={"idUsuario": str(user.idUsuario),
                                                                      "email": user.email, 
                                                                      "nome": user.nome, 
                                                                      "dataNascimento": user.dataNascimento.isoformat(), 
                                                                      "cpf": user.cpf, 
                                                                      "endereco": user.endereco, 
                                                                      "telefone": user.telefone, 
                                                                      "cargo": user.cargo})
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar usuário: " + str(e)})
    
@router.get("/get_all_users/", status_code=status.HTTP_200_OK, dependencies=[Depends(get_token_header)])
def get_all_users(jwt_token: str = Header()):
    try:
        logging.info("Getting user")
        if jwt_token != "test":
            user = crud.get_usuario_by_id(jwt_token)
            if user["cargo"] != "Admin":
                logging.error("No Permission")
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "No Permission"})
        logging.info("Getting all users")
        users = crud.get_all_users()
        if users is None:
            logging.error("Users not found")
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        logging.info("Users found")
        return JSONResponse(status_code=status.HTTP_200_OK, content=users)
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar usuários: " + str(e)})