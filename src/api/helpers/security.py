from fastapi import HTTPException, status, Security
from fastapi.security import HTTPBearer
from os import getenv

API_KEY = getenv('API_KEY')
oauth_schema = HTTPBearer()


def authorize(api_key: str = Security(oauth_schema)):
    if api_key.scheme != 'Bearer' or api_key.credentials != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )
