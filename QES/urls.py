from django.urls import path
from . import views

urlpatterns = [
    # HOme
    path('', views.index, name='index'),
    # Detail page
    path('detail/<int:id>', views.detail, name='detail'),
    path('save-comment', views.save_comment, name='save-comment'),
    path('save-upvote', views.save_upvote, name='save-upvote'),
    path('save-downvote', views.save_downvote, name='save-downvote'),

    path('notification', views.notification, name='notification'),

    # User Register
    path('accounts/signup/', views.register, name='register'),
    path('accounts/signin/', views.signin, name='signin'),
    # Profile
    path('accounts/profile/',views.profile,name='profile'),
    # Ask QUestion
    path('ask-question',views.ask_form,name='ask-question'),
    # tag page
    path('tag/<str:tag>', views.tag, name='tag'),
    # Tags Page / Topics
    path('tags', views.tags, name='tags'),
]