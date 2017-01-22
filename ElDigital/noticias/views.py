# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.


def post_list(request):
    return render(request,'noticias/post_list.html',{})
