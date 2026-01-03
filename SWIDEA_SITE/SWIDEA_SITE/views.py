from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator 
from django.http import JsonResponse
from .models import Idea, DevTool, IdeaStar
from .forms import IdeaForm, DevToolForm

def idea_list(request):
    sort = request.GET.get('sort', 'recent') 
    ideas = Idea.objects.all()

    if sort == 'name':
        ideas = ideas.order_by('title')
    elif sort == 'interest':
        ideas = ideas.order_by('-interest')
    elif sort == 'star':
        
        ideas = ideas.order_by('-created_date') 
    else: 
        ideas = ideas.order_by('-created_date')

    paginator = Paginator(ideas, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'SWIDEA_SITE/idea_list.html', {'page_obj': page_obj, 'sort': sort})


def idea_create(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save()
            return redirect('SWIDEA_SITE:idea_detail', pk=idea.pk)
    else:
        form = IdeaForm()
    return render(request, 'SWIDEA_SITE/idea_form.html', {'form': form})


def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)

    is_starred = False
    if request.user.is_authenticated:
        is_starred = IdeaStar.objects.filter(idea=idea, user=request.user).exists()
    
    return render(request, 'SWIDEA_SITE/idea_detail.html', {'idea': idea, 'is_starred': is_starred})

def idea_update(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES, instance=idea)
        if form.is_valid():
            idea = form.save()
            return redirect('SWIDEA_SITE:idea_detail', pk=idea.pk)
    else:
        form = IdeaForm(instance=idea)
    return render(request, 'SWIDEA_SITE/idea_form.html', {'form': form})

def idea_delete(request, pk):
    if request.method == 'POST':
        idea = get_object_or_404(Idea, pk=pk)
        idea.delete()
        return redirect('SWIDEA_SITE:idea_list')
    return redirect('SWIDEA_SITE:idea_detail', pk=pk)


def devtool_list(request):
    devtools = DevTool.objects.all()
    return render(request, 'SWIDEA_SITE/devtool_list.html', {'devtools': devtools})

def devtool_create(request):
    if request.method == 'POST':
        form = DevToolForm(request.POST)
        if form.is_valid():
            devtool = form.save()
            return redirect('SWIDEA_SITE:devtool_detail', pk=devtool.pk)
    else:
        form = DevToolForm()
    return render(request, 'SWIDEA_SITE/devtool_form.html', {'form': form})

def devtool_detail(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    related_ideas = devtool.idea_set.all()  
    
    return render(request, 'SWIDEA_SITE/devtool_detail.html', {
        'devtool': devtool,
        'related_ideas': related_ideas
    })

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



def idea_star_ajax(request, pk):
    if not request.user.is_authenticated:
         return JsonResponse({'message': '로그인이 필요합니다.', 'is_starred': False}, status=403)

    idea = get_object_or_404(Idea, pk=pk)
    star, created = IdeaStar.objects.get_or_create(idea=idea, user=request.user)

    if not created:
        star.delete()
        is_starred = False
    else:
        is_starred = True

    return JsonResponse({'is_starred': is_starred})

def idea_interest_ajax(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    action = request.GET.get('action') 

    if action == 'plus':
        idea.interest += 1
    elif action == 'minus':
        idea.interest -= 1
    
    idea.save()
    return JsonResponse({'interest': idea.interest})