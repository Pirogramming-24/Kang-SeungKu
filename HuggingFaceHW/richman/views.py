from django.shortcuts import render
from django.http import JsonResponse
from .services.huggingface import analyze_news_sentiment, generate_report
# 1. 메인 대시보드
def main(request):
    return render(request, 'main.html')

# 2. [기능 1] 감성 분석 페이지 (화면 보여주기)
def sentiment_view(request):
    return render(request, 'sentiment.html')

# 3. [기능 1-동작] 실제 감성 분석 실행 (AJAX 요청 처리)
# sentiment.html의 자바스크립트가 여기로 데이터를 보냅니다.
def analyze_view(request):
    if request.method == "POST":
        text = request.POST.get('text', '')
        result = analyze_news_sentiment(text)
        return JsonResponse(result)
    return JsonResponse({'error': '잘못된 접근입니다.'}, status=400)

# 4. [기능 2] 스팸 분류 페이지 (껍데기)
def spam_view(request):
    return render(request, 'spam.html')

# 5. [기능 3] NER 페이지 (껍데기)
def ner_view(request):
    return render(request, 'ner.html')

def report_view(request):
    # POST 요청(분석 버튼 클릭)이 오면
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        text = request.POST.get('text', '')
        
        # 파이프라인 가동! (번역 -> 요약)
        try:
            result = generate_report(text)
            return JsonResponse(result)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'error': '모델 처리 중 오류가 발생했습니다.'}, status=500)
            
    return render(request, 'report.html')