"""
services/ai_service.py
═══════════════════════════════════════════════════════════════
PRODUCTION-GRADE EVALUATION ENGINE
───────────────────────────────────────────────────────────────
Architecture:
  1. Strategy Generator     — personalised interview plan
  2. Three-Pass Evaluator   — CoT + rubric + reference comparison
  3. Ideal Answer Generator — expert reference for each question

Three-Pass Evaluation Logic:
  Pass 1 — Extraction: What did the candidate ACTUALLY say?
            (prevents scoring style over substance)
  Pass 2 — Comparison: Compare extracted facts vs ideal answer.
            Flag missing concepts, wrong statements, gaps.
  Pass 3 — Scoring: Assign 0-10 per dimension using rubric anchors
            + generate specific, actionable feedback.

Model: gemini-2.5-pro-preview (best reasoning, best instruction-follow)
Temperature: 0.0 for evaluation (fully deterministic)
             0.5 for strategy (creative, personalised)
═══════════════════════════════════════════════════════════════
"""

import json
import time
import random
from typing import Optional

from ..config import settings
from ..data.question_bank import SKILLS, IDEAL_ANSWERS

try:
    import google.generativeai as genai
    _SDK_OK = True
except ImportError:
    _SDK_OK = False


# ── Scoring rubric anchors (same for every call) ──────────────────
RUBRIC = """
SCORING RUBRIC — apply these criteria strictly:

OVERALL / CONCEPT SCORE:
  9-10: Precise definition + correct math/derivation + production example + trade-offs discussed
  7-8:  Correct concepts + good depth + minor gaps in math or examples
  5-6:  Mostly correct but missing depth, equations, or real examples
  3-4:  Partially correct, notable conceptual errors, or surface-level only
  1-2:  Mostly wrong, buzzwords without substance, or off-topic
  0:    No answer, single word, or complete nonsense

CLARITY SCORE:
  9-10: Perfect structure (define→explain→example→trade-off), precise language, no ambiguity
  7-8:  Clear and well-organised with minor structure issues
  5-6:  Understandable but rambling or lacks clear flow
  3-4:  Hard to follow, jumps around, or contradicts itself
  1-2:  Very unclear or incoherent
  0:    Cannot be evaluated

CONFIDENCE SCORE:
  9-10: Decisive statements, uses technical vocabulary correctly, no unjustified hedging
  7-8:  Mostly confident with occasional unnecessary qualification
  5-6:  Mix of confident and uncertain statements
  3-4:  Frequent hedging without justification ("I think maybe…")
  1-2:  Highly uncertain or apologetic throughout
  0:    Cannot be evaluated

IMPORTANT: Do NOT round up. A 5 means average. A 7 means genuinely good.
A 9 or 10 should be rare — only for truly exceptional answers.
"""


