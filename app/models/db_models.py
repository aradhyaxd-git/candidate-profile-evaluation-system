import uuid
from sqlalchemy import (Column, String, Integer, SmallInteger, DateTime,ForeignKey)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    college_tier = Column(SmallInteger, nullable=False)  
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Evaluation(Base):
    __tablename__ = "evaluations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(
        UUID(as_uuid=True),
        ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False
    )
    total_score = Column(Integer, nullable=False)  #0-100
    fit_category = Column(String, nullable=False)

    input_details = Column(JSONB, nullable=False)
    score_breakdown = Column(JSONB, nullable=False)
    explanation = Column(JSONB, nullable=False)

    rule_version = Column(String, nullable=False, default="v1.0")
    evaluated_at = Column(DateTime(timezone=True), server_default=func.now())

    candidate = relationship("Candidate", backref="evaluations")
