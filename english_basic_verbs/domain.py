from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class QuizMode(str, Enum):
    PAST_TENSE = "past-tense"
    PAST_PARTICIPLE = "past-participle"
    KOREAN_MEANING = "korean-meaning"


def normalize_answer(value: str) -> str:
    return " ".join(value.strip().casefold().split())


@dataclass(frozen=True)
class Answer:
    primary: str
    alternatives: tuple[str, ...] = field(default_factory=tuple)

    def matches(self, user_input: str) -> bool:
        normalized_input = normalize_answer(user_input)
        return normalized_input in {
            normalize_answer(answer) for answer in self.accepted_values
        }

    @property
    def accepted_values(self) -> tuple[str, ...]:
        return (self.primary, *self.alternatives)


@dataclass(frozen=True)
class BasicVerb:
    base: str
    past: str
    past_participle: str
    meanings: tuple[str, ...]
    example: str

    def answer_for(self, mode: QuizMode) -> Answer:
        if mode == QuizMode.PAST_TENSE:
            return Answer(self.past)
        if mode == QuizMode.PAST_PARTICIPLE:
            return Answer(self.past_participle)
        if mode == QuizMode.KOREAN_MEANING:
            return Answer(self.meanings[0], self.meanings[1:])
        raise ValueError(f"Unsupported quiz mode: {mode}")


@dataclass(frozen=True)
class Question:
    id: str
    prompt: str
    expected: Answer
    verb: BasicVerb
    mode: QuizMode


@dataclass(frozen=True)
class EvaluationResult:
    question_id: str
    user_answer: str
    correct_answer: str
    is_correct: bool


@dataclass(frozen=True)
class Score:
    correct: int = 0
    total_answered: int = 0

    @property
    def incorrect(self) -> int:
        return self.total_answered - self.correct

    @property
    def accuracy(self) -> float:
        if self.total_answered == 0:
            return 0.0
        return self.correct / self.total_answered

    def record(self, is_correct: bool) -> "Score":
        return Score(
            correct=self.correct + int(is_correct),
            total_answered=self.total_answered + 1,
        )
