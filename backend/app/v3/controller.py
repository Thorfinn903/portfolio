"""
Chat Controller (v3)
Orchestrates intent -> context -> strategy -> rules -> data -> LLM polish.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
import logging
import time
import os


from app.v3.layers.intent_detection import detect_intent, rank_intents
from app.v3.layers.context_manager import ContextManager
from app.v3.layers.strategy_engine import select_strategy
from app.v3.layers.domain_rules import run_rules
from app.v3.layers.llm_polish import polish_response
from app.v3.layers.entity_extraction import extract_entities
from app.v3.persona.persona_engine import apply_dynamic_persona
from app.v3.persona.recruiter_classifier import RecruiterClassifier
from app.v3.psychology.psychology_engine import apply_psychology_layer
from app.v3.analytics.analytics_engine import AnalyticsEngine
from app.v4.state.session_manager import SessionManager


@dataclass
class ChatRequest:
    question: str
    session_id: str | None = None
    metadata: Dict[str, Any] | None = None


@dataclass
class ChatResponse:
    answer: str
    intent: str
    strategy: str
    confidence_score: float
    evidence: Any
    debug: Optional[Dict[str, Any]] = None


logger = logging.getLogger("portfolio.v3")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO)

INTENT_CONFIDENCE_THRESHOLD = 0.45

def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(value, high))


def _entity_match_strength(question: str, entities: Dict[str, Any] | None) -> float:
    if entities:
        if any(entities.get(k) for k in ["projects", "tech_stack", "roles", "domains"]):
            return 1.0
    q = (question or "").lower()
    partial_keywords = ["project", "skill", "experience", "education", "certificate", "contact", "role"]
    if any(k in q for k in partial_keywords):
        return 0.6
    return 0.3


def _freshness_bonus(question: str) -> float:
    q = (question or "").lower()
    if any(k in q for k in ["current", "latest", "recent", "present", "now"]):
        return 1.0
    return 0.7


def _confidence_breakdown(
    *,
    intent_score: float,
    evidence: Any,
    question: str,
    entities: Dict[str, Any] | None,
) -> Dict[str, float]:
    evidence_count = len(evidence or []) if isinstance(evidence, list) else 0
    evidence_strength = min(evidence_count / 3.0, 1.0)
    entity_strength = _entity_match_strength(question, entities)
    freshness_bonus = _freshness_bonus(question)
    confidence = (
        (intent_score * 0.35)
        + (evidence_strength * 0.30)
        + (entity_strength * 0.20)
        + (freshness_bonus * 0.15)
    )
    confidence = _clamp(confidence, 0.1, 0.98)
    return {
        "confidence": round(confidence, 2),
        "intent_score": round(intent_score, 2),
        "evidence_strength": round(evidence_strength, 2),
        "entity_match_strength": round(entity_strength, 2),
        "freshness_bonus": round(freshness_bonus, 2),
    }


async def handle_chat(request: ChatRequest) -> ChatResponse:
    """
    Entry point for v3 chat flow. Pure orchestration; no business logic here.
    """
    meta = request.metadata or {}
    debug_mode = bool(meta.get("debug"))
    persona_mode = bool(meta.get("persona_mode"))
    timing: Dict[str, float] = {}
    pipeline_stage_results: Dict[str, Any] = {
        "intent_detected": None,
        "entities_found": None,
        "strategy_selected": None,
        "rules_result_length": None,
        "llm_attempted": False,
        "llm_success": False,
    }
    intent_score = 0.0
    latency_guard_triggered = False
    confidence_breakdown: Dict[str, float] | None = None
    intent_overridden = False
    unknown_intent_triggered = False
    persona_transform_ms: float | None = None
    recruiter_type_detected = "unknown"
    persona_variant_used: str | None = None
    psychology_layer_used = False
    psychology_profile: str | None = None
    evidence_ranking_applied = False

    t0 = time.monotonic()
    ctx = ContextManager.load(request.session_id)

    try:
        # Intent detection with ranking + fallback mapping
        t_intent_start = time.monotonic()
        ranked = rank_intents(request.question, ctx)
        intent = ranked[0][0] if ranked else "unknown_intent"
        intent_score = ranked[0][1] if ranked else 0.0
        timing["intent_ms"] = round((time.monotonic() - t_intent_start) * 1000, 2)
        pipeline_stage_results["intent_detected"] = {"intent": intent, "score": intent_score}

        if intent_score < INTENT_CONFIDENCE_THRESHOLD:
            intent = "unknown_intent"
            intent_overridden = True
            unknown_intent_triggered = True
            pipeline_stage_results["intent_detected"] = {"intent": intent, "score": intent_score}

        # Strategy selection
        t_strategy_start = time.monotonic()
        strategy = select_strategy(intent, ctx)
        timing["strategy_ms"] = round((time.monotonic() - t_strategy_start) * 1000, 2)
        pipeline_stage_results["strategy_selected"] = strategy.get("strategy_type")

        # Rules
        t_rules_start = time.monotonic()
        raw = run_rules(request.question, intent, strategy, ctx)
        timing["rules_ms"] = round((time.monotonic() - t_rules_start) * 1000, 2)
        pipeline_stage_results["rules_result_length"] = len(raw.answer or "")

        # Intent fallback ranking if low confidence
        if intent != "unknown_intent" and intent_score < 0.55 and ranked and len(ranked) > 1:
            best_raw = raw
            best_intent = intent
            best_strategy = strategy
            best_score = raw.confidence_score
            best_intent_score = intent_score
            for candidate_intent, _score in ranked[1:3]:
                candidate_strategy = select_strategy(candidate_intent, ctx)
                candidate_raw = run_rules(request.question, candidate_intent, candidate_strategy, ctx)
                if candidate_raw.confidence_score > best_score:
                    best_raw = candidate_raw
                    best_intent = candidate_intent
                    best_strategy = candidate_strategy
                    best_score = candidate_raw.confidence_score
                    best_intent_score = _score
            intent = best_intent
            strategy = best_strategy
            raw = best_raw
            intent_score = best_intent_score
            pipeline_stage_results["intent_detected"] = {"intent": intent, "score": intent_score}
            pipeline_stage_results["strategy_selected"] = strategy.get("strategy_type")
            pipeline_stage_results["rules_result_length"] = len(raw.answer or "")

        # Recruiter type with session memory
        user_id = request.session_id or "default_user"
        recruiter_type_detected = RecruiterClassifier.classify(request.question)
        session_manager = SessionManager()
        session_manager.update_session(user_id, recruiter_type_detected)
        final_type = session_manager.get_session(user_id) or recruiter_type_detected
        recruiter_type_detected = final_type

        # Psychology layer (after rules, before persona)
        AnalyticsEngine.track_interaction(intent, final_type)
        if intent != "unknown_intent":
            raw.answer, raw.evidence, psychology_profile, psychology_layer_used = apply_psychology_layer(
                raw.answer,
                raw.evidence,
                final_type,
                intent,
            )
            evidence_ranking_applied = psychology_layer_used

        # Persona mode (between rules and LLM)
        if persona_mode:
            t_persona_start = time.monotonic()
            raw.answer, persona_variant_used = apply_dynamic_persona(
                raw.answer,
                intent,
                strategy.get("strategy_type"),
                final_type,
            )
            persona_transform_ms = round((time.monotonic() - t_persona_start) * 1000, 2)

        # Unknown intent: skip entities and LLM
        if intent == "unknown_intent":
            entities = {}
            pipeline_stage_results["entities_found"] = {}
            raw.confidence_score = 0.0
            confidence_breakdown = {
                "confidence": 0.0,
                "intent_score": round(intent_score, 2),
                "evidence_strength": 0.0,
                "entity_match_strength": 0.0,
                "freshness_bonus": 0.0,
            }
            final = await polish_response(
                request.question,
                raw,
                intent=intent,
                strategy=strategy["strategy_type"],
                allow_llm=False,
                recruiter_type=recruiter_type_detected,
            )
            unknown_intent_triggered = True
        # Latency guard (pre-LLM, pre-entities)
        elif (time.monotonic() - t0) > 2.5:
            latency_guard_triggered = True
            entities = {}
            pipeline_stage_results["entities_found"] = {}
            confidence_breakdown = _confidence_breakdown(
                intent_score=intent_score,
                evidence=raw.evidence,
                question=request.question,
                entities=entities,
            )
            raw.confidence_score = confidence_breakdown["confidence"]
            final = await polish_response(
                request.question,
                raw,
                intent=intent,
                strategy=strategy["strategy_type"],
                allow_llm=False,
                recruiter_type=recruiter_type_detected,
            )
        else:
            # Entities (guarded)
            try:
                t_entities_start = time.monotonic()
                entities = extract_entities(request.question)
                timing["entities_ms"] = round((time.monotonic() - t_entities_start) * 1000, 2)
                pipeline_stage_results["entities_found"] = entities
            except Exception:
                entities = {}
                pipeline_stage_results["entities_found"] = {}

            # Confidence (must be after rules + evidence)
            confidence_breakdown = _confidence_breakdown(
                intent_score=intent_score,
                evidence=raw.evidence,
                question=request.question,
                entities=entities,
            )
            raw.confidence_score = confidence_breakdown["confidence"]

            # LLM usage policy
            raw_len = len(raw.answer or "")
            strategy_type = strategy.get("strategy_type")
            long_answer_chars = int(os.getenv("LLM_LONG_ANSWER_CHARS", "600"))
            q_lower = (request.question or "").lower()
            summary_request = any(k in q_lower for k in ["summary", "summarize", "overview", "about", "profile", "rewrite"])
            allow_llm = (
                intent == "role_fit_evaluation"
                or strategy_type in {"comparison_strategy", "highlight_strategy"}
                or (strategy_type == "summary_strategy" and summary_request)
                or raw_len >= long_answer_chars
            )
            t_polish_start = time.monotonic()
            final = await polish_response(
                request.question,
                raw,
                intent=intent,
                strategy=strategy_type,
                allow_llm=allow_llm,
                recruiter_type=recruiter_type_detected,
            )
            timing["polish_ms"] = round((time.monotonic() - t_polish_start) * 1000, 2)
            pipeline_stage_results["llm_attempted"] = bool(final.llm_used) or (
                final.llm_error_reason in {"timeout", "error"}
            )
            pipeline_stage_results["llm_success"] = bool(final.llm_used) and not final.llm_error

    except Exception as exc:
        logger.exception("v3.handle_chat.failed")
        # Fallback strategy: minimal safe response
        intent = "unknown_intent"
        strategy = {
            "strategy_type": "summary_strategy",
            "tone_style": "professional_brief",
            "evidence_required": False,
            "confidence_required": False,
        }
        entities = {}
        try:
            raw_fallback = run_rules(request.question, intent, strategy, ctx)
        except Exception:
            raw_fallback = type(
                "RawAnswerFallback",
                (),
                {
                    "answer": "A concise portfolio summary is available.",
                    "evidence": [{"source": "system", "note": "fallback_no_data"}],
                    "confidence_score": 0.1,
                },
            )()
        confidence_breakdown = _confidence_breakdown(
            intent_score=0.0,
            evidence=raw_fallback.evidence,
            question=request.question,
            entities={},
        )
        raw_fallback.confidence_score = confidence_breakdown["confidence"]
        final = await polish_response(
            request.question,
            raw_fallback,
            intent=intent,
            strategy=strategy["strategy_type"],
            allow_llm=False,
        )
        timing["error"] = str(exc)

    ContextManager.update(
        request.session_id,
        current_page=meta.get("current_page"),
        last_project_viewed=meta.get("last_project_viewed")
        or (entities.get("projects") or [None])[0],
        last_entities=entities,
        intent=intent,
        question=request.question,
    )

    timing["total_ms"] = round((time.monotonic() - t0) * 1000, 2)
    logger.info(
        "v3.chat",
        extra={
            "intent": intent,
            "strategy": strategy["strategy_type"],
            "confidence": final.confidence_score,
            "timing_ms": timing,
        },
    )

    debug_payload = None
    if debug_mode:
        debug_payload = {
            "timing_ms": timing,
            "llm_used": final.llm_used,
            "llm_error": final.llm_error,
            "llm_error_reason": final.llm_error_reason,
            "persona_mode_used": persona_mode,
            "persona_transform_ms": persona_transform_ms,
            "recruiter_type_detected": recruiter_type_detected,
            "persona_variant_used": persona_variant_used,
            "psychology_layer_used": psychology_layer_used,
            "psychology_profile": psychology_profile,
            "evidence_ranking_applied": evidence_ranking_applied,
            "llm_status": final.llm_status,
            "intent_score": intent_score,
            "intent_overridden": intent_overridden,
            "unknown_intent_triggered": unknown_intent_triggered,
            "intent_threshold": INTENT_CONFIDENCE_THRESHOLD,
            "latency_guard_triggered": latency_guard_triggered,
            "pipeline_stage_results": pipeline_stage_results,
            "confidence_breakdown": {
                "intent_score": (confidence_breakdown or {}).get("intent_score"),
                "evidence_strength": (confidence_breakdown or {}).get("evidence_strength"),
                "entity_match_strength": (confidence_breakdown or {}).get("entity_match_strength"),
                "freshness_bonus": (confidence_breakdown or {}).get("freshness_bonus"),
            },
        }

    return ChatResponse(
        answer=final.answer,
        intent=intent,
        strategy=strategy["strategy_type"],
        confidence_score=final.confidence_score,
        evidence=final.evidence,
        debug=debug_payload,
    )
