from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import confirm_logout, user_profile, SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('confirm/logout/', confirm_logout, name='confirm_logout'),
    path('profile/', user_profile, name='user_profile'),
]