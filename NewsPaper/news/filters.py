from django_filters import FilterSet, ModelChoiceFilter, CharFilter

from .models import Author


class PostFilter(FilterSet):
    author = ModelChoiceFilter(queryset=Author.objects.all(), label = 'Автор', empty_label='Все авторы')
    title = CharFilter(label='Заголовок',lookup_expr='iregex')
    text = CharFilter(field_name='content',label='Содержание',lookup_expr='iregex')
