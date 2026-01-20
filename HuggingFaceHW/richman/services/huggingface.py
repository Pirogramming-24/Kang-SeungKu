from transformers import pipeline
from django.conf import settings

# 1. 모델을 전역 변수로 선언 (Why? 성능 최적화)
# 처음에는 비어있지만, 한 번 로드되면 메모리에 계속 상주합니다.
_sentiment_analyzer = None

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