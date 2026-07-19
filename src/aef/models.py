"""Modelos de domínio sem dependências externas."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import IntEnum
from typing import Any


class Severity(IntEnum):
    CRITICAL = 50
    HIGH = 40
    MEDIUM = 30
    LOW = 20
    INFO = 10

    @property
    def label(self) -> str:
        return {
            Severity.CRITICAL: "crítico",
            Severity.HIGH: "alto",
            Severity.MEDIUM: "médio",
            Severity.LOW: "baixo",
            Severity.INFO: "informativo",
        }[self]


@dataclass(frozen=True)
class Issue:
    code: str
    message: str
    severity: Severity
    path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["severity"] = self.severity.label
        return data


@dataclass
class ValidationReport:
    issues: list[Issue] = field(default_factory=list)
    checks: dict[str, int] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return not any(issue.severity >= Severity.HIGH for issue in self.issues)

    def add(self, issue: Issue) -> None:
        self.issues.append(issue)

    def count(self, check: str, amount: int = 1) -> None:
        self.checks[check] = self.checks.get(check, 0) + amount

    def to_dict(self) -> dict[str, Any]:
        ordered = sorted(self.issues, key=lambda item: (-item.severity, item.code))
        return {
            "status": "aprovado" if self.passed else "reprovado",
            "checks": self.checks,
            "summary": {
                severity.label: sum(1 for issue in self.issues if issue.severity == severity)
                for severity in Severity
            },
            "issues": [issue.to_dict() for issue in ordered],
        }

