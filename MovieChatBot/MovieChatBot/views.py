import json
from openai import OpenAI 
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review
from .forms import MovieForm, ReviewForm
from django.db.models import Q 
from django.core.paginator import Paginator

# 1. 메인 페이지: 영화 리스트 (검색 + 정렬 기능)
def movie_list(request):
    # 1. 검색어(q)와 정렬기준(sort) 가져오기
    q = request.GET.get('q', '') 
    sort = request.GET.get('sort', 'latest')
    
    # 2. 모든 영화 가져오기
    movies = Movie.objects.all()
    
    # 3. 검색 필터링
    if q:
        movies = movies.filter(
            Q(title__icontains=q) |
            Q(director__icontains=q) |
            Q(actors__icontains=q)
        ).distinct()

    # 4. 정렬 적용
    if sort == 'latest':
        movies = movies.order_by('-release_year')
    elif sort == 'title':
        movies = movies.order_by('title')
    else:
        movies = movies.order_by('-pk') # 기본값 (최신 등록순)

    # 5. [핵심] 페이지네이션 기능 (8개씩 자르기)
    paginator = Paginator(movies, 8) # 한 페이지당 8개
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj, # 이제 'movies' 대신 'page_obj'를 템플릿으로 보냅니다.
        'sort': sort,
        'q': q, 
    }
    return render(request, 'MovieChatBot/movie_list.html', context)

# 2. 영화 상세 조회 (기능 1 - 상세)
def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    # 해당 영화에 달린 리뷰 중 첫 번째 것을 가져옴 (없으면 None)
    review = movie.reviews.first()
    
    context = {
        'movie': movie,
        'review': review,
    }
    return render(request, 'MovieChatBot/movie_detail.html', context)


# 3. 영화 및 리뷰 작성 (기능 1 - 작성)
def movie_create(request):
    if request.method == 'POST':
        # 폼 두 개를 동시에 받음 (이미지 포함)
        movie_form = MovieForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        
        if movie_form.is_valid() and review_form.is_valid():
            # 1. 영화 정보 먼저 저장
            movie = movie_form.save()
            
            # 2. 리뷰 정보 저장 (작성된 영화와 연결)
            review = review_form.save(commit=False)
            review.movie = movie
            review.save()
            
            # 상세 페이지로 이동
            return redirect('movie_detail', pk=movie.pk)
    else:
        movie_form = MovieForm()
        review_form = ReviewForm()

    context = {
        'movie_form': movie_form,
        'review_form': review_form
    }
    return render(request, 'MovieChatBot/movie_form.html', context)


# 4. 영화 및 리뷰 수정 (기능 1 - 수정)
def movie_update(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    # 기존 리뷰가 있으면 가져오고, 없으면(TMDB 데이터 등) 빈 폼을 띄움
    review = movie.reviews.first()

    if request.method == 'POST':
        movie_form = MovieForm(request.POST, request.FILES, instance=movie)
        review_form = ReviewForm(request.POST, instance=review) # 기존 리뷰 수정
        
        if movie_form.is_valid() and review_form.is_valid():
            movie = movie_form.save()
            
            review = review_form.save(commit=False)
            review.movie = movie
            review.save()
            
            return redirect('movie_detail', pk=movie.pk)
    else:
        # 기존 데이터를 폼에 채워서 보여줌
        movie_form = MovieForm(instance=movie)
        review_form = ReviewForm(instance=review)

    context = {
        'movie_form': movie_form,
        'review_form': review_form
    }
    return render(request, 'MovieChatBot/movie_form.html', context)


# 5. 영화 삭제 (기능 1 - 삭제)
def movie_delete(request, pk):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, pk=pk)
        movie.delete() # 영화를 삭제하면 연결된 리뷰도 같이 삭제됨 (CASCADE 설정 때문)
        return redirect('movie_list')
    # POST 요청이 아닐 경우 상세 페이지로 돌려보냄 (보안상 삭제는 POST로만)
    return redirect('movie_detail', pk=pk)

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message')

            # 1. Upstage API 설정
            # .env에 UPSTAGE_API_KEY를 넣거나, 여기에 직접 'up_...' 키를 넣으세요.
            api_key = getattr(settings, 'UPSTAGE_API_KEY', '형님의_UPSTAGE_API_KEY_입력')
            
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.upstage.ai/v1/solar"
            )

            # 2. DB에서 영화 정보 가져오기 (Context 생성)
            movies = Movie.objects.all()
            movie_context = "내 영화 컬렉션 데이터:\n"
            for m in movies:
                # 데이터가 너무 길어지면 잘릴 수 있으므로 핵심 정보만 요약
                genre_name = m.get_genre_display() if m.genre else "장르 미정"
                movie_context += f"- 제목: {m.title} / 장르: {genre_name} / 감독: {m.director} / 평점: {m.tmdb_average}점\n"

            # 3. Solar에게 프롬프트 전송
            system_instruction = f"""
            당신은 'My Movie Reviews' 사이트의 AI입니다.
            반드시 아래 [내 영화 컬렉션 데이터] 내에 있는 영화 중에서만 추천하고 답변하세요.
            데이터에 없는 영화를 물어보면 "죄송하지만 제 컬렉션에는 없는 영화네요."라고 정중히 답하세요.
            말투는 "형님, 이 영화는 어떠십니까?" 처럼 정중하고 위트 있게 하세요.

            {movie_context}
            """

            response = client.chat.completions.create(
                model="solar-1-mini-chat", # Upstage의 가성비 모델
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_message}
                ]
            )
            
            bot_reply = response.choices[0].message.content

        except Exception as e:
            print(f"Error: {e}") # 터미널에 에러 출력
            bot_reply = "죄송합니다 형님. AI 서버 연결 중 오류가 발생했습니다."

        return JsonResponse({'response': bot_reply})

    return render(request, 'MovieChatBot/chatbot.html')