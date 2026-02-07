from app.utils import scoring, explainability
from app.core.database import AsyncSessionLocal
from app.repositories.evaluation_repo import (
    get_or_create_candidate,
    save_evaluation
)


async def evaluate_candidate(payload):
    breakdown = {}
    explanation = {}
    exp_score = scoring.score_experience(payload.experience_years)

    proj_score = scoring.score_projects(payload.projects_completed)
    proj_score = min(
        int(proj_score * scoring.college_tier_multiplier(payload.college_tier)),
        25
    )

    skill_score = scoring.score_skill(payload.primary_skill_level.value)
    learning_score = scoring.score_learning_velocity(payload.learning_velocity.value)
    readiness_score = scoring.score_role_readiness(payload.role_readiness.value)

    breakdown.update({
        "experience": exp_score,
        "projects": proj_score,
        "skill": skill_score,
        "learning_velocity": learning_score,
        "role_readiness": readiness_score,
    })

    explanation.update({
        "experience": explainability.explain_experience(payload.experience_years, exp_score),
        "projects": explainability.explain_projects(
            payload.projects_completed, payload.college_tier, proj_score
        ),
        "skill": explainability.explain_skill(payload.primary_skill_level.value, skill_score),
        "learning_velocity": explainability.explain_learning(
            payload.learning_velocity.value, learning_score
        ),
        "role_readiness": explainability.explain_readiness(
            payload.role_readiness.value, readiness_score
        ),
    })

    total = sum(breakdown.values())

    if payload.experience_years <= 1:
        if payload.cgpa is not None:
            cgpa_bonus = min(int(payload.cgpa), 8)
            breakdown["cgpa"] = cgpa_bonus
            explanation["cgpa"] = f"CGPA {payload.cgpa} → +{cgpa_bonus}"
            total += cgpa_bonus

        if payload.github:
            gh_bonus = min(payload.github.active_months * 2, 6)
            breakdown["github"] = gh_bonus
            explanation["github"] = f"GitHub consistency → +{gh_bonus}"
            total += gh_bonus

        if payload.leetcode:
            lc_bonus = min(payload.leetcode.problems_solved // 50 * 2, 6)
            breakdown["leetcode"] = lc_bonus
            explanation["leetcode"] = f"LeetCode practice → +{lc_bonus}"
            total += lc_bonus

    total = min(total, 100)

    fit = (
        "Not Ready" if total < 40 else
        "Potential Fit" if total < 70 else
        "Strong Fit"
    )

    result = {
        "total_score": total,
        "fit_category": fit,
        "score_breakdown": breakdown,
        "explanation": explanation
    }


    async with AsyncSessionLocal() as db:
        candidate = await get_or_create_candidate(
            db,
            college_tier=payload.college_tier
        )

        evaluation = await save_evaluation(
            db,
            candidate,
            result,
            input_details=payload.model_dump()
        )

    result["evaluation_id"] = str(evaluation.id)
    return result

async def fetch_evaluation(evaluation_id: str):
    async with AsyncSessionLocal() as db:
        evaluation = await get_evaluation_by_id(db, evaluation_id)

        if not evaluation:
            return None

        return {
            "evaluation_id": str(evaluation.id),
            "total_score": evaluation.total_score,
            "fit_category": evaluation.fit_category,
            "score_breakdown": evaluation.score_breakdown,
            "explanation": evaluation.explanation,
            "input_details": evaluation.input_details,
            "evaluated_at": evaluation.evaluated_at,
        }
