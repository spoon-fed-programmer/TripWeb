from __future__ import annotations

import argparse

from english_basic_verbs.application import QuizService, StudySession
from english_basic_verbs.data import create_default_repository
from english_basic_verbs.domain import QuizMode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="english-basic-verbs",
        description="영어 기본 동사의 뜻, 과거형, 과거분사를 학습합니다.",
    )
    subcommands = parser.add_subparsers(dest="command")

    subcommands.add_parser("list", help="학습 가능한 기본 동사 목록을 보여줍니다.")

    search_parser = subcommands.add_parser("search", help="동사나 한국어 뜻으로 검색합니다.")
    search_parser.add_argument("query", help="검색어")

    quiz_parser = subcommands.add_parser("quiz", help="대화형 퀴즈를 시작합니다.")
    quiz_parser.add_argument("--limit", type=int, default=5, help="출제할 문제 수")
    quiz_parser.add_argument(
        "--mode",
        choices=[mode.value for mode in QuizMode],
        default=QuizMode.PAST_TENSE.value,
        help="퀴즈 유형",
    )
    quiz_parser.add_argument("--seed", type=int, default=None, help="반복 가능한 문제 순서용 시드")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    repository = create_default_repository()
    service = QuizService(repository)

    if args.command == "list":
        for verb in repository.list_all():
            meanings = ", ".join(verb.meanings)
            print(f"{verb.base:<12} {verb.past:<12} {verb.past_participle:<12} {meanings}")
        return 0

    if args.command == "search":
        matches = repository.search(args.query)
        if not matches:
            print("검색 결과가 없습니다.")
            return 1
        for verb in matches:
            meanings = ", ".join(verb.meanings)
            print(f"{verb.base}: {meanings} / 과거형 {verb.past} / 과거분사 {verb.past_participle}")
        return 0

    if args.command == "quiz":
        return run_quiz(service, limit=args.limit, mode=QuizMode(args.mode), seed=args.seed)

    parser.print_help()
    return 0


def run_quiz(service: QuizService, limit: int, mode: QuizMode, seed: int | None) -> int:
    session = StudySession(service, seed=seed)
    questions = session.start(limit=limit, mode=mode)

    for index, question in enumerate(questions, start=1):
        print(f"\n문제 {index}. {question.prompt}")
        user_answer = input("답: ")
        result = session.answer(question.id, user_answer)
        if result.is_correct:
            print("정답입니다!")
        else:
            print(f"오답입니다. 정답: {result.correct_answer}")
        print(f"예문: {question.verb.example}")

    percent = session.score.accuracy * 100
    print(
        f"\n결과: {session.score.correct}/{session.score.total_answered} "
        f"({percent:.0f}%)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
