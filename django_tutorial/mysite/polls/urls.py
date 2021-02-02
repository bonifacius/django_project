from django.urls import path

from . import views

# Создаем пространство имен polls что бы из polls/index.html считывался параметр
# url <app_name>:<view name> если мы захотим поменять url мы поменяем его только в polls/urls.py
# Это нужно что бы django понимал из какого приложения брать view.

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]