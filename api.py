import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

from generate_data import generate_students
from model import FEATURES, predict, train_model

app = FastAPI(title="Student Cloud Analytics API", version="1.0.0")
model = train_model(generate_students()).pipeline


class StudentInput(BaseModel):
    attendance: float = Field(ge=0, le=100)
    practice_score: float = Field(ge=0, le=100)
    activity: float = Field(ge=0, le=100)
    missed_tasks: int = Field(ge=0, le=50)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "student-cloud-analytics"}


@app.post("/predict")
def prediction(student: StudentInput) -> dict:
    frame = pd.DataFrame([student.model_dump()], columns=FEATURES)
    row = predict(model, frame).iloc[0]
    return {"risk_level": row["predicted_risk"], "confidence": float(row["confidence"])}

