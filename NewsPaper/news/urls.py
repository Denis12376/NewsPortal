from django.urls import path
from .views import newsdetails, PostListView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('', PostListView.as_view(), name='post'),
    path('<int:pk>/', newsdetails.as_view(), name="postid"),
    path('create/', PostCreateView.as_view(), name="create_or_edit"),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name="create_or_edit"),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name="post_delete"),
]