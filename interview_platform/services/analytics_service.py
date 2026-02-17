"""
services/analytics_service.py
─────────────────────────────────────────────────────────────
Readiness scoring, skill breakdown, weak-skill clustering,
and full report generation.
─────────────────────────────────────────────────────────────
"""

from datetime import datetime
from typing import Dict, List

from ..config import settings


class AnalyticsService:

    # ── Readiness ─────────────────────────────────────────────────

    @staticmethod
    def compute_readiness(answers: List[dict]) -> dict:
        """
        Composite =  concept×0.40 + clarity×0.20
                   + confidence×0.20 + consistency×0.20

        Bands:
          [0, 4)  → Beginner
          [4, 7)  → Intermediate
          [7, 10] → Interview Ready
        """
        if not answers:
            return {"score": 0.0, "level": "Beginner", "composite": {}}

        def avg(k: str) -> float:
            return sum(a.get(k, 0) for a in answers) / len(answers)

        concept    = avg("concept_score")
        clarity    = avg("clarity_score")
        confidence = avg("confidence_score")
        ov_scores  = [a.get("overall_score", 0) for a in answers]
        consistency = (
            10.0 - (max(ov_scores) - min(ov_scores))
            if len(ov_scores) > 1
            else ov_scores[0]
        )
        consistency = max(0.0, min(10.0, consistency))

        composite = (
            concept    * settings.w_concept
            + clarity  * settings.w_clarity
            + confidence * settings.w_confidence
            + consistency * settings.w_consistency
        )
        composite = round(max(0.0, min(10.0, composite)), 2)
        level = (
            "Interview Ready" if composite >= 7.0
            else "Intermediate"  if composite >= 4.0
            else "Beginner"
        )
        return {
            "score": composite,
            "level": level,
            "composite": {
                "concept":     round(concept,     2),
                "clarity":     round(clarity,     2),
                "confidence":  round(confidence,  2),
                "consistency": round(consistency, 2),
            },
        }

    # ── Skill breakdown ───────────────────────────────────────────

    @staticmethod
    def skill_breakdown(answers: List[dict]) -> Dict[str, dict]:
        buckets: Dict[str, dict] = {}
        for a in answers:
            sk = a.get("skill_tested", "Unknown")
            b  = buckets.setdefault(sk, {"o": [], "c": [], "cl": [], "cf": []})
            b["o"].append(a.get("overall_score",   0))
            b["c"].append(a.get("concept_score",   0))
            b["cl"].append(a.get("clarity_score",  0))
            b["cf"].append(a.get("confidence_score", 0))

        def _avg(lst): return round(sum(lst) / len(lst), 2) if lst else 0.0
        return {
            sk: {
                "avg_overall":    _avg(b["o"]),
                "avg_concept":    _avg(b["c"]),
                "avg_clarity":    _avg(b["cl"]),
                "avg_confidence": _avg(b["cf"]),
                "count":          len(b["o"]),
            }
            for sk, b in buckets.items()
        }

    @staticmethod
    def weak_skill_clusters(answers: List[dict], threshold: float = 5.0) -> List[str]:
        bd = AnalyticsService.skill_breakdown(answers)
        return [s for s, d in bd.items() if d["avg_overall"] < threshold]

    # ── Full report ───────────────────────────────────────────────

    @staticmethod
    def full_report(answers: List[dict], profile: dict, strategy: dict) -> dict:
        readiness = AnalyticsService.compute_readiness(answers)
        breakdown = AnalyticsService.skill_breakdown(answers)
        weak      = AnalyticsService.weak_skill_clusters(answers)
        avg_ov    = (
            round(sum(a.get("overall_score", 0) for a in answers) / len(answers), 2)
            if answers else 0.0
        )
        return {
            "profile":             profile,
            "strategy":            strategy,
            "readiness":           readiness,
            "skill_breakdown":     breakdown,
            "weak_skill_clusters": weak,
            "total_questions":     len(answers),
            "avg_overall":         avg_ov,
            "generated_at":        datetime.utcnow().isoformat(),
        }
