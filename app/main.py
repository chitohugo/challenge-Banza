from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, client, category, categories_clients, account, movement

app = FastAPI(title='Test Banza', version='0.1')

origins = [
    settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, tags=['Auth'], prefix='/api/auth')
app.include_router(client.router, tags=['Clients'], prefix='/api/clients')
app.include_router(category.router, tags=['Categories'], prefix='/api/categories')
app.include_router(categories_clients.router, tags=['CategoriesClients'], prefix='/api/categories-clients')
app.include_router(account.router, tags=['Accounts'], prefix='/api/accounts')
app.include_router(movement.router, tags=['Movements'], prefix='/api/movements')

