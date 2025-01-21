from schemas.auth import Token
from fastapi import APIRouter


router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login", response_model=Token)
async def login():
    pass

@router.post("/logout")
async def logout():
    pass

@router.post("/refresh", response_model=Token)
async def refresh_token():
    pass
