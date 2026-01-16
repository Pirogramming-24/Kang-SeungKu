from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review
from .forms import MovieForm, ReviewForm

# 1. 영화 리스트 (기능 1, 3 - 조회 및 정렬)
def movie_list(request):
    sort = request.GET.get('sort', 'latest')
    movies = Movie.objects.all()
    
    if sort == 'latest':
        movies = movies.order_by('-release_year')
    elif sort == 'title':
        movies = movies.order_by('title')
    
    context = {
        'movies': movies,
        'sort': sort
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
    return render(request, 'MovieChatBot/review_form.html', context)


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
    return render(request, 'MovieChatBot/review_form.html', context)


# 5. 영화 삭제 (기능 1 - 삭제)
def movie_delete(request, pk):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, pk=pk)
        movie.delete() # 영화를 삭제하면 연결된 리뷰도 같이 삭제됨 (CASCADE 설정 때문)
        return redirect('movie_list')
    # POST 요청이 아닐 경우 상세 페이지로 돌려보냄 (보안상 삭제는 POST로만)
    return redirect('movie_detail', pk=pk)