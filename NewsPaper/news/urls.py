from django.urls import path
from .views import post, newsdetails

urlpatterns = [
    path('post/', post),
    path('<int:pk>/', newsdetails.as_view(), name="postid"),
]