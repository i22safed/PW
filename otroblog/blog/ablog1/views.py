from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from ablog1.models import articulo, comentario, categoria, blog
from ablog1.forms import ComentarioForm, ArticuloForm, registroUsuario, categoriaForm, blogForm
from django.core.mail import EmailMessage
import datetime
#Administracion de usuarios:
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#Paginacion:
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):	#Vista de Inicio
	art=articulo.objects.order_by("-fecha")
	paginator=Paginator(art,5)
	page=request.GET.get('page')
	categorias=categoria.objects.all()
	blogs=blog.objects.all()
	try:
		articulos=paginator.page(page)
	except PageNotAnInteger:
		articulos=paginator.page(1)
	except EmptyPage:
		articulos=paginator.page(paginator.num_pages)
	return render_to_response('index.html',{'articulos':articulos, 'categorias':categorias, 'blogs':blogs},context_instance=RequestContext(request))

def un_articulo(request, idArticulo):	#Muestra una entrada concreta
	art=articulo.objects.get(id=idArticulo)
	comentarios=comentario.objects.filter(articulo=idArticulo)
	cats=categoria.objects.all()
	blogs=blog.objects.all()
	return render_to_response('articulo.html',{'articulo':art,'comentarios':comentarios, 'categorias':cats, 'blogs':blogs},context_instance=RequestContext(request))

def articulo_usuario(request, idUsuario):	#Muestra los articulos de un usuario
	usuario=User.objects.get(username=idUsuario)
	art=articulo.objects.filter(usuario=usuario)
	cats=categoria.objects.all()
	blogs=blog.objects.all()
	articulos=art.order_by("-fecha")
	return render_to_response('index.html', {'articulos':articulos,'categorias':cats, 'blogs':blogs},context_instance=RequestContext(request))

def articulo_categoria(request,idCategoria):  #Muestra los articulos por categorias
	cats=categoria.objects.get(id=idCategoria)
	blogs=blog.objects.all()
	articulos=articulo.objects.filter(categoria=cats)
	articulos=articulos.order_by("-fecha")
	categorias=categoria.objects.all()
	return render_to_response('index.html',{'articulos':articulos,'categorias':categorias,'blogs':blogs},context_instance=RequestContext(request))

def nuevo_comentario(request, idArticulo):	#Ingresa un nuevo comentario a un articulo
	blogs=blog.objects.all()
	categorias=categoria.objects.all()
	if request.method=='POST':
		formulario=ComentarioForm(request.POST)
		if formulario.is_valid():
			text=formulario.cleaned_data['texto']
			if request.user.is_anonymous():
				usuario=User.objects.filter(username='Invitado')
				if not usuario:	#Si el usuario invitado no existe aun, lo crea
					usuario=User.objects.create_user(username='Invitado')
				else:
					usuario=User.objects.get(username='Invitado')
			else:
				usuario=request.user
			art=articulo.objects.get(pk=idArticulo)
			comentarioNuevo=comentario.objects.create(texto=text,articulo=art,usuario=usuario)
			comentarioNuevo.save()
			return HttpResponseRedirect('/articulo/%s/'%idArticulo)	#Si es correcto redirige de nuevo al articulo
		else:
			return HttpResponseRedirect('/nuevo_comentario/%s/'%idArticulo)	#Si formulario incorrecto redirige a la misma pagina del formulario
	else:
		formulario=ComentarioForm()
	return render_to_response('comentarioForm.html',{'form':formulario,'categorias':categorias,'blogs':blogs},context_instance=RequestContext(request))

@login_required(login_url='/entrar')
def borrar_comentario(request, idArticulo, idComentario):	#Borrar comentario de un articulo
	com=comentario.objects.get(id=idComentario)
	if com:
		com.delete()
	return HttpResponseRedirect('/articulo/%s/'%idArticulo)

@login_required(login_url='/entrar')
def modificar_comentario(request, idArticulo, idComentario):	#Modificar un comentario
	blogs=blog.objects.all()
	categorias=categoria.objects.all()
	com=comentario.objects.get(pk=idComentario)
	art=articulo.objects.get(pk=idArticulo)
	if request.method=='POST':
		form=ComentarioForm(request.POST,instance=com)	#instance para enviar la informacion del objeto
		if form.is_valid():
			text=form.cleaned_data['texto']
			coment=comentario.objects.filter(pk=idComentario).update(texto=text,fechaMod=datetime.datetime.now())
			return HttpResponseRedirect('/articulo/%s/'%idArticulo)
		else:
			url=idArticulo+'/'+idComentario
			return HttpResponseRedirect('/modificar_comentario/%s/'%url)	#Sino es valido vuelve a preguntar
	else:
		form=ComentarioForm(instance=com)
	return render_to_response('comentarioForm.html',{'form':form,'categorias':categorias,'blogs':blogs,'articulo':art},context_instance=RequestContext(request))

