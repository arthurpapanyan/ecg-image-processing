import json
import os

from app.config import settings
from app.models import ECGSubmission
from app.services.rabbitmq import RabbitMQClient
from fastapi import APIRouter, UploadFile, File, Form

router = APIRouter()

ecg_submissions_db = []
ecg_reports_db = []

rabbitmq_client = RabbitMQClient(
    host=settings.RABBITMQ_HOST,
    port=settings.RABBITMQ_PORT,
    username=settings.RABBITMQ_USER,
    password=settings.RABBITMQ_PASSWORD,
)


@router.post("/ecg_submissions/", response_model=ECGSubmission)
async def create_ecg_submission(
        user_id: int = Form(...),
        ecg_image: UploadFile = File(...)
):
    ecg_image_path = f"ecg_images/{ecg_image.filename}"
    os.makedirs("ecg_images", exist_ok=True)
    with open(ecg_image_path, "wb") as buffer:
        buffer.write(await ecg_image.read())

    submission_id = len(ecg_submissions_db) + 1
    ecg_submission = ECGSubmission(
        id=submission_id,
        user_id=user_id,
        ecg_image_path=ecg_image_path,
    )
    ecg_submissions_db.append(ecg_submission)

    message = json.dumps(dict(ecg_submission))
    await rabbitmq_client.publish("ecg_queue", message)

    return ecg_submission
