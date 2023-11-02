from fastapi import FastAPI
from .users.routers.auth import router as auth_router
from .users.routers.users import router as users_router
from .adverts.routers import router as adverts_router

app = FastAPI()


app.include_router(users_router)
app.include_router(auth_router)
app.include_router(adverts_router)



@app.get('/api/healthchecker')
def root():
    return {'message': 'Hello World'}