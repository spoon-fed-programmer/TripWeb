import unittest

from english_basic_verbs.application import QuizService, StudySession
from english_basic_verbs.data import create_default_repository
from english_basic_verbs.domain import Answer, QuizMode


class BasicVerbRepositoryTests(unittest.TestCase):
    def test_default_repository_contains_core_beginner_verbs(self):
        repository = create_default_repository()

        verbs = repository.list_all()
        bases = {verb.base for verb in verbs}

        self.assertGreaterEqual(len(verbs), 20)
        self.assertIn("be", bases)
        self.assertIn("go", bases)
        self.assertIn("have", bases)

    def test_search_matches_english_forms_and_korean_meanings(self):
        repository = create_default_repository()

        by_past = repository.search("went")
        by_korean = repository.search("먹다")

        self.assertEqual([verb.base for verb in by_past], ["go"])
        self.assertEqual([verb.base for verb in by_korean], ["eat"])


class QuizServiceTests(unittest.TestCase):
    def test_creates_question_for_past_tense(self):
        repository = create_default_repository()
        service = QuizService(repository)

        question = service.create_question("go", QuizMode.PAST_TENSE)

        self.assertEqual(question.prompt, "'go'의 과거형은?")
        self.assertEqual(question.expected, Answer("went"))
        self.assertEqual(question.verb.base, "go")

    def test_answer_evaluation_ignores_case_and_extra_spaces(self):
        repository = create_default_repository()
        service = QuizService(repository)
        question = service.create_question("go", QuizMode.PAST_TENSE)

        result = service.evaluate(question, "  WENT  ")

        self.assertTrue(result.is_correct)
        self.assertEqual(result.correct_answer, "went")

    def test_meaning_question_accepts_one_of_multiple_meanings(self):
        repository = create_default_repository()
        service = QuizService(repository)
        question = service.create_question("take", QuizMode.KOREAN_MEANING)

        result = service.evaluate(question, "가지다")

        self.assertTrue(result.is_correct)


class StudySessionTests(unittest.TestCase):
    def test_session_builds_repeatable_questions_and_tracks_score(self):
        repository = create_default_repository()
        service = QuizService(repository)
        session = StudySession(service, seed=7)

        questions = session.start(limit=3, mode=QuizMode.PAST_TENSE)

        self.assertEqual(len(questions), 3)
        first_result = session.answer(questions[0].id, questions[0].expected.primary)
        second_result = session.answer(questions[1].id, "wrong answer")

        self.assertTrue(first_result.is_correct)
        self.assertFalse(second_result.is_correct)
        self.assertEqual(session.score.correct, 1)
        self.assertEqual(session.score.total_answered, 2)


if __name__ == "__main__":
    unittest.main()
