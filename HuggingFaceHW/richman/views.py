from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import ChatHistory 
from .utils import login_required_alert
from .services.huggingface import analyze_news_sentiment, generate_report, extract_entities, detect_spam
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


def main(request):
    return render(request, 'main.html')

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

# (1) 스팸 탐지
def spam_view(request):
    # 비로그인 접근 시 -> 알림창 띄우고 쫓아냄
    if not request.user.is_authenticated:
        return login_required_alert(request)
    
    if request.method == "POST":
        text = request.POST.get('text', '')
        result = detect_spam(text)
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

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('richman:main')
    
    # 2. 가입 화면 요청 (GET)
    else:
        form = UserCreationForm()
        
    return render(request, 'registration/signup.html', {'form': form})

@login_required # 로그인 안 했으면 접근 불가
def history_view(request):
    histories = ChatHistory.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'history.html', {'histories': histories})