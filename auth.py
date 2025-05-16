
from jose import JWTError, jwt
from datetime import timedelta, datetime
from pathlib import Path
from typing import Optional
from enum import Enum
from typedefs.user import  User
class Auth():
    def __init__(self):
        self.private_key = Path(".ssh/private.key").read_text()
        self.public_key = Path(".ssh/public.key").read_text()
        self.algorithm = "RS256"
        self.access_token_expire_minutes = 30

    def generate_jwt_token(
        self,
        user_id: int,
        username: str,
        email: str,
        first_name: str,
        last_name: str
    ) -> str:
        to_encode = {
            "sub": str(user_id),
            "username": username,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "exp": datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        }
        encoded_jwt = jwt.encode(to_encode, self.private_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_jwt_token(self, token: str) -> Optional[User]:
        try:
            payload = jwt.decode(token, self.public_key, algorithms=[self.algorithm])
            user = User(
                user_id=int(payload.get("sub")),
                username=payload.get("username"),
                email=payload.get("email"),
                first_name=payload.get("first_name", ""),
                last_name=payload.get("last_name", ""),
                is_active=True,
                is_deleted=False,
            )
            return user
        except (JWTError, ValueError, TypeError):
            raise ValueError("Invalid token")
        except Exception as e:  
            return None
        

    
