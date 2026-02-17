"""
engine/interview_engine.py — Adaptive interview orchestration
FIX: submit_answer now accepts skipped=True flag, passes it to AI evaluator.
"""

import random
import time
from datetime import datetime
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from ..config import settings
from ..data.question_bank import QUESTION_BANK, SKILLS
from ..database.models import Answer, InterviewSession, User
from ..services.ai_service import AIService
from ..services.analytics_service import AnalyticsService


class InterviewEngine:

    def __init__(self, ai: AIService, db: Session):
        self.ai  = ai
        self.db  = db
        self.strategy:         Optional[dict] = None
        self.session_obj:      Optional[InterviewSession] = None
        self.answers:          List[dict] = []
        self.used_skills:      List[str]  = []
        self.follow_up_count:  Dict[str, int] = {}
        self.current_question: Optional[dict] = None
        self.question_count:   int = 0

    def setup_profile(self, profile: dict) -> User:
        email = profile.get("email") or f"user_{int(time.time())}@demo.com"
        user  = self.db.query(User).filter(User.email == email).first()
        if not user:
            user = User(
                name=profile.get("name", "Candidate"),
                email=email,
                role=profile.get("role", "ML Engineer"),
                experience=profile.get("experience", "Fresher"),
                company_type=profile.get("company_type", "FAANG"),
                career_goal=profile.get("career_goal", ""),
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)

        self.strategy = self.ai.generate_strategy(profile)
        sess = InterviewSession(user_id=user.user_id, strategy_json=self.strategy)
        self.db.add(sess)
        self.db.commit()
        self.db.refresh(sess)
        self.session_obj = sess
        return user

    def next_question(self, follow_up: Optional[str] = None) -> Optional[dict]:
        if self.question_count >= settings.max_questions:
            return None

        if follow_up and self.current_question:
            skill = self.current_question["skill"]
            cnt   = self.follow_up_count.get(skill, 0)
            if cnt < settings.max_follow_ups_per_skill:
                self.follow_up_count[skill] = cnt + 1
                self.question_count += 1
                self.current_question = {
                    "question":     follow_up,
                    "skill":        skill,
                    "difficulty":   "hard",
                    "is_follow_up": True,
                }
                return self.current_question

        focus     = (self.strategy or {}).get("focus_skills", SKILLS)
        available = [s for s in focus if s not in self.used_skills]
        if not available:
            available = [s for s in SKILLS if s not in self.used_skills]
        if not available:
            available = focus

        skill  = available[0]
        diff   = (self.strategy or {}).get("difficulty", "medium")
        pool   = QUESTION_BANK.get(skill, {}).get(diff) \
               or QUESTION_BANK.get(skill, {}).get("medium", ["Explain this concept."])

        self.used_skills.append(skill)
        self.question_count += 1
        self.current_question = {
            "question":     random.choice(pool),
            "skill":        skill,
            "difficulty":   diff,
            "is_follow_up": False,
        }
        return self.current_question

    def submit_answer(self, answer_text: str, skipped: bool = False) -> dict:
        """
        Evaluate the answer. If skipped=True, passes that flag to AIService
        which returns honest 0/0/0/0 scores — never fakes good feedback.
        """
        if not self.current_question:
            raise ValueError("No active question — call next_question() first.")

        ev = self.ai.evaluate_answer(
            question   = self.current_question["question"],
            answer     = answer_text,
            skill      = self.current_question["skill"],
            difficulty = self.current_question["difficulty"],
            skipped    = skipped,
        )
        rec = Answer(
            session_id         = self.session_obj.session_id,
            skill_tested       = self.current_question["skill"],
            difficulty         = self.current_question["difficulty"],
            question_text      = self.current_question["question"],
            answer_text        = answer_text if not skipped else "— skipped —",
            overall_score      = ev["overall_score"],
            concept_score      = ev["concept_score"],
            clarity_score      = ev["clarity_score"],
            confidence_score   = ev["confidence_score"],
            strengths          = ev["strengths"],
            weaknesses         = ev["weaknesses"],
            improvement_tips   = ev["improvement_tips"],
            weak_skills        = ev.get("weak_skills", []),
            ideal_answer       = ev["ideal_answer"],
            follow_up_question = ev.get("follow_up_question"),
            is_follow_up       = self.current_question.get("is_follow_up", False),
        )
        self.db.add(rec)
        self.db.commit()
        self.answers.append({**ev, "skill_tested": self.current_question["skill"]})
        return ev

    def finalize(self) -> dict:
        report = AnalyticsService.full_report(
            answers=self.answers, profile={}, strategy=self.strategy or {}
        )
        r = report["readiness"]
        self.session_obj.final_score     = r["score"]
        self.session_obj.readiness_level = r["level"]
        self.session_obj.is_complete     = True
        self.session_obj.completed_at    = datetime.utcnow()
        self.db.commit()
        return report
