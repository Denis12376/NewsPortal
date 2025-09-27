from django import forms
from django.conf import settings
from django.core.mail import send_mail
from pyexpat.errors import messages

from  .models import Post
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm

class PostForm(forms.ModelForm):


    class Meta:
        model = Post
        fields = ['title', 'content','categories']
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
            'categories': 'Категория'
        }
        widgets = {
            'content': forms.Textarea(attrs={'class':'form-textarea', 'rows': 5, 'cols': 40}),
        }


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        html_content = (
            f'<p>Привет, {user.username}!</p>'
            f'<p>Вы успешно прошли регистрацию на <a href="{settings.SITE_URL}/main/">Новостном портале!</a></p>'

        )
        send_mail(
            subject='Регистрация',
            message='Вы успешно прошли регистрацию на Новостном портале!',
            html_message=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']