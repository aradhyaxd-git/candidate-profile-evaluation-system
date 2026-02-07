from pydantic import BaseModel, Field
from typing import Optional, Dict
from enum import Enum


class SkillLevel(str, Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"


class LearningVelocity(str, Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"


class RoleReadiness(str, Enum):
    NotReady = "Not Ready"
    PartiallyReady = "Partially Ready"
    Ready = "Ready"


class GithubStats(BaseModel):
    repos: int = Field(ge=0)
    active_months: int = Field(ge=0)


class LeetCodeStats(BaseModel):
    problems_solved: int = Field(ge=0)


class CandidateEvaluationInput(BaseModel):
    experience_years: int = Field(ge=0)
    projects_completed: int = Field(ge=0)
    primary_skill_level: SkillLevel
    learning_velocity: LearningVelocity
    role_readiness: RoleReadiness

    # for context-aware boosters (students)
    cgpa: Optional[float] = Field(default=None, ge=0, le=10)
    github: Optional[GithubStats] = None
    leetcode: Optional[LeetCodeStats] = None
    college_tier: int = Field(default=2, ge=1, le=3)


class EvaluationResponse(BaseModel):
    evaluation_id: str
    total_score: int
    fit_category: str
    score_breakdown: Dict
    explanation: Dict
