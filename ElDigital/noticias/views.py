# -*- coding: utf-8 -*-

from django.shortcuts import render
from .models import Post, Comentario, Mensaje
from django.utils import timezone

# Create your views here.


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request,'noticias/post_list.html',{'posts':posts})

def post_detail(request,pk):
    post = get_object_or_404(Post, pk = pk)
    return render(request, 'noticias/post_detail.html', {'post': post})
