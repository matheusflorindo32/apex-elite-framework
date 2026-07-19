from aef.loop import IterationState, stop_reason


def test_stops_when_quality_gate_passes():
    state = IterationState(1, 3, critical_or_high_open=0, mandatory_criteria_open=0, progress_score=1.0)
    assert stop_reason(state) == "quality-gate-passed"


def test_stops_when_budget_is_exhausted():
    state = IterationState(3, 3, critical_or_high_open=1, mandatory_criteria_open=1, progress_score=0.5)
    assert stop_reason(state) == "cycle-budget-exhausted"


def test_stops_after_two_cycles_without_progress():
    state = IterationState(2, 3, critical_or_high_open=1, mandatory_criteria_open=1, progress_score=0.5, no_progress_cycles=2)
    assert stop_reason(state) == "no-measurable-progress"


def test_continues_while_progress_is_possible():
    state = IterationState(1, 3, critical_or_high_open=1, mandatory_criteria_open=1, progress_score=0.5, no_progress_cycles=0)
    assert stop_reason(state) is None

