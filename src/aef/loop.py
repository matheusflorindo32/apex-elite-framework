"""Controle determinístico de iterações e condições de parada."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IterationState:
    cycle: int
    max_cycles: int
    critical_or_high_open: int
    mandatory_criteria_open: int
    progress_score: float
    no_progress_cycles: int = 0


def stop_reason(state: IterationState) -> str | None:
    if state.mandatory_criteria_open == 0 and state.critical_or_high_open == 0:
        return "quality-gate-passed"
    if state.cycle >= state.max_cycles:
        return "cycle-budget-exhausted"
    if state.no_progress_cycles >= 2:
        return "no-measurable-progress"
    return None
