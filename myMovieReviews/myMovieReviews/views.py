from django.shortcuts import render

# Create your views here.

# myMovieReviews/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from .forms import ReviewForm

# 1. 리뷰 리스트 페이지 (기능 1, 2, 3)
def review_list(request):
    reviews = Review.objects.all().order_by('-created_at') # 최신순 정렬
    return render(request, 'myMovieReviews/review_list.html', {'reviews': reviews})

# 2. 리뷰 디테일 페이지 (기능 4, 5, 6, 7)
def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'myMovieReviews/review_detail.html', {'review': review})

# 3. 리뷰 작성 페이지 (기능 8, 10)
def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('review_list') # 저장 후 리스트로 이동
    else:
        form = ReviewForm() # 빈 폼
    return render(request, 'myMovieReviews/review_form.html', {'form': form})

# 4. 리뷰 수정 페이지 (기능 9, 11)
def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review) # 기존 데이터 포함
        if form.is_valid():
            form.save()
            return redirect('review_detail', pk=review.pk) # 수정 후 디테일로 이동
    else:
        form = ReviewForm(instance=review) # 기존 데이터 채워진 폼
    return render(request, 'myMovieReviews/review_form.html', {'form': form})

# 5. 리뷰 삭제 기능 (기능 7)
def review_delete(request, pk):
    if request.method == 'POST':
        review = get_object_or_404(Review, pk=pk)
        review.delete()
    return redirect('review_list')