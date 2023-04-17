import hashlib
import secrets
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Request
from ..helpers.database import get_db
from ..models import APIKey


class AuthService:
    def __init__(self, user_id, db: Session) -> None:
        self.user_id = user_id
        self.db = db

    def create_api_key(self):
        api_key = AuthService.generate_api_key()
        hashed_api_key = AuthService.hash_api_key(api_key)
        self.save_api_key(hashed_api_key)
        return api_key

    @staticmethod
    def generate_api_key():
        return secrets.token_urlsafe(32)

    @staticmethod
    def hash_api_key(api_key: str):
        try:
            sha256 = hashlib.sha256()
            sha256.update(api_key.encode('utf-8'))
            return sha256.hexdigest()
        except Exception:
            return None  # TODO Handle this error.

    def save_api_key(self, api_key_hashed):
        db_api_key = APIKey(key=api_key_hashed, user_id=self.user_id)
        self.db.add(db_api_key)
        self.db.commit()
        self.db.refresh(db_api_key)
        return db_api_key

    @staticmethod
    def validate_api_key(request: Request, db: Session = Depends(get_db)):
        key = request.headers.get('Api-key', None)
        key_hash = AuthService.hash_api_key(key)
        api_key = AuthService.get_api_key(db, key_hash)
        if not api_key:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized. A valid Api-key is needed."
            )

    def get_api_key(db: Session, key_hash):
        return db.query(APIKey).filter(APIKey.key == key_hash).first()
