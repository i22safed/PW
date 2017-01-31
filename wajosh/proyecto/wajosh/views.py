from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
from wajosh.models import UserProfile, Anuncio, Comentario, Categoria, Provincia, Mensaje
from django.shortcuts import render_to_response, get_object_or_404, redirect, render

#sistema de autenticacion
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
#from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

#sistema de plantillas
from django.template import RequestContext

from django.http import HttpResponse, HttpResponseRedirect

#formularios
from wajosh.forms import contactoForm, anuncioForm,SingUpForm,comentarioForm,nuevoMensaje, distribucionForm, ActualizarForm

from django.core.mail import EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # Paginador

def home(request):

	home=Anuncio.objects.all().order_by('-fecha')[:9]
	usuario=request.user
	#
	if request.method=='POST':
		formularioD = distribucionForm(request.POST)
		if formularioD.is_valid():
			formularioD.save()
			return HttpResponseRedirect('/')
	else:
		formularioD = distribucionForm()
	return render_to_response('wajosh/principal.html',{'home':home,'usuario':usuario,'formularioD':formularioD},context_instance=RequestContext(request))

def cabeza(request):

	usuario=request.user

	return render_to_response('index.html',{'usuario':usuario},context_instance=RequestContext(request))


def listar_anuncios(request):
	
	anuncios=Anuncio.objects.all()
	categoria=Categoria.objects.all()
	provincia=Provincia.objects.all()
	usuario=request.user
	paginator=Paginator(anuncios, 4) # Muestra de 3 en 3 comentarios por pagina
	page=request.GET.get('page')
	try:
		anuncios=paginator.page(page)
	except PageNotAnInteger:
		anuncios=paginator.page(1)
	except EmptyPage:
		anuncios=paginator.page(paginator.num_pages)

	return render_to_response('wajosh/listar_anuncios.html',{'provincia':provincia,'listar_anuncios':anuncios,'usuario':usuario,'categoria':categoria}, context_instance=RequestContext(request))

#def listar_anunciosP(request):
	
#	anunciosP=Anuncio.objects.all()

#	return render_to_response('index.html',{'listar_anunciosP':anunciosP}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def lista_usuarios(request):
	usuario=request.user
	usuarios=UserProfile.objects.all()
	provincia=Provincia.objects.all()
	paginator=Paginator(usuarios, 4) # Muestra de 3 en 3 comentarios por pagina
	page=request.GET.get('page')
	try:
		usuarios=paginator.page(page)
	except PageNotAnInteger:
		usuarios=paginator.page(1)
	except EmptyPage:
		usuarios=paginator.page(paginator.num_pages)

	return render_to_response('wajosh/lista_usuarios.html',{'lista_usuarios':usuarios, 'usuario':usuario,'provincia':provincia},context_instance=RequestContext(request))

def busquedaAlias(request):
	usuario=request.user
	alias=request.GET['alias']
	usuarioT=UserProfile.objects.filter(username__contains=alias)
	return render_to_response('wajosh/busquedaAlias.html',{'uAlias':usuarioT, 'usuario':alias, 'usuario':usuario},context_instance=RequestContext(request))


def busquedaProvinciaU(request):
	usuario=request.user
	provincia=request.GET['provincia']
	usuarioP=UserProfile.objects.filter(provincia__nombre__contains=provincia)
	return render_to_response('wajosh/busquedaPusuario.html',{'uPronvincia':usuarioP, 'provincia':provincia, 'usuario':usuario},context_instance=RequestContext(request))


#vista nuevo_usuario
def nuevo_usuario(request):
	if request.method=='POST':
		#formulario=UserCreationForm(resquest.POST)
		formulario=SingUpForm(request.POST, request.FILES)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/')
	else:
		formulario=SingUpForm()
	return render_to_response('wajosh/nuevo_usuario.html',{'formulario':formulario}, context_instance=RequestContext(request))


