import json
import logging
import random

from app.config import settings
from app.services.rabbitmq import RabbitMQClient
from fastapi import FastAPI

logger = logging.getLogger('uvicorn.info')

app = FastAPI(title="ECG Digitalizer", version="1.0.0")

rabbitmq_client = RabbitMQClient(
    host=settings.RABBITMQ_HOST,
    port=settings.RABBITMQ_PORT,
    username=settings.RABBITMQ_USER,
    password=settings.RABBITMQ_PASSWORD,
)


def digitalize_ecg_image(submission_data):
    """MOCK FUNCTION"""
    return {
        "metadata": {
            "patient_id": random.randint(1, 100),
            "ecg_result_id": random.randint(1000, 10000),
        },
        "ecg_result": [3.811, 1.222, 4.9333, 4.83223, 1.23245]
    }


async def process_ecg_message(message):
    try:
        message = message.body.decode()
        logger.info(f"ECG Image Processed: {digitalize_ecg_image(message)}")
        metadata = digitalize_ecg_image(message).get("metadata", {})
        await rabbitmq_client.publish("diagnostic_queue", json.dumps(metadata))
    except:
        raise Exception("Failed to digitalize image")


@app.on_event("startup")
async def startup_event():
    await rabbitmq_client.connect()
    await rabbitmq_client.consume(queue_name="ecg_queue", callback=process_ecg_message, )


@app.on_event("shutdown")
async def shutdown_event():
    await rabbitmq_client.close()


@app.get("/")
async def root():
    return {"message": "ECG Digitalizer Service"}
