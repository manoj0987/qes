# from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.db.models import Count
# Create your views here.


#Home page
def index(request):
    quests=Question.objects.all()
    tags=[]
    for quest in quests:
        qtags=[tag.strip() for tag in quest.tags.split(',')]
        for tag in qtags:
            if tag not in tags:
                tags.append(tag)
    # Fetch Questions
    tag_with_count=[]
    for tag in tags:
        tag_data={
            'name':tag,
            'count':Question.objects.filter(tags__icontains=tag).count()
        }
        tag_with_count.append(tag_data)

    if 'q' in request.GET:
        q=request.GET['q']
        quests=Question.objects.annotate(total_comments=Count('answer__comment')).filter(title__icontains=q).order_by('-id')
    else:
        quests=Question.objects.annotate(total_comments=Count('answer__comment')).all().order_by('-id')
    paginator=Paginator(quests,5)
    page_num=request.GET.get('page',1)
    quests=paginator.page(page_num)
    return render(request,'index.html',{'quests':quests, 'tags':tag_with_count})


# Detail
def detail(request,id):
    quest=Question.objects.get(pk=id)
    tags=quest.tags.split(',')
    answers=Answer.objects.filter(question=quest)

    answerForm=AnswerForm
    if request.method=='POST':
        answerData=AnswerForm(request.POST)
        if answerData.is_valid():
            answer=answerData.save(commit=False)
            answer.question=quest
            answer.user=request.user
            answer.save()
            messages.success(request,'Answer has been submitted')
    return render(request,'detail.html',{
        'quest':quest,
        'tags':tags, 
        'answers':answers,
        'answerForm':answerForm,
        })


def notification(request):
    return render(request,'notification.html')


# Save-commnet
def save_comment(request):
    if request.method=='POST':
        comment=request.POST['comment']
        answerid=request.POST['answerid']
        answer=Answer.objects.get(pk=answerid)
        user=request.user
        Comment.objects.create(
            answer=answer,
            comment=comment,
            user=user   
        )
        return JsonResponse({'bool':True})

# Save Upvote
def save_upvote(request):
    if request.method=='POST':
        answerid=request.POST['answerid']
        answer=Answer.objects.get(pk=answerid)
        user=request.user
        check=Upvote.objects.filter(answer=answer,user=user).count()
        if check > 0:
            return JsonResponse({'bool':False})
        else:
            Upvote.objects.create(
                answer=answer,
                user=user
            )
            return JsonResponse({'bool':True})

# Save Downvote
def save_downvote(request):
    if request.method=='POST':
        answerid=request.POST['answerid']
        answer=Answer.objects.get(pk=answerid)
        user=request.user
        check=Downvote.objects.filter(answer=answer,user=user).count()
        if check > 0:
            return JsonResponse({'bool':False})
        else:
            Downvote.objects.create(
                answer=answer,
                user=user
            )
            return JsonResponse({'bool':True})
        
# User Register
def register(request):
    form=UserCreationForm
    if request.method=='POST':
        regForm=UserCreationForm(request.POST)
        if regForm.is_valid():
            regForm.save()
            messages.success(request,'User has been registered!!')
    return render(request,'registration/signup.html',{'form':form})

# Sign In 
def signin(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        login_form = AuthenticationForm(request=request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
    return render(request, 'registration/signin.html', {'form': form})


# Ask Form
def ask_form(request):
    form=QuestionForm
    if request.method=='POST':
        questForm=QuestionForm(request.POST)
        if questForm.is_valid():
            questForm=questForm.save(commit=False)
            questForm.user=request.user
            questForm.save()
            messages.success(request,'Question has been added.')
    return render(request,'ask.html',{'form':form})


# Questions according to tag
def tag(request,tag):
    quests=Question.objects.annotate(total_comments=Count('answer__comment')).filter(tags__icontains=tag).order_by('-id')
    paginator=Paginator(quests,10)
    page_num=request.GET.get('page',1)
    quests=paginator.page(page_num)
    return render(request,'topic.html',{'quests':quests,'tag':tag})


def profile(request):
    # if not request.user.is_authenticated:
    #     login_form = AuthenticationForm()
    #     return render(request, 'registration/login.html', {'form': login_form})
    
    quests = Question.objects.filter(user=request.user).order_by('-id')
    answers = Answer.objects.filter(user=request.user).order_by('-id')
    comments = Comment.objects.filter(user=request.user).order_by('-id')
    upvotes = Upvote.objects.filter(user=request.user).order_by('-id')
    downvotes = Downvote.objects.filter(user=request.user).order_by('-id')
    
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile has been updated.')
    
    form = ProfileForm(instance=request.user)

    return render(request, 'registration/profile.html', {
        'form': form,
        'quests': quests,
        'answers': answers,
        'comments': comments,
        'upvotes': upvotes,
        'downvotes': downvotes,
    })

# Tags Page
def tags(request):
    quests=Question.objects.all()
    tags=[]
    for quest in quests:
        qtags=[tag.strip() for tag in quest.tags.split(',')]
        for tag in qtags:
            if tag not in tags:
                tags.append(tag)
    # Fetch Questions
    tag_with_count=[]
    for tag in tags:
        tag_data={
            'name':tag,
            'count':Question.objects.filter(tags__icontains=tag).count()
        }
        tag_with_count.append(tag_data)
    return render(request,'tags.html',{'tags':tag_with_count})
   
