from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Protocol

from english_basic_verbs.domain import (
    BasicVerb,
    EvaluationResult,
    Question,
    QuizMode,
    Score,
)


class VerbRepository(Protocol):
    def list_all(self) -> list[BasicVerb]:
        raise NotImplementedError

    def find_by_base(self, base: str) -> BasicVerb | None:
        raise NotImplementedError

    def search(self, query: str) -> list[BasicVerb]:
        raise NotImplementedError


class QuizService:
    def __init__(self, repository: VerbRepository):
        self._repository = repository

    def create_question(self, base: str, mode: QuizMode) -> Question:
        verb = self._repository.find_by_base(base)
        if verb is None:
            raise ValueError(f"Unknown verb: {base}")
        return self._build_question(verb, mode)

    def create_questions(self, limit: int, mode: QuizMode, seed: int | None = None) -> list[Question]:
        if limit < 1:
            raise ValueError("limit must be greater than zero")

        verbs = self._repository.list_all()
        if not verbs:
            return []

        selected_verbs = verbs[:]
        random.Random(seed).shuffle(selected_verbs)
        return [
            self._build_question(verb, mode, sequence=index + 1)
            for index, verb in enumerate(selected_verbs[:limit])
        ]

    def evaluate(self, question: Question, user_answer: str) -> EvaluationResult:
        is_correct = question.expected.matches(user_answer)
        return EvaluationResult(
            question_id=question.id,
            user_answer=user_answer,
            correct_answer=question.expected.primary,
            is_correct=is_correct,
        )

    def _build_question(
        self,
        verb: BasicVerb,
        mode: QuizMode,
        sequence: int | None = None,
    ) -> Question:
        prompt = self._prompt_for(verb, mode)
        suffix = f":{sequence}" if sequence is not None else ""
        return Question(
            id=f"{verb.base}:{mode.value}{suffix}",
            prompt=prompt,
            expected=verb.answer_for(mode),
            verb=verb,
            mode=mode,
        )

    @staticmethod
    def _prompt_for(verb: BasicVerb, mode: QuizMode) -> str:
        if mode == QuizMode.PAST_TENSE:
            return f"'{verb.base}'의 과거형은?"
        if mode == QuizMode.PAST_PARTICIPLE:
            return f"'{verb.base}'의 과거분사는?"
        if mode == QuizMode.KOREAN_MEANING:
            return f"'{verb.base}'의 한국어 뜻은?"
        raise ValueError(f"Unsupported quiz mode: {mode}")


@dataclass
class StudySession:
    quiz_service: QuizService
    seed: int | None = None

    def __post_init__(self) -> None:
        self._questions_by_id: dict[str, Question] = {}
        self.score = Score()

    def start(self, limit: int = 5, mode: QuizMode = QuizMode.PAST_TENSE) -> list[Question]:
        questions = self.quiz_service.create_questions(limit=limit, mode=mode, seed=self.seed)
        self._questions_by_id = {question.id: question for question in questions}
        self.score = Score()
        return questions

    def answer(self, question_id: str, user_answer: str) -> EvaluationResult:
        try:
            question = self._questions_by_id[question_id]
        except KeyError as exc:
            raise ValueError(f"Unknown question id: {question_id}") from exc

        result = self.quiz_service.evaluate(question, user_answer)
        self.score = self.score.record(result.is_correct)
        return result
