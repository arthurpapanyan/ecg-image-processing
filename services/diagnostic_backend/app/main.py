import logging

from app.config import settings
from app.services.rabbitmq import RabbitMQClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger('uvicorn.error')

app = FastAPI(title="Diagnostic Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rabbitmq_client = RabbitMQClient(
    host=settings.RABBITMQ_HOST,
    port=settings.RABBITMQ_PORT,
    username=settings.RABBITMQ_USER,
    password=settings.RABBITMQ_PASSWORD,
)


def diagnose_ecg_results(message):
    """MOCK FUNCTION"""
    return {
        "metadata": {
            "patient_id": "123456",
            "date": "2023-10-01",
            "diagnosis_id": 2334234,
        },
        "heart_rate": 75,
        "rhythm": "Sinus",
        "p_wave": {
            "present": True,
            "morphology": "Normal"
        },
        "pr_interval": 160,
        "qrs_duration": 100,
        "qt_interval": 400,
        "t_wave": {
            "present": True,
            "morphology": "Normal"
        },
        "st_segment": {
            "elevation": False,
            "depression": False,
            "morphology": "Normal"
        },
        "axis": "Normal",
        "interpretation": "Normal ECG",
        "abnormalities": []
    }


async def process_ecg_results(message):
    """
    This function receives task to process digitalized ECG data.
    Args:
        message: Message containing diagnosis generation instructions.
    Returns:
        None
    """
    try:
        message = message.body.decode()
        logger.info(f"Diagnose Ready {diagnose_ecg_results(message)}")
    except:
        raise Exception("Failed to generate diagnosis")


@app.on_event("startup")
async def startup_event():
    await rabbitmq_client.connect()
    await rabbitmq_client.consume(queue_name="diagnostic_queue", callback=process_ecg_results)


@app.on_event("shutdown")
async def shutdown_event():
    await rabbitmq_client.close()


@app.get("/")
async def root():
    return {"message": "Diagnostic Backend Service"}
