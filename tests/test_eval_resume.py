"""A retomada da avaliação decide quanta cota do Gemini se gasta: precisa de teste."""

import json
from types import SimpleNamespace

import pytest

from evals.run_eval import USE_CASES, answered_counts, load_previous, plan_calls

CASES = [SimpleNamespace(name="a"), SimpleNamespace(name="b")]
USES = list(USE_CASES)


def record(use_case, case, error=None):
    return {"use_case": use_case, "case": case, **({"error": error} if error else {})}


def test_without_previous_results_plans_every_call():
    plan = plan_calls(CASES, reps=2)

    assert len(plan) == len(CASES) * len(USES) * 2


def test_skips_calls_that_already_have_an_answer():
    previous = [record("trilha", "a"), record("trilha", "a"), record("guia", "a")]

    plan = plan_calls(CASES, reps=2, previous=previous)

    names = [(use, case.name) for use, case in plan]
    assert ("trilha", "a") not in names
    assert names.count(("guia", "a")) == 1
    assert names.count(("analise", "a")) == 2
    assert names.count(("trilha", "b")) == 2


@pytest.mark.parametrize(
    "error", ["ai_quota_exceeded", "ai_timeout", "ai_provider_error", "ai_unavailable"]
)
def test_infrastructure_failures_are_planned_again(error):
    previous = [record("trilha", "a", error), record("trilha", "a", error)]

    plan = plan_calls([CASES[0]], reps=2, previous=previous)

    assert [use for use, _ in plan].count("trilha") == 2


def test_an_answer_that_failed_the_checks_still_counts_as_answered():
    """Um erro de conteúdo (ex.: saída fora do schema) é resultado da avaliação, não da infra."""
    previous = [record("trilha", "a", "ai_invalid_response"), record("trilha", "a")]

    plan = plan_calls([CASES[0]], reps=2, previous=previous)

    assert "trilha" not in [use for use, _ in plan]


def test_never_plans_more_than_the_repetitions_even_with_extra_answers():
    previous = [record("trilha", "a")] * 5

    plan = plan_calls([CASES[0]], reps=2, previous=previous)

    assert "trilha" not in [use for use, _ in plan]


def test_answered_counts_ignores_infrastructure_failures():
    counts = answered_counts([record("guia", "a"), record("guia", "a", "ai_quota_exceeded")])

    assert counts[("guia", "a")] == 1


def write_result(tmp_path, model="gemini-2.5-flash", thinking_budget=0):
    path = tmp_path / "result.json"
    path.write_text(
        json.dumps(
            {"model": model, "thinking_budget": thinking_budget, "records": [record("guia", "a")]}
        )
    )
    return str(path)


def test_load_previous_returns_the_records(tmp_path):
    path = write_result(tmp_path)

    assert load_previous(path, "gemini-2.5-flash", 0) == [record("guia", "a")]


@pytest.mark.parametrize(
    ("model", "thinking_budget"), [("gemini-2.5-pro", 0), ("gemini-2.5-flash", -1)]
)
def test_load_previous_refuses_a_different_configuration(tmp_path, model, thinking_budget):
    path = write_result(tmp_path)

    with pytest.raises(SystemExit, match="--resume"):
        load_previous(path, model, thinking_budget)
