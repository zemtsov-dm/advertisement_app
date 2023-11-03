from fastapi import FastAPI
from fastapi_pagination import add_pagination
from .users.routers.auth import router as auth_router
from .users.routers.users import router as users_router
from .adverts.routers import router as adverts_router
from .complaint.routers import router as complaints_router

app = FastAPI()

add_pagination(app)

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(adverts_router)
app.include_router(complaints_router)



@app.get('/api/healthchecker')
def root():
    return {'message': 'Hello World'}