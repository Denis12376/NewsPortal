from django import forms
from  .models import Post
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm

class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['author'].empty_label = 'Выберите автора'

    class Meta:
        model = Post
        fields = ['author','title', 'content','categories']
        labels = {
            'author': 'Автор',
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
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']