def contacto(request):
	usuario=request.user
	if request.method=='POST':
		formulario = contactoForm(request.POST)
		if formulario.is_valid():
			titulo ='Mensaje desde wajosh'
			contenido=formulario.cleaned_data['mensaje']+ "\n"
			contenido += 'Comunicarse a: ' + formulario.cleaned_data['correo']
			correo = EmailMessage(titulo, contenido, to=['wajosh2015@gmail.com'])
			correo.send()
			return HttpResponseRedirect('/')
	else:
		formulario=contactoForm()
	return render_to_response('wajosh/contacto.html',{'formulario':formulario,'usuario':usuario},context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def nuevo_anuncio(request):
	usuario=request.user
	if request.method=='POST':
		formulario =anuncioForm(request.POST, request.FILES)#, instance=request.user
		if formulario.is_valid():
			#formulario.save()
			com=formulario.save(commit=False)# Guardar sin enviar a la base de datos
			com.propietario=request.user# Ya que el campo es opcional el formulario valida, pero nosotros rellenamos este campo antes de guardar
			com.save()# Ahora que rellenamos el campo guardamos de verdad
			#return HttpResponseRedirect('/mizona/clasificados/usuario.id')
			return HttpResponseRedirect('/usuario/mizona/clasificados/%s' % usuario.id)
	else:
		data={'propietario': request.user.username}#s
		formulario = anuncioForm(initial=data)
	return render_to_response('wajosh/anuncioForm.html',{'formulario':formulario,'usuario':usuario}, context_instance=RequestContext(request))


def ingresar(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/privado')
	if request.method=='POST':
		formulario=AuthenticationForm(request.POST)
		if formulario.is_valid:
			usuario=request.POST['username']
			clave=request.POST['password']
			acceso=authenticate(username=usuario, password=clave)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso) #auth_login -sesion

					return HttpResponseRedirect('/')#/privado
				else:
					return render_to_response('wajosh/noactivo.html', context_instance=RequestContext(request))
			else:
				return render_to_response('wajosh/nousuario.html',context_instance=RequestContext(request))
	else:
		formulario=AuthenticationForm()
	return render_to_response('wajosh/ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def privado(request):
	usuario=request.user
	return render_to_response('wajosh/privado.html',{'usuario':usuario},context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def cerrar(request):
	logout(request)
	return HttpResponseRedirect('/')

@login_required(login_url='/ingresar')
def verAnuncio(request, id_anuncio):
	#anuncio=Anuncio.objects.filter(pk=2)
	usuario=request.user
	comentarios=Comentario.objects.filter(anuncio=id_anuncio)
	paginator=Paginator(comentarios, 2) # Muestra de 3 en 3 comentarios por pagina
	page=request.GET.get('page')
	try:
		comentarios=paginator.page(page)
	except PageNotAnInteger:
		comentarios=paginator.page(1)
	except EmptyPage:
		comentarios=paginator.page(paginator.num_pages)
	id_anuncio=get_object_or_404(Anuncio,pk=id_anuncio)	
	if id_anuncio.propietario.id==usuario.id:
		conectado=usuario.id
		return render_to_response('wajosh/verAnuncio.html',{'coment':comentarios,'anuncio':id_anuncio,'conectado':conectado,'usuario':usuario},context_instance=RequestContext(request))
	return render_to_response('wajosh/verAnuncio.html',{'coment':comentarios,'anuncio':id_anuncio,'usuario':usuario},context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def miZona(request, id_usuario):
	usuario=request.user
	id_usuario=get_object_or_404(UserProfile,pk=id_usuario)
	if id_usuario.username==usuario.username:
		conectado=usuario.id
		return render_to_response('wajosh/miZona.html',{'user':id_usuario,'conectado':conectado,'usuario':usuario},context_instance=RequestContext(request))
		#return redirect('/')
	return render_to_response('wajosh/miZona.html',{'user':id_usuario,'usuario':usuario},context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def clasificados(request, id_usuario):
	user=request.user
	usuario=UserProfile.objects.get(pk=id_usuario)
	anuncio=Anuncio.objects.filter(propietario=id_usuario)
	paginator=Paginator(anuncio, 3) # Muestra de 3 en 3 anuncios por pagina
	page=request.GET.get('page')
	try:
		anuncio=paginator.page(page)
	except PageNotAnInteger:
		anuncio=paginator.page(1)
	except EmptyPage:
		anuncio=paginator.page(paginator.num_pages)
	return render_to_response('wajosh/clasificados.html',{'clasificados':anuncio,'nombre':usuario, 'usuario':user},context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def eliminarCuenta(request, id_usuario):
	user=UserProfile.objects.get(pk=id_usuario)
	if user.username==request.user.username:
		user=get_object_or_404(UserProfile, pk=id_usuario)
		user.delete()
		return redirect('/')	
	else:
		return redirect('/')

@login_required(login_url='/login')
def eliminarAnuncio(request, id_anuncio):
	anuncio=Anuncio.objects.get(pk=id_anuncio)
	if anuncio.propietario.username==request.user.username:
		anuncio=get_object_or_404(Anuncio, pk=id_anuncio)
		anuncio.delete()
		return redirect('/')
	else:
		return redirect('/')

@login_required(login_url='/login')
def editarAnuncio(request, id_anuncio):
	usuario=request.user
	anuncio=Anuncio.objects.get(pk=id_anuncio)
	if anuncio.propietario.username==request.user.username:
		if request.method=='POST':
			formulario=anuncioForm(request.POST, request.FILES, instance=anuncio)
			if formulario.is_valid():
				formulario.save()
				return redirect('/verAnuncio/'+id_anuncio)
		else:
			formulario=anuncioForm(instance=anuncio)
		context={'formulario':formulario, 'usuario':usuario}
		return render(request,'wajosh/anuncioForm.html',context)
	else:
		return redirect('/')

@login_required(login_url='/login')
def editarPerfil(request, id_usuario):
	usuario=request.user
	perfil=UserProfile.objects.get(pk=id_usuario)
	if perfil.username==request.user.username:
		if request.method=='POST':
			formulario=ActualizarForm(request.POST, request.FILES, instance=perfil)
			if formulario.is_valid():
				formulario.save()
				return redirect('/usuario/mizona/'+id_usuario)
		else:
			formulario=ActualizarForm(instance=perfil)
		context={'formulario':formulario, 'usuario':usuario,'perfil':perfil}
		return render(request, 'wajosh/editarUsuario.html',context)
	else:
		return redirect('/')

@login_required(login_url='/ingresar')
def comentarios(request, id_anuncio):
	what=Anuncio.objects.get(pk=id_anuncio)
	usuario=request.user		
	if request.method=='POST':
		formucomentario = comentarioForm(request.POST)
		if formucomentario.is_valid():
			comi=formucomentario.save(commit=False)
			comi.propietario=request.user
			comi.anuncio=what
			comi.save()
			return HttpResponseRedirect('/verAnuncio/%s' % id_anuncio)
	else:
		data={'propietario': request.user.username}#s
		formucomentario = comentarioForm(initial=data)
	return render_to_response('wajosh/comentarioform.html',{'formucomentario':formucomentario,'usuario':usuario,'anuncioComent':what},context_instance=RequestContext(request))

def busquedaTitulo(request):
	usuario=request.user
	titulo=request.GET['titulo']
	anuncioT=Anuncio.objects.filter(titulo__contains=titulo)
	return render_to_response('wajosh/busquedaTitulo.html',{'aTitulo':anuncioT, 'titulo':titulo,'usuario':usuario} ,context_instance=RequestContext(request))


def busquedaProvincia(request):
	usuario=request.user
	provincia=request.GET['provincia']
	anuncioP=Anuncio.objects.filter(provincia__nombre__contains=provincia)
	return render_to_response('wajosh/busquedaProvincia.html',{'aPronvincia':anuncioP, 'provincia':provincia,'usuario':usuario},context_instance=RequestContext(request))
		

def busquedaCategoria(request):
	usuario=request.user
	categoria=request.GET['categoria'] 
	anuncioC=Anuncio.objects.filter(categoria__nombre__contains=categoria)
	return render_to_response('wajosh/busquedaCategoria.html',{'aCategoria':anuncioC, 'cat':categoria,'usuario':usuario},context_instance=RequestContext(request))

@login_required(login_url='/login')		
def mensajeDetail(request, mensaje_id):
	mensaje = Mensaje.objects.get(pk=mensaje_id)
	mensaje.leido = False
	mensaje.save()
	context = {'mensaje': mensaje}
	return render(request, 'wajosh/mensaje.html', context)

@login_required(login_url='/login')
def buzon(request):
	usuario=request.user		
	user = get_object_or_404(User,pk=usuario.id)						#date
	list = Mensaje.objects.filter(to=user).order_by('leido').order_by('-fecha')
	return render_to_response('wajosh/buzon.html',{'recibidos' : list,'usuario':usuario},context_instance=RequestContext(request))

@login_required(login_url='/login')
def enviarMensaje(request, id_usuario):
	receptor=UserProfile.objects.get(pk=id_usuario)
	usuario=request.user		
	if request.method == 'POST':
		form = nuevoMensaje(request.POST)

		if form.is_valid():
			mensaje = form.save(commit=False)
			mensaje.fromu = get_object_or_404(User,pk=usuario.id)
			mensaje.to = get_object_or_404(UserProfile,pk=receptor)
			mensaje.save()
			#return actividad(request)
			return redirect('wajosh/buzon.html')
	else:
		form = nuevoMensaje()
		

	return render_to_response('wajosh/enviar.html',{'form':form,'usuario':usuario,'receptor':receptor},context_instance=RequestContext(request))

@login_required(login_url='/login')
def mensajesEnviados(request):
	#user = UserProfile.objects.get(pk=request.session['conectado'])
	usuario=request.user
	usem = get_object_or_404(User,pk=usuario.id)
	list = Mensaje.objects.filter(fromu=usem).order_by('-fecha')

	return render_to_response('wajosh/enviados.html',{'enviados':list,'usuario':usuario},context_instance=RequestContext(request))

@login_required(login_url='/login')
def eliminarMensaje(request, id_mensaje):
	sms=Mensaje.objects.get(pk=id_mensaje)
	if sms.fromu.username==request.user.username or sms.to.username==request.user.username:
		sms=get_object_or_404(Mensaje, pk=id_mensaje)
		sms.delete()
		return redirect('/usuario/mizona/buzon/enviados/')
	else:
		return redirect('/usuario/mizona/buzon/')

def listaDistribucion(request):
	if request.method=='POST':
		formularioD = distribucionForm(request.POST)
		if formularioD.is_valid():
			formularioD.save()
			return HttpResponseRedirect('/')
	else:
		formularioD = distribucionForm()
	return render_to_response('wajosh/distribucion.html',{'formularioD':formularioD},context_instance=RequestContext(request))

@login_required(login_url='/login')	
def eliminarComentario(request, id_comentario):
	user=request.user
	comentario=Comentario.objects.get(pk=id_comentario)
	usuario=UserProfile.objects.get(pk=comentario.propietario.id)

	if comentario.propietario.id==usuario.id:
		comentario=get_object_or_404(Comentario, pk=id_comentario)
		comentario.delete()
		return redirect('/')
	else:
		return redirect('/')


#class Categorias(TemplateView):
#	template_name = "categorias.html"

def categorias(request):
	cates=Categoria.objects.all()

	return render_to_response('wajosh/categorias.html',{'listar':cates},context_instance=RequestContext(request))
