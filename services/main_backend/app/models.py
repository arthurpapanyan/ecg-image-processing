from pydantic import BaseModel


class ECGPayload(BaseModel):
    user_id: int


class ECGSubmission(BaseModel):
    id: int
    user_id: int
    ecg_image_path: str


class ECGReport(BaseModel):
    id: int
    submission_id: int
    analysis_result: str
