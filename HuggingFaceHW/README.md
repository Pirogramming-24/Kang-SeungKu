# 나만의 AI 사이트 (Django)

---
## 사용 모델 (3개 이상)

### 1. ProsusAI/finbert
- **태스크**: Financial Sentiment Analysis (금융 특화 감성 분석)
- **입력 예시**: "Samsung Electronics reports record profits for Q3."
- **출력 예시**: `{'label': 'positive', 'score': 95.0, 'korean_label': '호재 🚀'}`
- **설명**: 일반적인 감성 분석이 아닌, 금융 문맥(Financial Context)을 이해하여 호재/악재/중립을 판단함.
- **실행 화면 예시**: (감성 분석 결과 화면 스크린샷 위치)

### 2. dbmdz/bert-large-cased-finetuned-conll03-english
- **태스크**: Named Entity Recognition (NER, 핵심 정보 추출)
- **입력 예시**: "Elon Musk announced that Tesla will build a new factory in Mexico."
- **출력 예시**: `{'ORG': ['Tesla'], 'PER': ['Elon Musk'], 'LOC': ['Mexico']}`
- **설명**: 뉴스 텍스트에서 기업(ORG), 인물(PER), 장소(LOC) 등의 고유명사를 식별하여 시각화 태그로 제공. (Base 모델 대비 인물 식별 정확도 향상)
- **실행 화면 예시**: (NER 결과 화면 스크린샷 위치)

### 3. mshenoda/roberta-spam
- **태스크**: Spam/Phishing Detection (스팸 및 피싱 탐지)
- **입력 예시**: "Congratulations! You won $1,000 Walmart gift card. Click link to claim!"
- **출력 예시**: `{'label': 'spam', 'score': 98.5, 'korean_label': '🚫 스팸 / 피싱 (위험)'}`
- **설명**: 금융 사기 문자나 피싱 이메일 패턴을 분석하여 스팸 여부와 위험도를 백분율로 진단.
- **실행 화면 예시**: (스팸 탐지 결과 화면 스크린샷 위치)

### 4. NHNDQ/nllb-finetuned-en2ko + daekeun-ml/ko-summary-t5 (Pipeline)
- **태스크**: Translation & Summarization (글로벌 뉴스 리포트)
- **입력 예시**: (장문의 영어 뉴스 기사)
- **출력 예시**: (한국어로 번역된 후 3줄로 요약된 텍스트)
- **설명**: 번역 모델(NLLB)과 요약 모델(T5)을 직렬로 연결하여 영어 뉴스를 한국어 핵심 요약본으로 변환.

---
## 로그인 제한(Access Control)

- 비로그인 사용자는 **1개 탭(시장 감성 분석)만 사용 가능**
- 제한 탭(스팸, NER, 리포트) 접근 시 **“로그인 후 이용해주세요” alert 후 로그인 페이지로 이동**
- 로그인 성공 시 **원래 페이지로 복귀(next 파라미터 적용)**

---
## 구현 체크리스트

- [x] 탭 3개 이상(감성, 스팸, NER, 리포트) + 각 탭 별 URL 분리
- [x] 각 탭: 입력 → 실행 → 결과 출력 (AJAX 비동기 처리 완료)
- [x] 에러 처리: 모델 호출 실패 시 사용자에게 alert 메시지 표시
- [x] 로딩 표시: 버튼 내 “처리 중…” 텍스트 및 로딩 인디케이터 적용
- [x] 요청 히스토리: 로그인 유저 대상 DB 저장 및 마이페이지 조회 기능 구현
- [x] `.env` 사용 (또는 settings.py 내 환경 설정 분리)
- [x] `README.md`에 모델 정보/사용 예시/실행 방법 작성 후 GitHub push

### 로그인 제한 체크
- [x] 비로그인 사용자는 1개 탭(공개 탭)만 접근 가능
- [x] 제한 탭 접근 시 alert 후 로그인 페이지로 redirect (`login_required_alert` 유틸리티 구현)
- [x] 로그인 성공 시 원래 페이지로 복귀 (Login View의 next 처리)

## 프로젝트 구조 (Directory Tree)

```text
HuggingFaceHW
├── config
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── __init__.py
├── manage.py
├── README.md
├── requirements.txt
└── richman
    ├── admin.py
    ├── apps.py
    ├── migrations
    │   └── __init__.py
    ├── models.py
    ├── services
    │   └── huggingface.py
    ├── static
    │   ├── css
    │   │   └── style.css
    │   └── js
    ├── templates
    │   ├── registration
    │   │   ├── login.html
    │   │   └── signup.html
    │   ├── alert_login.html
    │   ├── history.html
    │   ├── main.html
    │   ├── ner.html
    │   ├── report.html
    │   ├── sentiment.html
    │   └── spam.html
    ├── tests.py
    ├── urls.py
    ├── utils.py
    ├── views.py
    └── __init__.py