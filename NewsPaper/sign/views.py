from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignUpForm


class SignUpView(CreateView):
    model = User
    template_name = 'sign/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')

def confirm_logout(request):
    return render(request, 'sign/confirm_logout.html')

@login_required
def user_profile(request):
    return render(request, 'sign/profile.html')