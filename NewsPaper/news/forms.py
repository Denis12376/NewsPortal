from django import forms
from  .models import Post

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