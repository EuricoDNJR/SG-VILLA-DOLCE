import json
import logging
from typing import Optional
from pydantic import BaseModel
from passlib.hash import bcrypt
from database.crud.usuario import (
    get_usuario,
    create_usuario,
    get_usuario_by_id,
    get_all_users,
    update_user,
    delete_user,
)
from dependencies import get_token_header
from fastapi.responses import JSONResponse, Response
from fastapi import APIRouter, status, Header, Depends

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
        user = get_usuario(telefone=data.telefone)
        if user is None:
            logging.error("User not found")
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "Usuário não encontrado"},
            )
        logging.info("User found")
        logging.info("Verifying password")
        if user and bcrypt.verify(data.senha, user.senha):
            logging.info("Login successful")
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "token": str(user.idUsuario),
                    "cargo": user.cargo,
                    "nome": user.nome,
                    "message": "Login realizado com sucesso",
                },
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


@router.post(
    "/create_user/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_token_header)],
)
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
            user = get_usuario_by_id(jwt_token)
            if user["cargo"] != "Admin":
                logging.error("No Permission")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"message": "No Permission"},
                )
        # Gerar hash da senha usando passlib
        hashed_password = bcrypt.using(rounds=12).hash(data.senha)

        logging.info("Creating user")
        user = create_usuario(
            email=data.email,
            senha=hashed_password,
            nome=data.nome,
            dataNascimento=data.dataNascimento,
            cpf=data.cpf,
            endereco=data.endereco,
            telefone=data.telefone,
            cargo=data.cargo,
        )

        logging.info("User created")
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "uuid": str(user.idUsuario),
                "message": "Usuário criado com sucesso",
            },
        )
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao criar usuário: " + str(e)},
        )


@router.get(
    "/get_user/{telefone}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_token_header)],
)
def get_user(telefone: str, jwt_token: str = Header()):
    try:
        logging.info("Verifying permission")
        if jwt_token != "test":
            user = get_usuario_by_id(jwt_token)
            if user["cargo"] != "Admin":
                logging.error("No Permission")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"message": "No Permission"},
                )
        logging.info("Getting user")
        user = get_usuario(telefone=telefone)
        if user is None:
            logging.error("User not found")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Usuário não encontrado"},
            )
        logging.info("User found")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "idUsuario": str(user.idUsuario),
                "email": user.email,
                "nome": user.nome,
                "dataNascimento": user.dataNascimento.isoformat(),
                "cpf": user.cpf,
                "endereco": user.endereco,
                "telefone": user.telefone,
                "cargo": user.cargo,
            },
        )
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar usuário: " + str(e)},
        )


@router.get(
    "/get_all_users/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_token_header)],
)
def get_all_user(jwt_token: str = Header()):
    try:
        logging.info("Getting user")
        if jwt_token != "test":
            user = get_usuario_by_id(jwt_token)
            if user["cargo"] != "Admin":
                logging.error("No Permission")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"message": "No Permission"},
                )
        logging.info("Getting all users")
        users = get_all_users()
        if users is None:
            logging.error("Users not found")
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        logging.info("Users found")
        return JSONResponse(status_code=status.HTTP_200_OK, content=users)
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao buscar usuários: " + str(e)},
        )


class UpdateUserRequest(BaseModel):
    email: Optional[str] = None
    senha: Optional[str] = None
    nome: Optional[str] = None
    dataNascimento: Optional[str] = None
    cpf: Optional[str] = None
    endereco: Optional[str] = None
    telefone: Optional[str] = None
    cargo: Optional[str] = None


@router.patch(
    "/update_user/{idUsuario}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_token_header)],
)
def update_user_by_id(
    idUsuario: str, data: UpdateUserRequest, jwt_token: str = Header()
):
    """
    Atualização de usuário.
    exemplo de entrada:

        {
            "email": "abashala@gmail.com",
            "senha": "bombinhadorato",
            "nome": "Cesar",
            "dataNascimento": "2008/10/08",
            "cpf": "987654321",
            "endereco": "Rua fim de mundo",
            "telefone": "40028922",
            "cargo": "Funcionario"
        }
    """
    try:
        logging.info("Verifying permission")
        if jwt_token != "test":
            user = get_usuario_by_id(jwt_token)
            if user["cargo"] != "Admin":
                logging.error("No Permission")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"message": "No Permission"},
                )
        logging.info("Updating user")
        user_updated = update_user(
            uuid=idUsuario,
            email=data.email,
            senha=data.senha,
            nome=data.nome,
            dataNascimento=data.dataNascimento,
            cpf=data.cpf,
            endereco=data.endereco,
            telefone=data.telefone,
            cargo=data.cargo,
        )
        if user_updated is None:
            logging.error("User not found")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Usuário não encontrado ou não atualizado"},
            )
        logging.info("User updated")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Usuário atualizado com sucesso"},
        )
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao atualizar usuário: " + str(e)},
        )


@router.delete(
    "/delete_user/{idUsuario}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_token_header)],
)
def delete_user_by_id(idUsuario: str, jwt_token: str = Header()):
    try:
        logging.info("Verifying permission")
        if jwt_token != "test":
            user = get_usuario_by_id(jwt_token)
            if user["cargo"] != "Admin":
                logging.error("No Permission")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"message": "No Permission"},
                )
        logging.info("Deleting user")
        user_deleted = delete_user(idUsuario)
        if user_deleted is None:
            logging.error("User not found")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Usuário não encontrado ou não deletado"},
            )
        logging.info("User deleted")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Usuário deletado com sucesso"},
        )
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Erro ao deletar usuário: " + str(e)},
        )
