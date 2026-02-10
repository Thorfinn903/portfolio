from app.v3.persona.recruiter_classifier import detect_recruiter_type
from app.v3.persona.persona_engine import apply_dynamic_persona


def test_recruiter_classifier_hr():
    q = "Is he a good cultural fit?"
    assert detect_recruiter_type(q, {}) == "hr_recruiter"


def test_recruiter_classifier_technical():
    q = "How strong is he in backend architecture?"
    assert detect_recruiter_type(q, {}) == "technical_reviewer"


def test_recruiter_classifier_founder():
    q = "Can he build scalable backend for startup?"
    assert detect_recruiter_type(q, {}) == "founder_cto"


def test_persona_output_hr():
    answer, variant = apply_dynamic_persona(
        "base", "about_query", "summary_strategy", "hr_recruiter"
    )
    assert variant == "hr"
    assert "FastAPI" in answer


def test_persona_output_technical():
    answer, variant = apply_dynamic_persona(
        "base", "about_query", "summary_strategy", "technical_reviewer"
    )
    assert variant == "technical"
    assert "REST APIs" in answer or "database" in answer


def test_persona_output_founder():
    answer, variant = apply_dynamic_persona(
        "base", "about_query", "summary_strategy", "founder_cto"
    )
    assert variant == "founder"
    assert "business" in answer.lower() or "product" in answer.lower()
