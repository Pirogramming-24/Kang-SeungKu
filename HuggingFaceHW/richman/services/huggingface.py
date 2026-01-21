from transformers import pipeline
from django.conf import settings

_sentiment_analyzer = None
_translator = None
_summarizer = None

def get_sentiment_model():
    """
    모델을 싱글톤(Singleton)처럼 관리하는 함수입니다.
    앱이 실행되고 나서 모델을 한 번만 로드하여 메모리를 아낍니다.
    """
    global _sentiment_analyzer
    
    if _sentiment_analyzer is None:
        print("📥 [System] FinBERT 모델을 로드 중입니다... (최초 1회 실행)")
        # 금융 특화 감성 분석 모델 로드
        _sentiment_analyzer = pipeline(
            "text-classification", 
            model="ProsusAI/finbert"
        )
        print("✅ [System] 모델 로드 완료!")
        
    return _sentiment_analyzer

def analyze_news_sentiment(headline: str):
    """
    뉴스 헤드라인을 받아서 호재/악재/중립을 판단해주는 함수
    Input: "Samsung Electronics reports record profits"
    Output: {'label': 'positive', 'score': 0.95, 'korean_label': '호재'}
    """
    # 2. 모델 가져오기 (이미 로드되어 있으면 바로 가져옴)
    analyzer = get_sentiment_model()
    
    # 3. 모델 예측 실행
    # 결과 예시: [{'label': 'positive', 'score': 0.95}]
    result = analyzer(headline)[0]
    
    label = result['label']
    score = result['score']
    
    # 4. 결과를 한국어로 변환 (UI에 보여주기 위해)
    if label == 'positive':
        korean_label = '호재 🚀'
    elif label == 'negative':
        korean_label = '악재 📉'
    else:
        korean_label = '중립 😐'
        
    # 5. 최종 결과 반환
    return {
        'original_text': headline,
        'label': label,           # positive/negative/neutral
        'score': round(score * 100, 2), # 확률을 백분율로 변환 (0.95 -> 95.0)
        'korean_label': korean_label
    }

# 1. 번역 모델 로드 (영어 -> 한국어)
def get_translator():
    global _translator
    if _translator is None:
        print("📥 [System] 번역 모델 로드 중... (NHNDQ NLLB)")
        
        model_id = "NHNDQ/nllb-finetuned-en2ko"
        
        # 2. 파이프라인 생성 (주의: NLLB는 언어 코드를 지정해야 정확합니다)
        _translator = pipeline(
            "translation", 
            model=model_id, 
            src_lang="eng_Latn",  # 입력: 영어
            tgt_lang="kor_Hang"   # 출력: 한국어
        )
    return _translator

# 2. 요약 모델 로드 (한국어 요약)
def get_summarizer():
    global _summarizer
    if _summarizer is None:
        print("📥 [System] 요약 모델 로드 중... (KoBART)")
        # 한국어 요약에 특화된 모델입니다
        _summarizer = pipeline("summarization", model="gogamza/kobart-summarization")
    return _summarizer

# 3. [핵심] 파이프라인 함수: 번역하고 -> 요약한다
def generate_report(english_news: str):
    """
    Input: 긴 영어 뉴스
    Output: 번역된 한국어 전문 + 3줄 요약
    """
    # 1단계: 번역 (Translation)
    translator = get_translator()
    # 긴 문장은 잘릴 수 있어서 truncation 옵션 추가
    trans_result = translator(english_news, max_length=512, truncation=True)
    korean_text = trans_result[0]['translation_text']
    
    # 2단계: 요약 (Summarization) -> 번역된 결과를 입력으로 넣음! (이게 파이프라인!)
    summarizer = get_summarizer()
    summary_result = summarizer(korean_text, max_length=100, min_length=30, truncation=True)
    summary_text = summary_result[0]['summary_text']
    
    return {
        'original': english_news,
        'translated': korean_text,
        'summary': summary_text
    }