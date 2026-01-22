from transformers import pipeline
from django.conf import settings

_sentiment_analyzer = None
_translator = None
_summarizer = None
_ner_analyzer = None
_spam_analyzer = None

def get_sentiment_model():

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
    # 2. 모델 가져오기 
    analyzer = get_sentiment_model()
    
    # 3. 모델 예측 실행
    # 결과 예시: [{'label': 'positive', 'score': 0.95}]
    result = analyzer(headline)[0]
    
    label = result['label']
    score = result['score']
    
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
        _summarizer = pipeline("summarization", model="gogamza/kobart-summarization")
    return _summarizer

# 3. 파이프라인 함수: 번역하고 -> 요약한다
def generate_report(english_news: str):
    """
    Input: 
    출처 : https://www.investing.com/news/stock-market-news/ford-recalls-over-119000-vehicles-over-engine-block-heater-fire-risk-nhtsa-says-4456865
    
    Jan 21 (Reuters) - Ford Motor is recalling 119,075 vehicles in the U.S. 
    as the engine block heater may crack and leak coolant, potentially causing 
    a short circuit and increasing the risk of a fire when the heater is plugged in, 
    the National Highway Traffic Safety Administration said on Wednesday.

    The recall includes certain Focus, Escape, Explorer and Lincoln MKC vehicles, the agency said.
    Owners are advised not to plug in their block heaters until the vehicles are repaired, NHTSA said, 
    adding that dealers will replace the block heaters free of charge.
    
    Output: 
    """
    # 1단계: 번역 (Translation)
    translator = get_translator()
    # 긴 문장은 잘릴 수 있어서 truncation 옵션 추가
    trans_result = translator(english_news, max_length=512, truncation=True)
    korean_text = trans_result[0]['translation_text']
    
    # 2단계: 요약 (Summarization) -> 번역된 결과를 입력으로 넣음
    summarizer = get_summarizer()
    summary_result = summarizer(korean_text, max_length=100, min_length=30, truncation=True)
    summary_text = summary_result[0]['summary_text']
    
    return {
        'original': english_news,
        'translated': korean_text,
        'summary': summary_text
    }


    
def get_ner_model():
    global _ner_analyzer
    if _ner_analyzer is None:
        print("📥 [System] 고성능 NER 모델(Large) 로드 중... (약 1.3GB)")
        
        _ner_analyzer = pipeline(
            "ner", 
            model="dbmdz/bert-large-cased-finetuned-conll03-english", 
            aggregation_strategy="simple"
        )
    return _ner_analyzer

def extract_entities(text: str):
    """
    Input: "Elon Musk bought Twitter in San Francisco."
    Output: {'ORG': ['Twitter'], 'PER': ['Elon Musk'], 'LOC': ['San Francisco']}
    """
    analyzer = get_ner_model()
    results = analyzer(text)
    
    # 결과를 깔끔하게 분류해서 정리함
    entities = {
        "ORG": [],  # 조직/회사
        "PER": [],  # 사람
        "LOC": [],  # 장소
        "MISC": []  # 기타
    }
    
    for item in results:
        category = item['entity_group'] # ORG, PER, LOC 등
        word = item['word']
        
        if category in entities and word not in entities[category]:
            entities[category].append(word)
            
    return entities

def get_spam_model():
    global _spam_analyzer
    if _spam_analyzer is None:
        print("📥 [System] 스팸 탐지 모델 로드 중... (RoBERTa)")
        _spam_analyzer = pipeline(
            "text-classification", 
            model="mshenoda/roberta-spam"
        )
    return _spam_analyzer

def detect_spam(text: str):
    """
    Input: "You won $1000 cash prize! Click here."
    Output: {'label': 'SPAM', 'score': 98.5, 'korean_label': '스팸(위험)'}
    """
    analyzer = get_spam_model()
    
    # 결과 예시: [{'label': 'LABEL_1', 'score': 0.98}] 
    # (LABEL_1 = 스팸, LABEL_0 = 정상)
    result = analyzer(text)[0]
    
    label_code = result['label']
    score = result['score']
    
    if label_code == 'LABEL_1':
        final_label = 'spam'
        korean_label = '🚫 스팸 / 피싱 (위험)'
    else:
        final_label = 'ham'
        korean_label = '✅ 정상 메시지 (안전)'
        
    return {
        'label': final_label,  
        'score': round(score * 100, 2),
        'korean_label': korean_label
    }