from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import articulo

def index(request):
        lista=articulo.objects.all()
        context={ 'lista' : lista }

        return render(request, 'index.html', context)

def login_view(request):
        user_name = user_pass = status = ''
        if request.POST:
            user_name=request.POST.get('usuario')
            user_pass=request.POST.get('pass')

            user=authenticate(username=user_name, password=user_pass)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    status='Has entrado correctamente'
                else:
                    status='Su usuario esta bloqueado por el administrador'
            else:
                status='Los datos son incorrectos'

        context = {'status':status}
        return render(request, 'login.html', context)


def register_view(request):
        status=user_nombre=user_apellidos=user_pass=user_usuario=user_email=''

        if request.POST:
            user_nombre=request.POST.get('nombre')
            user_apellidos=request.POST.get('apellidos')
            user_pass=request.POST.get('password')
            user_usuario=request.POST.get('usuario')
            user_email=request.POST.get('email')

            user= User.objects.create_user(
            username=user_usuario,
            password=user_pass,
            email=user_email,
            first_name=user_nombre,
            last_name=user_apellidos)

            status='Usuario creado satisfactoriamente'

        context={'status':status}

        return render(request, 'register.html', context)

def logout_view(request):
    logout(request)
    status='Se ha deslogeado con exito'
    context={'status':status}

    return render(request, 'logout.html', context)

def  publicar_view(request):
    status=titulo=texto=''

    if request.POST:
        titulo=request.POST.get('titulo')
        texto=request.POST.get('texto')

        article=articulo.objects.create(
        titulo=titulo,
        texto=texto,
        user=request.user
        )
        article.save()
        status='Se ha publicado correctamente'

    context={'status':status}
    return render(request, 'publicar.html', context)


def articulosprivados_view(request):
    status=''
    lista=articulo.objects.filter(user=request.user)
    context={ 'lista':lista,
              'isEditing' : True }

    return render(request, 'articulosprivados.html', context)

def modificar_view(request, num):
    status=''
    article=articulo.objects.get(id=num)
    if request.POST:
        titulo=request.POST.get('titulo')
        texto=request.POST.get('texto')
        article.titulo=titulo
        article.texto=texto

        article.save()
        status='Se ha modificado correctamente'


    context={'article':article, 'status':status}

    return render(request, 'modificar.html', context)

def borrar_view(request, num):
    status='Se ha borrado correctamente'
    article=articulo.objects.get(id=num)

    article.delete()
    context={'status':status}
    return render(request,'borrar.html', context)
