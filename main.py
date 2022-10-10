from fastapi import FastAPI, APIRouter

from viws import user_router

app = FastAPI()

router = APIRouter()


@router.get('/')
def first():
    return 'Hello World!'


app.include_router(prefix='/first', router=router)
app.include_router(user_router)
