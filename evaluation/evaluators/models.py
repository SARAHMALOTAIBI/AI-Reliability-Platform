from dataclasses import dataclass


@dataclass(frozen=True)
class ScoreResult:
    score: float
    explanation: str

    def __post_init__(self) -> None:
        if not 0.0 <= self.score <= 1.0:
            raise ValueError(
                "Score must be between 0 and 1."
            )


@dataclass(frozen=True)
class NumericEvaluationResult:
    score: float
    contradiction: bool
    explanation: str
    unsupported_answer_values: tuple[float, ...]

    def __post_init__(self) -> None:
        if not 0.0 <= self.score <= 1.0:
            raise ValueError(
                "Score must be between 0 and 1."
            )


@dataclass(frozen=True)
class StatusResult:
    status: str
    explanation: str