def nuevo_usuario(request):	#Ingresa un nuevo usuario a la bd
	blogs=blog.objects.all()
	categorias=categoria.objects.all()
	form=registroUsuario()
	if request.method=="POST":
		form=registroUsuario(request.POST)
		if form.is_valid():
			user=form.cleaned_data['username']
			email=form.cleaned_data['email']
			password1=form.cleaned_data['password1']
			password2=form.cleaned_data['password2']
			userNuevo=User.objects.create_user(username=user,email=email,password=password1)
			userNuevo.save()
			acceso=authenticate(username=user, password=password1)	#Inicia sesion
			login(request,acceso)
			return HttpResponseRedirect('/')
		else:
			form=registroUsuario()
	return render_to_response('nuevo_usuario.html',{'form':form,'categorias':categorias,'blogs':blogs},context_instance=RequestContext(request))

@login_required(login_url='/entrar')	#Accion solo realizable por usuarios identificados, sino los manda a /entrar
def nuevo_articulo(request):	#Un usuario ingresa una nueva entrada
	blogs=blog.objects.all()
	cats=categoria.objects.all()
	if request.method=='POST':
		form=ArticuloForm(request.POST,request.FILES)
		if form.is_valid():
			usuario=request.user
			titulo=form.cleaned_data['titulo']
			cuerpo=form.cleaned_data['cuerpo']
			if 'categoria' in request.POST:
				cat=form.cleaned_data['categoria']
				if 'imagen' in request.FILES:
					imagen=request.FILES['imagen']
					articuloNuevo=articulo.objects.create(titulo=titulo,cuerpo=cuerpo,categoria=cat,usuario=usuario,imagen=imagen)
				else:
					articuloNuevo=articulo.objects.create(titulo=titulo,cuerpo=cuerpo,categoria=cat,usuario=usuario)
			else:
				if 'imagen' in request.FILES:
					imagen=request.FILES['imagen']
					articuloNuevo=articulo.objects.create(titulo=titulo,cuerpo=cuerpo,usuario=usuario,imagen=imagen)
				else:
					articuloNuevo=articulo.objects.create(titulo=titulo,cuerpo=cuerpo,usuario=usuario)
			return HttpResponseRedirect('/articulo/%s'%articuloNuevo.pk)
		else:
			return HttpResponseRedirect('/nuevo_articulo')
	else:
		form=ArticuloForm()
	return render_to_response('articuloForm.html',{'form':form,'categorias':cats,'blogs':blogs},context_instance=RequestContext(request))

@login_required(login_url='/entrar')
def modificar_articulo(request, idArticulo):
	blogs=blog.objects.all()
	cats=categoria.objects.all()
	art=articulo.objects.get(id=idArticulo)
	if request.method=='POST':
		form=ArticuloForm(request.POST,request.FILES,instance=art)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/articulo/%s/'%idArticulo)
		else:
			return HttpResponseRedirect('/modificar_articulo/%s/'%idArticulo)
	else:
		form=ArticuloForm(instance=art)
	return render_to_response('articuloForm.html', {'form':form,'articulo':art,'categorias':cats,'blogs':blogs}, context_instance=RequestContext(request))

@login_required(login_url='/entrar')
def borrar_articulo(request, idArticulo):	#Borrar una entrada
	art=articulo.objects.get(id=idArticulo)
	if art:
		comentariosArticulo=comentario.objects.filter(articulo=idArticulo)
		comentariosArticulo.delete()
		art.delete()
	return HttpResponseRedirect('/')

def entrar(request):	#Registro de la pagina
	blogs=blog.objects.all()
	categorias=categoria.objects.all()
	if request.method=='POST':
		form=AuthenticationForm(request.POST)
		if form.is_valid:
			user=request.POST['username']
			passw=request.POST['password']
			acceso=authenticate(username=user, password=passw)
			if acceso is not None and acceso.is_active:
				login(request,acceso)
				return HttpResponseRedirect('/')
			else:
				return render_to_response('entrar.html',{'mensaje':"Usuario y/o Password incorrectos", 'formulario':form}, context_instance=RequestContext(request))
	formulario=AuthenticationForm()
	return render_to_response('entrar.html',{'formulario':formulario,'categorias':categorias,'blogs':blogs}, context_instance=RequestContext(request))

@login_required(login_url='/entrar')	#Cerrar sesion
def salir(request):
	logout(request)
	return HttpResponseRedirect('/')

@login_required(login_url='/entrar')
def nueva_categoria(request):
	blogs=blog.objects.all()
	categorias=categoria.objects.all()
	if request.method=='POST':
		form=categoriaForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/')
		else:
			return HttpResponseRedirect('/nueva_categoria')
	else:
		form=categoriaForm()
	return render_to_response('nueva_categoria.html',{'form':form,'categorias':categorias,'blogs':blogs},context_instance=RequestContext(request))

@login_required(login_url='/entrar')
def nuevo_blog(request):
	blogs=blog.objects.all()
	categorias=categoria.objects.all()
	if request.method=='POST':
		form=blogForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/')
		else:
			return HttpResponseRedirect('/nuevo_blog')
	else:
		form=blogForm()
	return render_to_response('nuevo_blog.html',{'form':form,'categorias':categorias,'blogs':blogs},context_instance=RequestContext(request))
