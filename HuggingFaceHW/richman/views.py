from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import ChatHistory # 모델 가져오기
from .utils import login_required_alert # 아까 만든 쫓아내는 도구
# 서비스 함수들 임포트 (기존 유지)
from .services.huggingface import analyze_news_sentiment, generate_report, extract_entities, detect_spam

# 1. 메인 대시보드
def main(request):
    return render(request, 'main.html')

# ==========================================
# 1. 공개 탭 (감성 분석) - 누구나 이용 가능
# ==========================================
def sentiment_view(request):
    return render(request, 'sentiment.html')

def analyze_view(request):
    if request.method == "POST":
        text = request.POST.get('text', '')
        result = analyze_news_sentiment(text)
        
        # [핵심] 로그인한 형님이면 -> DB에 저장!
        if request.user.is_authenticated:
            ChatHistory.objects.create(
                user=request.user,
                feature_name='sentiment',
                user_input=text,
                ai_response=result
            )
        
        return JsonResponse(result)

# ==========================================
# 2. 제한 탭 (나머지) - 로그인 필수 + Alert
# ==========================================

# (1) 스팸 탐지
def spam_view(request):
    # 비로그인 접근 시 -> 알림창 띄우고 쫓아냄
    if not request.user.is_authenticated:
        return login_required_alert(request)
    
    if request.method == "POST":
        text = request.POST.get('text', '')
        result = detect_spam(text)
        
        # 로그인 상태가 확실하므로 바로 저장
        ChatHistory.objects.create(
            user=request.user,
            feature_name='spam',
            user_input=text,
            ai_response=result
        )
        return JsonResponse(result)
        
    return render(request, 'spam.html')

# (2) NER (핵심 정보)
def ner_view(request):
    if not request.user.is_authenticated:
        return login_required_alert(request)

    if request.method == "POST":
        text = request.POST.get('text', '')
        result = extract_entities(text)
        
        ChatHistory.objects.create(
            user=request.user,
            feature_name='ner',
            user_input=text,
            ai_response=result
        )
        return JsonResponse(result)

    return render(request, 'ner.html')

# (3) 리포트 (복합 기능)
def report_view(request):
    if not request.user.is_authenticated:
        return login_required_alert(request)

    if request.method == "POST":
        text = request.POST.get('text', '')
        result = generate_report(text)
        
        ChatHistory.objects.create(
            user=request.user,
            feature_name='report',
            user_input=text,
            ai_response=result
        )
        return JsonResponse(result)

    return render(request, 'report.html')