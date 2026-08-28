from pydantic import BaseModel
from typing import List

class AimRating(BaseModel):
    aim: int
    movement: int
    positioning: int
    gameSense: int
    recoil: int
    crosshair: int
    decisions: int
    utility: int

class TimestampEvent(BaseModel):
    id: str
    timestamp: str
    seconds: int
    title: str
    severity: str  # "critical" | "warning" | "positive" | "info"
    category: str
    confidence: int
    description: str

class TrainingPlan(BaseModel):
    drills: List[str]
    focusAreas: List[str]

class AnalysisResponse(BaseModel):
    jobId: str
    overallScore: float
    strengths: List[str]
    weaknesses: List[str]
    mistakes: List[str]
    improvements: List[str]
    events: List[TimestampEvent]
    ratings: AimRating
    summary: str
    recommendations: List[str]
    trainingPlan: TrainingPlan
