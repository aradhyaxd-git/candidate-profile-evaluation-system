from fastapi import APIRouter,HTTPException
from app.models.schemas import CandidateEvaluationInput, EvaluationResponse
from app.services.evaluation_service import evaluate_candidate, fetch_evaluation

router = APIRouter(prefix="/evaluate", tags=["CPES"])


@router.post("/", response_model=EvaluationResponse)
async def evaluate(payload: CandidateEvaluationInput):
    return await evaluate_candidate(payload)


@router.get("/evaluation/{evaluation_id}")
async def get_evaluation(evaluation_id: str):
    result = await fetch_evaluation(evaluation_id)

    if not result:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    return result