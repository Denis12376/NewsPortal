from django.urls import path
from .views import newsdetails, PostListView, PostCreateView, PostUpdateView, PostDeleteView
from . import views

urlpatterns = [
    path('news/search/', PostListView.as_view(), name='post'),
    path('news/<int:pk>/', newsdetails.as_view(), name="postid"),
    path('news/create/', PostCreateView.as_view(), name="create_or_edit"),
    path('news/<int:pk>/edit/', PostUpdateView.as_view(), name="create_or_edit"),
    path('news/<int:pk>/delete/', PostDeleteView.as_view(), name="post_delete"),

    path('articles/create/', views.PostCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/', views.newsdetails.as_view(), name='article_detail'),
    path('articles/<int:pk>/edit/', views.PostUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', views.PostDeleteView.as_view(), name='article_delete'),
    path('become_author/', views.become_author, name='become_author'),

]