from fastapi import FastAPI
from src.routes import contacts, users, auth, token
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()


app.include_router(contacts.router, prefix="/api")  # Можете додати префікс "/api"
app.include_router(users.router, prefix="/api")     # Можете додати префікс "/api"
app.include_router(auth.router, prefix="/api/auth") # Додайте маршрути з авторизацією
app.include_router(token.router, prefix="/api/token") # Додайте маршрути для токенів
@app.get("/")
def read_root():
    return {"message": "Hello World"}


# Налаштування CORS
origins = [
    "http://localhost",
    "http://localhost:8080",  # Додайте адреси, з яких дозволяєте запити
    "http://example.com",
    "https://example.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)