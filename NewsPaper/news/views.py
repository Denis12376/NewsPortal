from django.shortcuts import render
from django.views.generic import ListView, DeleteView

from .models import Post


def post(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, 'post.html', context)

class newsdetails(DeleteView):
    model = Post
    template_name = 'postid.html'
    context_object_name = 'post'


