# 3rd party libraries
from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader

# Source
from src.settings import settings


api_key_header_auth = APIKeyHeader(name=settings.API_KEY_NAME, auto_error=True)


async def get_api_key(api_key_header: str = Security(api_key_header_auth)):
    if api_key_header != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
