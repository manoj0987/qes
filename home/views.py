# from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator
# Create your views here.


#Home page
def index(request):
    if 'q' in request.GET:
        q = request.GET['q']
        quests=Question.objects.filter(title__icontains=q).order_by('-id')
    else:
        quests=Question.objects.all().order_by('-id')
    paginator=Paginator(quests,10)
    page_num=request.GET.get('page',1)
    quests=paginator.page(page_num)
    return render(request,'index.html',{'quests':quests})

# Detail
def detail(request,id):
    quest=Question.objects.get(pk=id)
    tags=quest.tags.split(',')
    return render(request,'detail.html',{'quest':quest,'tags':tags})

def ask(request):
    return render(request,'ask.html')

def notification(request):
    return render(request,'notification.html')

def topic(request):
    return render(request,'topic.html')

def signup(request):
    return render(request,'signup.html')

def signin(request):
    return render(request,'signin.html')