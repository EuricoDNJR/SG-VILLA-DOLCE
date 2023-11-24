import json
import logging
from passlib.hash import bcrypt
from ...database import crud
from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    status,
)

router = APIRouter()

@router.post("/login/", status_code=status.HTTP_200_OK)
def login(data: str = Form()):
        logging.info("Receiving data")
        json_data = json.loads(data)
        logging.info("Data received")
        logging.info("Getting user")
        user = crud.get_usuario(telefone=json_data["telefone"])
        if user is None:
            logging.error("User not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        logging.info("User found")
        logging.info("Verifying password")
        if user and bcrypt.verify(json_data["senha"], user.senha):
            logging.info("Login successful")
            return {"message": "Login bem-sucedido"}
        else:
            logging.warning("Login failed: Invalid email or password")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
            )

@router.post("/create_user/", status_code=status.HTTP_201_CREATED)
def create_user(data: str = Form()):
    try:
        logging.info("Receiving data")
        json_data = json.loads(data)
        logging.info("Data received")

        # Gerar hash da senha usando passlib
        hashed_password = bcrypt.using(rounds=12).hash(json_data["senha"])

        logging.info("Creating user")
        user = crud.create_usuario(
            email=json_data["email"],
            senha=hashed_password,
            nome=json_data["nome"],
            dataNascimento=json_data["dataNascimento"],
            cpf=json_data["cpf"],
            endereco=json_data["endereco"],
            telefone=json_data["telefone"],
            cargo=json_data["cargo"],
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