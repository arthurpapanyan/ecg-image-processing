import logging

from app.config import settings
from app.routes import user
from app.services.rabbitmq import RabbitMQClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger('uvicorn.info')

rabbitmq_client = RabbitMQClient(
    host=settings.RABBITMQ_HOST,
    port=settings.RABBITMQ_PORT,
    username=settings.RABBITMQ_USER,
    password=settings.RABBITMQ_PASSWORD,
)

app = FastAPI(title="Main Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/users", tags=["users"])


@app.on_event("startup")
async def startup_event():
    await rabbitmq_client.connect()


@app.on_event("shutdown")
async def shutdown_event():
    await rabbitmq_client.close()


@app.get("/")
async def root():
    return {"message": "Main Backend Service"}
