import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Post
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment , Profile, Story
from .forms import PostForm, CommentForm, StoryForm, PostUpdateForm
from django.contrib.auth.models import User
from django.db.models import Q

@login_required
def main(request):
    # 1. 팔로우한 사람들의 게시글 (기존 로직)
    user = request.user
    followings = user.profile.following.all()
    posts = Post.objects.filter(Q(author__in=followings) | Q(author=user)).order_by('-pk')

    # 2. [수정됨] 스토리가 있는 유저들만 가져오기 (중복 제거)
    # 나를 제외하고, 스토리가 존재하는 유저만 가져옵니다.
    story_users = User.objects.filter(stories__isnull=False).exclude(id=user.id).distinct()
    
    # 3. 내 스토리 확인 (내가 올린 스토리가 있는지)
    my_stories = Story.objects.filter(author=user)
    has_my_story = my_stories.exists()

    comment_form = CommentForm()
    
    context = {
        'posts': posts,
        'story_users': story_users, # 템플릿으로 유저 목록 전달
        'has_my_story': has_my_story,
        'comment_form': comment_form,
    }
    return render(request, 'main.html', context)

def post_create(request):
    if request.method == 'POST':
        # 입력된 데이터(POST)와 파일(FILES)을 폼에 담음
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False) # 바로 저장하지 않고 대기
            post.author = request.user     # 작성자를 현재 로그인한 유저로 채움
            post.save()                    # 최종 저장
            return redirect('pirostagram:main') # 저장 후 메인으로 이동
    else:
        form = PostForm()
    
    context = {
        'form': form
    }
    return render(request, 'post_create.html', context)

@login_required # 로그인한 사람만 좋아요 가능
def post_like(request):
    if request.method == 'POST':
        # 프론트엔드(JS)에서 보낸 데이터를 꺼냄
        req = json.loads(request.body)
        post_id = req['id']
        
        post = Post.objects.get(id=post_id)
        user = request.user
        
        # 이미 좋아요를 눌렀다면 -> 취소 (remove)
        if post.like_users.filter(id=user.id).exists():
            post.like_users.remove(user)
            message = "취소"
        # 안 눌렀다면 -> 추가 (add)
        else:
            post.like_users.add(user)
            message = "좋아요"
        
        # 변경된 좋아요 개수와 상태를 다시 프론트엔드로 던져줌
        context = {
            'like_count': post.like_users.count(),
            'message': message
        }
        return JsonResponse(context)
    
@login_required
def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('pirostagram:main')

@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    # 본인이 쓴 댓글인 경우에만 삭제
    if request.user == comment.author:
        comment.delete()
    return redirect('pirostagram:main')

def search(request):
    query = request.GET.get('q')
    if query:
        # 아이디(username)에 검색어가 포함된 유저 찾기
        users = User.objects.filter(username__icontains=query)
    else:
        users = []
    
    context = {
        'users': users,
        'query': query
    }
    return render(request, 'search_result.html', context)

def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    # 해당 유저가 쓴 글만 가져오기
    posts = Post.objects.filter(author=user).order_by('-pk')
    
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)
        
    context = {
        'profile_user': user,
        'posts': posts,
    }
    return render(request, 'profile.html', context)

@login_required
def follow(request, user_id):
    target_user = get_object_or_404(User, pk=user_id)
    me = request.user
    
    if not hasattr(me, 'profile'):
        Profile.objects.create(user=me)
    
    my_profile = me.profile
    
    # 이미 팔로우 중이면 -> 취소 (remove)
    if my_profile.following.filter(id=target_user.id).exists():
        my_profile.following.remove(target_user)
    # 아니면 -> 추가 (add)
    else:
        my_profile.following.add(target_user)
    
    return redirect('pirostagram:profile', user_id=user_id)

@login_required
def story_create(request):
    if request.method == 'POST':
        # [수정됨] 여러 장의 사진을 받기 위해 getlist 사용
        files = request.FILES.getlist('photo') 
        
        if files:
            for f in files:
                # 각각의 사진에 대해 Story 객체 생성
                Story.objects.create(author=request.user, photo=f)
            return redirect('pirostagram:main')
            
    else:
        form = StoryForm()
    return render(request, 'story_create.html', {'form': form})

@login_required
def post_update(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect('pirostagram:main') # 권한 없으면 튕겨냄
        
    if request.method == 'POST':
        form = PostUpdateForm(request.POST, instance=post) # instance=post가 있어야 수정 모드
        if form.is_valid():
            form.save()
            return redirect('pirostagram:main')
    else:
        form = PostUpdateForm(instance=post)
    
    return render(request, 'post_update.html', {'form': form})

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user == post.author:
        post.delete()
    return redirect('pirostagram:main')