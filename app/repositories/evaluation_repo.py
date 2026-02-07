from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db_models import Candidate, Evaluation


HARDCODED_EMAIL = "test@example.com"


async def get_or_create_candidate(
    db: AsyncSession,
    college_tier: int
) -> Candidate:
    result = await db.execute(
        select(Candidate).where(Candidate.email == HARDCODED_EMAIL)
    )
    candidate = result.scalar_one_or_none()

    if candidate:
        return candidate

    candidate = Candidate(
        email=HARDCODED_EMAIL,
        college_tier=college_tier
    )
    db.add(candidate)
    await db.flush()   # gets candidate.id
    return candidate


async def save_evaluation(
    db: AsyncSession,
    candidate: Candidate,
    result: dict,
    input_details: dict
) -> Evaluation:

    evaluation = Evaluation(
        candidate_id=candidate.id,
        total_score=result["total_score"],
        fit_category=result["fit_category"],
        input_details=input_details,
        score_breakdown=result["score_breakdown"],
        explanation=result["explanation"],
    )

    db.add(evaluation)
    await db.commit()
    await db.refresh(evaluation)

    return evaluation


async def get_evaluation_by_id(
    db: AsyncSession,
    evaluation_id: str
) -> Evaluation | None:
    result = await db.execute(
        select(Evaluation).where(Evaluation.id == evaluation_id)
    )
    return result.scalar_one_or_none()