class AIService:

    def __init__(self, api_key: Optional[str] = None, mock: bool = False):
        self.mock = mock
        self._eval_model     = None
        self._strategy_model = None
        key = api_key or settings.gemini_api_key

        if not mock and key:
            if _SDK_OK:
                genai.configure(api_key=key)
                # Evaluation: fully deterministic
                self._eval_model = genai.GenerativeModel(
                    model_name=settings.gemini_model_eval,
                    generation_config=genai.GenerationConfig(
                        temperature=0.0,
                        max_output_tokens=1800,
                    ),
                )
                # Strategy: creative & personalised
                self._strategy_model = genai.GenerativeModel(
                    model_name=settings.gemini_model_strategy,
                    generation_config=genai.GenerationConfig(
                        temperature=0.5,
                        max_output_tokens=800,
                    ),
                )
            else:
                print("[AIService] google-generativeai not installed.")
                self.mock = True
        elif not mock:
            self.mock = True

    # ═══════════════════════════════════════════════════════════════
    #  PUBLIC API
    # ═══════════════════════════════════════════════════════════════

    def generate_strategy(self, profile: dict) -> dict:
        """Generate a personalised interview strategy."""
        if self.mock:
            return self._mock_strategy()

        prompt = f"""
You are a principal ML interview architect at a top tech company.
Analyse this candidate profile and build a targeted interview strategy.
Return ONLY valid JSON — no markdown, no explanation.

CANDIDATE:
  Role target:    {profile['role']}
  Company type:   {profile['company_type']}
  Experience:     {profile['experience']}
  Self-reported weak areas: {', '.join(profile.get('weak_areas', [])) or 'none'}
  Career goal:    {profile.get('career_goal', '') or 'not specified'}

AVAILABLE SKILLS: {', '.join(SKILLS)}

CALIBRATION RULES:
  FAANG / Big Tech → hard difficulty, deep theory, math derivations required
  Startup          → medium, applied ML, system design, MLOps
  Research Lab     → hard, optimisation theory, paper-level depth
  Finance / Quant  → hard, statistics, probability, risk
  Student/Fresher  → easy-medium, strong fundamentals, conceptual clarity
  1-2 Years        → medium, applied knowledge, some depth
  3-5 Years        → hard, design decisions, production experience
  5+ Years         → hard, architecture, leadership, edge cases

RULES:
- Prioritise self-reported weak areas as focus skills
- Pick exactly 4 focus skills most relevant to their target role
- interview_style must match the company type
- style_reason must be 1 specific, actionable sentence

Return EXACTLY:
{{
  "focus_skills":    ["s1","s2","s3","s4"],
  "difficulty":      "easy|medium|hard",
  "interview_style": "conceptual|research|applied|system-design",
  "probing_enabled": true,
  "style_reason":    "One specific sentence explaining this strategy."
}}"""

        raw = self._call_json(prompt, model="strategy")
        valid = [s for s in raw.get("focus_skills", []) if s in SKILLS]
        return {
            "focus_skills":    valid[:4] if valid else random.sample(SKILLS, 4),
            "difficulty":      raw.get("difficulty",      "medium"),
            "interview_style": raw.get("interview_style", "applied"),
            "probing_enabled": bool(raw.get("probing_enabled", True)),
            "style_reason":    raw.get("style_reason",    "Balanced strategy based on your profile."),
        }

    def evaluate_answer(self, question: str, answer: str,
                        skill: str, difficulty: str,
                        skipped: bool = False) -> dict:
        """
        Three-pass evaluation:
          Pass 1 → Extract what candidate said
          Pass 2 → Compare against ideal answer
          Pass 3 → Score + feedback
        """
        # ── Hard gates ────────────────────────────────────────────
        if skipped:
            ideal = self._get_ideal(question, skill)
            return {
                "overall_score": 0.0, "concept_score": 0.0,
                "clarity_score": 0.0, "confidence_score": 0.0,
                "strengths":         "Question was skipped.",
                "weaknesses":        "No attempt made. This is a critical gap.",
                "improvement_tips":  f"Study {skill} thoroughly. Start with fundamentals, then work through derivations and real examples.",
                "weak_skills":       [skill],
                "ideal_answer":      ideal,
                "follow_up_question": None,
                "reasoning":         "Skipped — no evaluation performed.",
            }

        clean = answer.strip()
        if len(clean) < 25:
            ideal = self._get_ideal(question, skill)
            return {
                "overall_score": 0.5, "concept_score": 0.5,
                "clarity_score": 0.0, "confidence_score": 0.0,
                "strengths":         "An attempt was made.",
                "weaknesses":        "Answer is too short to evaluate. Minimum 2-3 full sentences required.",
                "improvement_tips":  "Write a complete answer: define the concept, explain it, give an equation or example.",
                "weak_skills":       [skill],
                "ideal_answer":      ideal,
                "follow_up_question": None,
                "reasoning":         "Too short to evaluate.",
            }

        if self.mock:
            return self._mock_evaluation(skill)

        return self._three_pass_evaluate(question, clean, skill, difficulty)

    # ═══════════════════════════════════════════════════════════════
    #  THREE-PASS EVALUATION ENGINE
    # ═══════════════════════════════════════════════════════════════

    def _three_pass_evaluate(self, question: str, answer: str,
                              skill: str, difficulty: str) -> dict:
        ideal = self._get_ideal(question, skill)

        # ── Pass 1: Extract what the candidate actually said ──────
        pass1_prompt = f"""
You are extracting factual claims from a candidate's interview answer.
Be objective. Do not evaluate quality yet — just extract.

QUESTION: {question}
SKILL: {skill}
CANDIDATE ANSWER: "{answer}"

List every distinct technical claim, definition, formula, or example the candidate mentioned.
Be precise and literal. If they said something wrong, still list it.

Return JSON:
{{
  "claimed_facts": ["fact1", "fact2", ...],
  "mentioned_equations": ["eq1", ...],
  "mentioned_examples": ["ex1", ...],
  "answer_length": "short|medium|long",
  "has_structure": true|false
}}"""

        extracted = self._call_json(pass1_prompt, model="eval")

        # ── Pass 2: Compare against ideal answer ──────────────────
        pass2_prompt = f"""
You are a senior ML expert comparing a candidate's answer to the ideal answer.

QUESTION: {question}
SKILL: {skill}  
DIFFICULTY: {difficulty}

IDEAL ANSWER (expert level):
{ideal}

WHAT CANDIDATE CLAIMED:
{json.dumps(extracted, indent=2)}

FULL CANDIDATE ANSWER: "{answer}"

Analyse the gap between candidate and ideal:

Return JSON:
{{
  "correct_points":   ["things they got right"],
  "missing_concepts": ["important concepts they omitted"],
  "wrong_statements": ["factual errors if any"],
  "depth_assessment": "surface|basic|intermediate|deep|expert",
  "has_math":         true|false,
  "has_real_example": true|false,
  "covers_tradeoffs": true|false
}}"""

        comparison = self._call_json(pass2_prompt, model="eval")

        # ── Pass 3: Score and generate feedback ───────────────────
        pass3_prompt = f"""
You are a strict senior ML interviewer. Score this answer using the rubric below.
Return ONLY valid JSON.

{RUBRIC}

CONTEXT:
  Question:   {question}
  Skill:      {skill}
  Difficulty: {difficulty}
  
IDEAL ANSWER:
{ideal}

EVALUATION SUMMARY:
  Correct points:   {comparison.get('correct_points', [])}
  Missing concepts: {comparison.get('missing_concepts', [])}
  Wrong statements: {comparison.get('wrong_statements', [])}
  Depth:            {comparison.get('depth_assessment', 'basic')}
  Has math:         {comparison.get('has_math', False)}
  Has real example: {comparison.get('has_real_example', False)}
  Covers tradeoffs: {comparison.get('covers_tradeoffs', False)}

FULL CANDIDATE ANSWER: "{answer}"

SCORING ADJUSTMENT RULES:
- difficulty=hard → be 1 point stricter (harder to earn high scores)
- Missing all key concepts from ideal → concept_score max 4
- No math when math is expected → concept_score max 6  
- No real example → clarity_score capped at 7
- Has wrong statements → subtract 1-2 points from concept_score
- Short answer (1-2 sentences) → overall max 4

FOLLOW-UP LOGIC:
  overall < 4  → ask for clarification on the weakest concept they mentioned
  4-6          → ask them to give a concrete production example
  7-8          → push deeper with math or edge case
  9-10         → challenge with an adversarial scenario
  wrong answer → null (correct it in ideal_answer instead)

Return EXACTLY this JSON:
{{
  "overall_score":      <0.0-10.0, one decimal>,
  "concept_score":      <0.0-10.0, one decimal>,
  "clarity_score":      <0.0-10.0, one decimal>,
  "confidence_score":   <0.0-10.0, one decimal>,
  "strengths":          "Specific things done well (2-3 sentences)",
  "weaknesses":         "Specific gaps or errors (2-3 sentences, be direct)",
  "improvement_tips":   "3 concrete actionable steps to improve",
  "weak_skills":        ["specific sub-skill 1", "specific sub-skill 2"],
  "ideal_answer":       "Complete 3-5 sentence expert answer to this question",
  "follow_up_question": "Specific follow-up question or null",
  "reasoning":          "1 sentence explaining your overall score"
}}"""

        result = self._call_json(pass3_prompt, model="eval")

        c = self._clamp
        return {
            "overall_score":      c(result.get("overall_score",    0)),
            "concept_score":      c(result.get("concept_score",    0)),
            "clarity_score":      c(result.get("clarity_score",    0)),
            "confidence_score":   c(result.get("confidence_score", 0)),
            "strengths":          result.get("strengths",          "Attempted the question."),
            "weaknesses":         result.get("weaknesses",         "Insufficient depth to fully evaluate."),
            "improvement_tips":   result.get("improvement_tips",   "Study the core concepts and practice with examples."),
            "weak_skills":        result.get("weak_skills",        [skill]),
            "ideal_answer":       result.get("ideal_answer",       ideal),
            "follow_up_question": result.get("follow_up_question"),
            "reasoning":          result.get("reasoning",          ""),
        }

    # ═══════════════════════════════════════════════════════════════
    #  IDEAL ANSWER GENERATOR
    # ═══════════════════════════════════════════════════════════════

    def _get_ideal(self, question: str, skill: str) -> str:
        # Check pre-written bank first
        key = question.strip()[:80]
        if key in IDEAL_ANSWERS:
            return IDEAL_ANSWERS[key]

        if self.mock:
            return (
                f"A complete answer defines the concept precisely, provides the key equation "
                f"or derivation, gives a production example, and discusses trade-offs and "
                f"failure modes relevant to {skill}."
            )

        prompt = f"""
You are a principal ML engineer at a top company.
Write a complete, expert-level answer to this interview question.

Question: "{question}"
Skill area: {skill}

Requirements:
- Start with a precise definition
- Include the key equation or mathematical formulation if relevant
- Give a concrete real-world example
- Mention at least one trade-off or limitation
- 3-5 sentences maximum, dense and precise

Write ONLY the answer, no labels, no JSON."""

        try:
            resp = self._strategy_model.generate_content(prompt)
            text = resp.text.strip()
            return text[:800] if text else f"See {skill} fundamentals for a complete answer."
        except Exception:
            return f"A thorough understanding of {skill} concepts is required to answer this question well."

    # ═══════════════════════════════════════════════════════════════
    #  INTERNAL HELPERS
    # ═══════════════════════════════════════════════════════════════

    def _call_json(self, prompt: str, model: str = "eval") -> dict:
        m = self._eval_model if model == "eval" else self._strategy_model
        retries = 2
        for attempt in range(retries):
            try:
                resp = m.generate_content(prompt)
                return self._parse(resp.text)
            except Exception as exc:
                if attempt == retries - 1:
                    print(f"[AIService] Gemini error after {retries} attempts: {exc}")
                    return {}
                time.sleep(1.5)
        return {}

    @staticmethod
    def _parse(text: str) -> dict:
        if not text:
            return {}
        text = text.strip()
        # Strip markdown fences
        if "```" in text:
            parts = text.split("```")
            for part in parts:
                cleaned = part.lstrip("json").strip()
                if cleaned.startswith("{"):
                    text = cleaned
                    break
        try:
            return json.loads(text)
        except Exception:
            s = text.find("{")
            e = text.rfind("}") + 1
            if s != -1 and e > s:
                try:
                    return json.loads(text[s:e])
                except Exception:
                    pass
        return {}

    @staticmethod
    def _clamp(v, lo: float = 0.0, hi: float = 10.0) -> float:
        try:
            return round(max(lo, min(hi, float(v))), 1)
        except Exception:
            return 0.0

    # ═══════════════════════════════════════════════════════════════
    #  MOCK (realistic, varied — not fake-good)
    # ═══════════════════════════════════════════════════════════════

    def _mock_strategy(self) -> dict:
        return {
            "focus_skills":    random.sample(SKILLS, 4),
            "difficulty":      "medium",
            "interview_style": "applied",
            "probing_enabled": True,
            "style_reason":    "Balanced applied strategy targeting key ML fundamentals.",
        }

    def _mock_evaluation(self, skill: str) -> dict:
        # Realistic distribution — not always high
        weights = [0.10, 0.20, 0.30, 0.25, 0.10, 0.05]
        bands   = [(1,2), (3,4), (5,6), (6,7), (7,8), (8,9)]
        band    = random.choices(bands, weights=weights)[0]
        s       = round(random.uniform(*band), 1)
        return {
            "overall_score":      s,
            "concept_score":      self._clamp(s + random.uniform(-1.5, 1.0)),
            "clarity_score":      self._clamp(s + random.uniform(-1.0, 1.0)),
            "confidence_score":   self._clamp(s + random.uniform(-1.5, 0.8)),
            "strengths":          "Demonstrated partial understanding of the core concept.",
            "weaknesses":         "Missing mathematical depth and production-level examples.",
            "improvement_tips":   (
                "1) Study the mathematical derivation. "
                "2) Implement it from scratch. "
                "3) Relate to a real project you have worked on."
            ),
            "weak_skills":        [skill],
            "ideal_answer": (
                "A strong answer precisely defines the concept, provides the key equation, "
                "demonstrates it with a concrete example, and discusses failure modes."
            ),
            "follow_up_question": (
                f"Can you walk through the mathematical formulation of this?" if s < 6 else None
            ),
            "reasoning": f"Score reflects {'partial' if s < 6 else 'solid'} understanding with {'significant' if s < 5 else 'minor'} gaps.",
        }
