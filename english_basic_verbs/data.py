from __future__ import annotations

from english_basic_verbs.application import VerbRepository
from english_basic_verbs.domain import BasicVerb, normalize_answer


class InMemoryVerbRepository(VerbRepository):
    def __init__(self, verbs: list[BasicVerb]):
        self._verbs = tuple(verbs)
        self._by_base = {normalize_answer(verb.base): verb for verb in verbs}

    def list_all(self) -> list[BasicVerb]:
        return list(self._verbs)

    def find_by_base(self, base: str) -> BasicVerb | None:
        return self._by_base.get(normalize_answer(base))

    def search(self, query: str) -> list[BasicVerb]:
        normalized_query = normalize_answer(query)
        if not normalized_query:
            return []

        return [
            verb
            for verb in self._verbs
            if self._matches(verb, normalized_query)
        ]

    @staticmethod
    def _matches(verb: BasicVerb, normalized_query: str) -> bool:
        searchable_values = (
            verb.base,
            verb.past,
            verb.past_participle,
            *verb.meanings,
            verb.example,
        )
        return any(
            normalized_query in normalize_answer(value)
            for value in searchable_values
        )


def create_default_repository() -> InMemoryVerbRepository:
    return InMemoryVerbRepository(
        [
            BasicVerb("be", "was/were", "been", ("이다", "있다"), "I am a student."),
            BasicVerb("have", "had", "had", ("가지다",), "We have breakfast."),
            BasicVerb("do", "did", "done", ("하다",), "Do your homework."),
            BasicVerb("say", "said", "said", ("말하다",), "She said hello."),
            BasicVerb("go", "went", "gone", ("가다",), "They go to school."),
            BasicVerb("get", "got", "gotten", ("얻다", "받다"), "I got a letter."),
            BasicVerb("make", "made", "made", ("만들다",), "Make a cake."),
            BasicVerb("know", "knew", "known", ("알다",), "I know the answer."),
            BasicVerb("think", "thought", "thought", ("생각하다",), "Think about it."),
            BasicVerb("take", "took", "taken", ("가지다", "데려가다", "가져가다"), "Take an umbrella."),
            BasicVerb("see", "saw", "seen", ("보다",), "I saw a movie."),
            BasicVerb("come", "came", "come", ("오다",), "Come here."),
            BasicVerb("want", "wanted", "wanted", ("원하다",), "I want water."),
            BasicVerb("look", "looked", "looked", ("보다", "바라보다"), "Look at the sky."),
            BasicVerb("use", "used", "used", ("사용하다",), "Use this pen."),
            BasicVerb("find", "found", "found", ("찾다", "발견하다"), "Find your keys."),
            BasicVerb("give", "gave", "given", ("주다",), "Give me a call."),
            BasicVerb("tell", "told", "told", ("말하다", "알려주다"), "Tell me the truth."),
            BasicVerb("work", "worked", "worked", ("일하다", "작동하다"), "I work at home."),
            BasicVerb("call", "called", "called", ("부르다", "전화하다"), "Call your friend."),
            BasicVerb("try", "tried", "tried", ("시도하다", "노력하다"), "Try again."),
            BasicVerb("ask", "asked", "asked", ("묻다", "요청하다"), "Ask a question."),
            BasicVerb("need", "needed", "needed", ("필요하다",), "I need help."),
            BasicVerb("feel", "felt", "felt", ("느끼다",), "I feel happy."),
            BasicVerb("become", "became", "become", ("되다",), "Become a teacher."),
            BasicVerb("leave", "left", "left", ("떠나다", "남기다"), "Leave the room."),
            BasicVerb("put", "put", "put", ("놓다", "두다"), "Put it on the table."),
            BasicVerb("mean", "meant", "meant", ("의미하다",), "What does it mean?"),
            BasicVerb("keep", "kept", "kept", ("유지하다", "간직하다"), "Keep the change."),
            BasicVerb("let", "let", "let", ("허락하다",), "Let me help."),
            BasicVerb("begin", "began", "begun", ("시작하다",), "Begin the lesson."),
            BasicVerb("help", "helped", "helped", ("돕다",), "Help your family."),
            BasicVerb("talk", "talked", "talked", ("말하다", "이야기하다"), "Talk to me."),
            BasicVerb("turn", "turned", "turned", ("돌다", "바꾸다"), "Turn left."),
            BasicVerb("start", "started", "started", ("시작하다",), "Start now."),
            BasicVerb("show", "showed", "shown", ("보여주다",), "Show your work."),
            BasicVerb("hear", "heard", "heard", ("듣다",), "I heard music."),
            BasicVerb("play", "played", "played", ("놀다", "연주하다"), "Play the piano."),
            BasicVerb("run", "ran", "run", ("달리다", "운영하다"), "Run fast."),
            BasicVerb("move", "moved", "moved", ("움직이다", "이사하다"), "Move the chair."),
            BasicVerb("live", "lived", "lived", ("살다",), "I live in Seoul."),
            BasicVerb("believe", "believed", "believed", ("믿다",), "Believe in yourself."),
            BasicVerb("bring", "brought", "brought", ("가져오다",), "Bring your book."),
            BasicVerb("write", "wrote", "written", ("쓰다",), "Write your name."),
            BasicVerb("sit", "sat", "sat", ("앉다",), "Sit down."),
            BasicVerb("stand", "stood", "stood", ("서다",), "Stand up."),
            BasicVerb("lose", "lost", "lost", ("잃다", "지다"), "Do not lose hope."),
            BasicVerb("pay", "paid", "paid", ("지불하다",), "Pay the bill."),
            BasicVerb("meet", "met", "met", ("만나다",), "Meet your teacher."),
            BasicVerb("include", "included", "included", ("포함하다",), "Include your name."),
            BasicVerb("continue", "continued", "continued", ("계속하다",), "Continue reading."),
            BasicVerb("set", "set", "set", ("놓다", "설정하다"), "Set the table."),
            BasicVerb("learn", "learned", "learned", ("배우다",), "Learn English."),
            BasicVerb("change", "changed", "changed", ("바꾸다", "변하다"), "Change your plan."),
            BasicVerb("lead", "led", "led", ("이끌다",), "Lead the team."),
            BasicVerb("understand", "understood", "understood", ("이해하다",), "I understand you."),
            BasicVerb("watch", "watched", "watched", ("보다", "지켜보다"), "Watch TV."),
            BasicVerb("follow", "followed", "followed", ("따르다",), "Follow me."),
            BasicVerb("stop", "stopped", "stopped", ("멈추다",), "Stop here."),
            BasicVerb("create", "created", "created", ("창조하다", "만들다"), "Create a story."),
            BasicVerb("speak", "spoke", "spoken", ("말하다",), "Speak slowly."),
            BasicVerb("read", "read", "read", ("읽다",), "Read a book."),
            BasicVerb("spend", "spent", "spent", ("쓰다", "보내다"), "Spend time wisely."),
            BasicVerb("grow", "grew", "grown", ("자라다", "기르다"), "Grow a plant."),
            BasicVerb("open", "opened", "opened", ("열다",), "Open the door."),
            BasicVerb("walk", "walked", "walked", ("걷다",), "Walk to school."),
            BasicVerb("win", "won", "won", ("이기다",), "Win the game."),
            BasicVerb("offer", "offered", "offered", ("제공하다", "제안하다"), "Offer help."),
            BasicVerb("remember", "remembered", "remembered", ("기억하다",), "Remember this word."),
            BasicVerb("love", "loved", "loved", ("사랑하다", "좋아하다"), "Love your work."),
            BasicVerb("consider", "considered", "considered", ("고려하다",), "Consider the idea."),
            BasicVerb("appear", "appeared", "appeared", ("나타나다",), "Stars appear at night."),
            BasicVerb("buy", "bought", "bought", ("사다",), "Buy some milk."),
            BasicVerb("wait", "waited", "waited", ("기다리다",), "Wait a minute."),
            BasicVerb("serve", "served", "served", ("제공하다", "섬기다"), "Serve dinner."),
            BasicVerb("die", "died", "died", ("죽다",), "Plants die without water."),
            BasicVerb("send", "sent", "sent", ("보내다",), "Send an email."),
            BasicVerb("expect", "expected", "expected", ("기대하다", "예상하다"), "Expect a call."),
            BasicVerb("build", "built", "built", ("짓다", "만들다"), "Build a house."),
            BasicVerb("stay", "stayed", "stayed", ("머무르다",), "Stay at home."),
            BasicVerb("fall", "fell", "fallen", ("떨어지다", "넘어지다"), "Leaves fall in autumn."),
            BasicVerb("cut", "cut", "cut", ("자르다",), "Cut the paper."),
            BasicVerb("reach", "reached", "reached", ("도착하다", "도달하다"), "Reach the goal."),
            BasicVerb("kill", "killed", "killed", ("죽이다",), "Do not kill time."),
            BasicVerb("remain", "remained", "remained", ("남다",), "Remain calm."),
            BasicVerb("eat", "ate", "eaten", ("먹다",), "Eat an apple."),
        ]
    )
