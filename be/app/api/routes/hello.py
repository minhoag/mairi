from fastapi import APIRouter

router = APIRouter(prefix="/hello", tags=["hello"])

@router.get("/")
def read_hello() -> str:
    return "Hello world"
