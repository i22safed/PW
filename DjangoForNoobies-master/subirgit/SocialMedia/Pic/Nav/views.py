from django.shortcuts import render
from Nav.models import SingUpForm, UploadPicture, UserProfile, Image, imageList, search, Comentario, newComent, newMensaje, Mensaje
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import render_to_response
from django.contrib.auth import login, authenticate, logout
from django.template import RequestContext
from django.db import models
import mimetypes
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required



# Create your views here

def nuevoUser(request):
	if request.method=='POST':
		form = SingUpForm(request.POST, request.FILES)

		if form.is_valid():
								
			form.save()

		return HttpResponseRedirect('/')
	else:
		form = SingUpForm()

	return render_to_response('register.html', {'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/genericindex')
def indexUser(request):
		user = UserProfile.objects.get(pk=request.session['conectado'])
		context={'UserProfile' : user }
		return render_to_response('index.html', context, context_instance=RequestContext(request))

def ingresar(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/')
	if request.method=='POST':
		form = AuthenticationForm(request.POST)
		if form.is_valid:
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if not user is None:
				if user.is_active:
					login(request, user)
					m = UserProfile.objects.get(username=username)
					request.session['conectado'] = m.id
					print request.session['conectado']
					return HttpResponseRedirect('/')
				else:
					return render_to_response('noactivo.html', context_instance=RequestContext(request))
			else:
					return render_to_response('noexiste.html', context_instance=RequestContext(request))

	else:
		form= AuthenticationForm()
	return render_to_response('ingresar.html', {'form':form}, context_instance=RequestContext(request))

def cerrar(request):
	logout(request)
	request.session['conectado'] = False
	return HttpResponseRedirect('/')

def editar(request):
	user = User.objects.get(pk=request.session['conectado'])
	if request.method == 'POST':
		form = SingUpForm(request.POST, instance = user)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/')
		
	else:
		form = SingUpForm(instance = user)

		return render(request, 'editar.html', {'form': form})

def UploadPictures(request):
	if request.method=='POST':
		form = UploadPicture(request.POST, request.FILES)				
		if form.is_valid():
			temp = form.save(commit=False)
			temp.autor = User.objects.get(pk=request.session['conectado'])
			temp.save()
			return HttpResponseRedirect('/')
	else:
		form = UploadPicture()

	return render_to_response('upload.html', {'form':form}, context_instance=RequestContext(request))

def realizarBusqueda(request):
	if request.method == 'POST':
		form = search(request.POST)

		if form.is_valid():
			sl = form.save()
			return searchImage(request, etiqueta=sl.busqueda)

	else:
		form = search()
		
	return render(request, 'search.html', {'form':form})

def buscaAmigos(request):
	if request.method == 'POST':
		form = search(request.POST)

		if form.is_valid():
			sl = form.save()
			return searchFriend(request, nombre=sl.busqueda)

	else:
		form = search()
		
	return render(request, 'search.html', {'form':form})

def imageList(request, user_id):
	user = UserProfile.objects.get(pk=user_id)
	otherlist = user.amigos.all()
	list = Image.objects.filter(autor=user).order_by('-date')
	list2 = Image.objects.filter(repicers=user).order_by('-date')
	sesion = request.session['conectado']
	context = { 'imageList': list, 'userList' : otherlist, 'user' : user, 'sesion' : sesion, 'imageList2' : list2}
	return render(request, 'tablon.html', context)


def searchImage(request, etiqueta):
	list = Image.objects.filter(etiquetas=etiqueta).order_by('-date')
	context = { 'imageList' : list }
	return render(request, 'searcheti.html', context)

def searchFriend(request, nombre):
	list =UserProfile.objects.filter(username=nombre)
	context = { 'userList' : list }
	return render(request, 'searchfriend.html', context)


def comentar(request, image_id):
	img = Image.objects.get(pk=image_id)
	list = Comentario.objects.filter(what=img).order_by('-date')
	if request.method == 'POST':
		form = newComent(request.POST)

		if form.is_valid:
			coment = form.save(commit=False)
			coment.who = UserProfile.objects.get(pk=request.session['conectado'])
			coment.what = img
			coment.save()
			list = Comentario.objects.filter(what=img)
			context= { 'image': img , 'comentarioList' : list , 'form' : form }
			return render(request, 'comentar.html', context)
	else:
		form = newComent()
		
	context= { 'image': img , 'comentarioList' : list , 'form' : form }
	return render(request, 'comentar.html', context)

def votar(request, coment_id, img_id):
	coment = Comentario.objects.get(pk=coment_id)
	print coment.positivos
	coment.positivos = coment.positivos + 1
	print coment.positivos
	coment.save()
	return comentar(request, image_id=img_id)

def repic(request, img_id, user_id):
	img = Image.objects.get(pk=img_id)
	user = User.objects.get(pk=request.session['conectado'])
	img.repicers.add(user)
	img.save()
	return imageList(request, user_id=user_id)

def addFriend(request, user_id):
	user1 = UserProfile.objects.get(pk=request.session['conectado'])
	user2 = UserProfile.objects.get(pk=user_id)
	user1.amigos.add(user2)
	user1.save()
	return imageList(request, user_id=user_id)

def allImg(request):
	list = Image.objects.all()
	context = {'img1' : list }
	return render(request, 'actividad.html', context)

@login_required(login_url='/genericactivity')
def actividad(request):
	user = UserProfile.objects.get(pk=request.session['conectado'])
	list = Image.objects.filter(autor=user).order_by('-date')
	list2 = Image.objects.filter(repicers=user).order_by('-date')
	aux = user.amigos.all()
	list3 = Image.objects.filter(autor=aux).exclude(repicers=user).order_by('-date')
	listm = Mensaje.objects.filter(to=user).filter(leido=True)
	context = {'img1': list, 'img2' : list2, 'img3' : list3, 'user' : user, 'listm': listm}
	return render(request, 'actividad.html', context)

def enviarMensaje(request):
	if request.method == 'POST':
		form = newMensaje(request.POST)

		if form.is_valid():
			mensaje = form.save(commit=False)
			mensaje.fromu = UserProfile.objects.get(pk=request.session['conectado'])
			mensaje.save()
			return actividad(request)
	else:
		form = newMensaje()
		
	context= { 'form' : form }
	return render(request, 'enviar.html', context)

def mensajeDetail(request, mensaje_id):
	mensaje = Mensaje.objects.get(pk=mensaje_id)
	mensaje.leido = False
	mensaje.save()
	context = {'mensaje': mensaje}
	return render(request, 'mensaje.html', context)	

def enviados(request):
	user = UserProfile.objects.get(pk=request.session['conectado'])
	list = Mensaje.objects.filter(fromu=user).order_by('-date')
	context = { 'enviados' : list }
	return render(request, 'enviados.html', context)
	
def buzon(request):
	user = UserProfile.objects.get(pk=request.session['conectado'])
	list = Mensaje.objects.filter(to=user).order_by('leido').order_by('-date')
	context = { 'recibidos' : list}
	return render(request, 'buzon.html', context)



	
