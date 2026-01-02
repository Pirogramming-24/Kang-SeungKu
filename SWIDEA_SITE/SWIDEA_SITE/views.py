from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator 
from django.http import JsonResponse
from .models import Idea, DevTool, IdeaStar
from .forms import IdeaForm, DevToolForm

# ---------------------------------------------------------
# 1. 아이디어(Idea) 관리
# ---------------------------------------------------------

# [메인] 아이디어 리스트 (정렬 + 페이지네이션)
def idea_list(request):
    sort = request.GET.get('sort', 'recent') 
    ideas = Idea.objects.all()

    # 정렬 로직
    if sort == 'name':
        ideas = ideas.order_by('title')
    elif sort == 'interest':
        ideas = ideas.order_by('-interest')
    elif sort == 'star':
        # 찜하기 순은 복잡해서 일단 등록순으로 두거나, 
        # 별도 로직(annotate)이 필요하지만 과제 수준에선 id순 등으로 대체 가능
        ideas = ideas.order_by('-created_date') 
    else: # recent
        ideas = ideas.order_by('-created_date')

    # 페이지네이션 (4개씩)
    paginator = Paginator(ideas, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'SWIDEA_SITE/idea_list.html', {'page_obj': page_obj, 'sort': sort})

# [등록] 아이디어 생성
def idea_create(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save()
            # 등록 후 디테일 페이지로 이동 (요구사항 기능 15)
            return redirect('SWIDEA_SITE:idea_detail', pk=idea.pk)
    else:
        form = IdeaForm()
    return render(request, 'SWIDEA_SITE/idea_form.html', {'form': form})

# [조회] 아이디어 디테일
def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    
    # 찜 여부 확인 (로그인 유저인 경우)
    is_starred = False
    if request.user.is_authenticated:
        is_starred = IdeaStar.objects.filter(idea=idea, user=request.user).exists()
    
    return render(request, 'SWIDEA_SITE/idea_detail.html', {'idea': idea, 'is_starred': is_starred})

# [수정] 아이디어 수정
def idea_update(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if request.method == 'POST':
        # instance=idea를 넣어줘야 기존 내용이 채워진 상태로 수정됨 (요구사항 기능 9)
        form = IdeaForm(request.POST, request.FILES, instance=idea)
        if form.is_valid():
            idea = form.save()
            return redirect('SWIDEA_SITE:idea_detail', pk=idea.pk)
    else:
        form = IdeaForm(instance=idea)
    return render(request, 'SWIDEA_SITE/idea_form.html', {'form': form})

# [삭제] 아이디어 삭제
def idea_delete(request, pk):
    if request.method == 'POST':
        idea = get_object_or_404(Idea, pk=pk)
        idea.delete()
        return redirect('SWIDEA_SITE:idea_list')
    # GET으로 들어오면 그냥 디테일로 돌려보내거나 확인 페이지 띄움
    return redirect('SWIDEA_SITE:idea_detail', pk=pk)


# ---------------------------------------------------------
# 2. 개발툴(DevTool) 관리
# ---------------------------------------------------------

# [리스트] 개발툴 목록
def devtool_list(request):
    devtools = DevTool.objects.all()
    return render(request, 'SWIDEA_SITE/devtool_list.html', {'devtools': devtools})

# [등록] 개발툴 등록
def devtool_create(request):
    if request.method == 'POST':
        form = DevToolForm(request.POST)
        if form.is_valid():
            devtool = form.save()
            # 등록 후 디테일 페이지로 이동 (요구사항 기능 15)
            return redirect('SWIDEA_SITE:devtool_detail', pk=devtool.pk)
    else:
        form = DevToolForm()
    return render(request, 'SWIDEA_SITE/devtool_form.html', {'form': form})

# [조회] 개발툴 디테일 (해당 툴을 쓴 아이디어 리스트 포함)
def devtool_detail(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    # 해당 개발툴을 참조하는 아이디어들 가져오기 (Reverse Accessor)
    # models.py에서 related_name을 안 썼으면 기본적으로 idea_set으로 접근 가능
    related_ideas = devtool.idea_set.all()  
    
    return render(request, 'SWIDEA_SITE/devtool_detail.html', {
        'devtool': devtool,
        'related_ideas': related_ideas
    })

# [수정] 개발툴 수정
def devtool_update(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    if request.method == 'POST':
        form = DevToolForm(request.POST, instance=devtool)
        if form.is_valid():
            devtool = form.save()
            return redirect('SWIDEA_SITE:devtool_detail', pk=devtool.pk)
    else:
        form = DevToolForm(instance=devtool)
    return render(request, 'SWIDEA_SITE/devtool_form.html', {'form': form})

# [삭제] 개발툴 삭제
def devtool_delete(request, pk):
    if request.method == 'POST':
        devtool = get_object_or_404(DevTool, pk=pk)
        devtool.delete()
        return redirect('SWIDEA_SITE:devtool_list')
    return redirect('SWIDEA_SITE:devtool_detail', pk=pk)


# ---------------------------------------------------------
# 3. AJAX (찜하기, 관심도) - 챌린지 과제
# ---------------------------------------------------------

# [AJAX] 찜하기 토글
def idea_star_ajax(request, pk):
    # 로그인 여부 체크 (로그인 안했으면 에러 혹은 리다이렉트 처리 필요하나 과제용으로 패스 가능)
    if not request.user.is_authenticated:
         return JsonResponse({'message': '로그인이 필요합니다.', 'is_starred': False}, status=403)

    idea = get_object_or_404(Idea, pk=pk)
    # get_or_create: 있으면 가져오고(created=False), 없으면 만듬(created=True)
    star, created = IdeaStar.objects.get_or_create(idea=idea, user=request.user)

    if not created:
        # 이미 찜이 되어 있던 상태 -> 삭제 (찜 취소)
        star.delete()
        is_starred = False
    else:
        # 새로 찜함
        is_starred = True

    return JsonResponse({'is_starred': is_starred})

# [AJAX] 관심도 조절 (+/-)
def idea_interest_ajax(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    action = request.GET.get('action') # URL 쿼리 스트링에서 action 가져옴

    if action == 'plus':
        idea.interest += 1
    elif action == 'minus':
        idea.interest -= 1
    
    idea.save()
    return JsonResponse({'interest': idea.interest})