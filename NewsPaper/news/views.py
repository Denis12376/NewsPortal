from django.shortcuts import render
from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from django_filters.views import FilterView
from django.urls import reverse_lazy

from .forms import PostForm
from .models import Post
from .filters import PostFilter

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'post.html'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.post_filtered = PostFilter(self.request.GET, queryset=queryset)
        return self.post_filtered.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.post_filtered
        return context



class newsdetails(DeleteView):
    model = Post
    template_name = 'postid.html'
    context_object_name = 'post'

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create_or_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_or_edit'] = "Добовление" if self.request.path == "/news/create/" else "Редактирование"
        return context

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create_or_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_or_edit'] = "Добовление" if self.request.path == "/news/create/" else "Редактирование"
        return context


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy("post")