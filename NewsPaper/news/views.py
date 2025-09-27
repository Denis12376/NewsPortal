from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django_filters.views import FilterView
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from .forms import PostForm, UserForm
from .models import Post, Author, Category
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

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create_or_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'news' in self.request.path:
            context['create_or_edit'] = "Добавление новости"
            context['post_type'] = 'NW'
        elif 'articles' in self.request.path:
            context['create_or_edit'] = "Добавление статьи"
            context['post_type'] = 'AR'
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user.author
        if 'articles' in self.request.path:
            post.post_type = 'AR'
        else:
            post.post_type = 'NW'
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        if hasattr(self, 'object') and self.object:
            return reverse_lazy('postid', kwargs={'pk': self.object.pk})
        return reverse_lazy('post')

class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create_or_update.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.change_post'


    def get_queryset(self):
        # Фильтруем по типу поста из URL
        if 'news' in self.request.path:
            return Post.objects.filter(post_type='NW')
        elif 'articles' in self.request.path:
            return Post.objects.filter(post_type='AR')
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'news' in self.request.path:
            context['create_or_edit'] = "Редактирование новости"
        elif 'articles' in self.request.path:
            context['create_or_edit'] = "Редактирование статьи"
        return context

    def get_success_url(self):
        if hasattr(self, 'object') and self.object:
            return reverse_lazy('postid', kwargs={'pk': self.object.pk})
        return reverse_lazy('post_list')



class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy("post")

    def get_queryset(self):
        # Фильтруем по типу поста из URL
        if 'news' in self.request.path:
            return Post.objects.filter(post_type='NW')
        elif 'articles' in self.request.path:
            return Post.objects.filter(post_type='AR')
        return Post.objects.all()

    def get_success_url(self):
        # Возвращаем на нужный список в зависимости от типа
        if 'news' in self.request.path:
            return reverse_lazy('post')
        elif 'articles' in self.request.path:
            return reverse_lazy('post')
        return reverse_lazy('post')


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'profile_edit.html'
    success_url = '/'

    def get_object(self, queryset=None):
        return self.request.user

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

@login_required
def subscribe(request, pk):
    category = Category.objects.get(pk=pk)
    if not category.subscribers.filter(id=request.user.id).exists():
        category.subscribers.add(request.user)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def unsubscribe(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribers.remove(request.user)
    return redirect(request.META.get('HTTP_REFERER'))



@login_required
def become_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():
        Author.objects.create(user=user)
    return redirect('/main/')