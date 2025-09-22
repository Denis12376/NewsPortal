from django_filters import FilterSet, ModelChoiceFilter, CharFilter, DateFilter
from django import forms
from .models import Author



class PostFilter(FilterSet):
    author = ModelChoiceFilter(queryset=Author.objects.all(), label = 'Автор', empty_label='Все авторы')
    title = CharFilter(label='Заголовок',lookup_expr='iregex')
    text = CharFilter(field_name='content',label='Содержание',lookup_expr='iregex')
    created_after = DateFilter(
        field_name='created_at',
        lookup_expr='gte',  # greater than or equal (после или равно)
        label='Опубликовано после',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'placeholder': 'Выберите дату'
        })
    )


