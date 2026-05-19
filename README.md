# English Basic Verbs

영어 초급자가 자주 쓰는 기본 동사의 뜻, 과거형, 과거분사를 학습하는 CLI 프로그램입니다.

## 기능

- 기본 동사 80개 이상 제공
- 영어 원형/과거형/과거분사/한국어 뜻/예문 조회
- 영어 또는 한국어 검색
- 과거형, 과거분사, 한국어 뜻 퀴즈
- 대소문자와 불필요한 공백을 무시한 정답 판정

## 실행

```bash
python3 -m english_basic_verbs list
python3 -m english_basic_verbs search 먹다
python3 -m english_basic_verbs quiz --limit 5 --mode past-tense
python3 -m english_basic_verbs quiz --limit 5 --mode korean-meaning --seed 7
```

## 테스트

```bash
python3 -m unittest discover -s tests
```
