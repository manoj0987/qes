from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:id>', views.detail, name='detail'),
    path('ask', views.ask, name='ask'),
    path('topic', views.topic, name='topic'),
    path('notification', views.notification, name='notification'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    
]