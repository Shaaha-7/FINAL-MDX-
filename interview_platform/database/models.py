"""
database/models.py
ORM models:  User → InterviewSession → Answer
"""

from datetime import datetime

from sqlalchemy import (
    Boolean, Column, DateTime, Float,
    ForeignKey, Integer, JSON, String, Text,
)
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    user_id      = Column(Integer, primary_key=True, autoincrement=True)
    name         = Column(String(100))
    email        = Column(String(200), unique=True, index=True)
    role         = Column(String(100))
    experience   = Column(String(50))
    company_type = Column(String(50))
    career_goal  = Column(Text, nullable=True)
    created_at   = Column(DateTime, default=datetime.utcnow)

    sessions = relationship("InterviewSession", back_populates="user")


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    session_id      = Column(Integer, primary_key=True, autoincrement=True)
    user_id         = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    strategy_json   = Column(JSON)
    final_score     = Column(Float, nullable=True)
    readiness_level = Column(String(50), nullable=True)
    is_complete     = Column(Boolean, default=False)
    started_at      = Column(DateTime, default=datetime.utcnow)
    completed_at    = Column(DateTime, nullable=True)

    user    = relationship("User", back_populates="sessions")
    answers = relationship("Answer", back_populates="session")


class Answer(Base):
    __tablename__ = "answers"

    answer_id         = Column(Integer, primary_key=True, autoincrement=True)
    session_id        = Column(Integer, ForeignKey("interview_sessions.session_id"), nullable=False)
    skill_tested      = Column(String(100))
    difficulty        = Column(String(20))
    question_text     = Column(Text)
    answer_text       = Column(Text)
    overall_score     = Column(Float)
    concept_score     = Column(Float)
    clarity_score     = Column(Float)
    confidence_score  = Column(Float)
    strengths         = Column(Text, nullable=True)
    weaknesses        = Column(Text, nullable=True)
    improvement_tips  = Column(Text, nullable=True)
    weak_skills       = Column(JSON, nullable=True)
    ideal_answer      = Column(Text, nullable=True)
    follow_up_question = Column(Text, nullable=True)
    is_follow_up      = Column(Boolean, default=False)
    answered_at       = Column(DateTime, default=datetime.utcnow)

    session = relationship("InterviewSession", back_populates="answers")
