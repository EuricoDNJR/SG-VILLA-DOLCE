import os
import logging
import dotenv
from fastapi import Header, HTTPException, status
from database.crud import get_usuario_by_id

dotenv.load_dotenv()

TEST = os.getenv("TEST")

async def get_token_header(jwt_token: str = Header()):
    try:
        if TEST == "ON":
            logging.warning("Test mode")
            if jwt_token != "test":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid JWT token"
                )

            return "test"
        
        user = get_usuario_by_id(jwt_token)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid JWT token"
            )
        
        return jwt_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid JWT token"
        )
            
        
        
