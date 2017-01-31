from django.shortcuts import render, render_to_response, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.views import generic
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from . import models
from blog.models import Comentario, Entry, Mensaje
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from blog.forms import ComentarioForm, EntradaForm, TagsForm, MensajeForm
from datetime import datetime
from time import strftime
from django.views.generic import DayArchiveView

MONTH_NAMES = ('', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre')


def BlogIndex(request):
	entradas = Entry.objects.filter(publish = True)
	paginator = Paginator(entradas, 2)
	comentarios = Comentario.objects.all()

	try: page = int(request.GET.get("page", '1'))
	except ValueError: page = 1

	try:
		entradas = paginator.page(page)
	except (InvalidPage, EmptyPage):
		entradas = paginator.page(paginator.num_pages)

	return render_to_response("home.html", {"entradas":entradas, "comentarios":comentarios,}, context_instance=RequestContext(request))

#class BlogDetail(generic.DetailView):
	#model = models.Entry
	
	#template_name = "post.html"

	#def comentarios(request, id_entrada):
	#comentario=Comentario.objects.filter(entry=id_entrada)
	#return render_to_response('post.html', {"comentarios":comentario}, context_instance=RequestContext(request))

def BlogDetail(request, slug):
	get_entrada = get_object_or_404(Entry, slug = slug)
	comentarios = Comentario.objects.filter(entry = get_entrada)
	num_comentarios = len(comentarios)


	return render_to_response('post.html', {"comentarios":comentarios, "entrada":get_entrada, "num_comentarios":num_comentarios}, context_instance=RequestContext(request))

def nuevo_usuario(request):
	if request.method=='POST':
		formulario = UserCreationForm(request.POST)
		if formulario.is_valid:
			formulario.save()
			return HttpResponseRedirect('/')
	else:
		formulario = UserCreationForm()
	return render_to_response('nuevousuario.html', {'formulario':formulario}, context_instance=RequestContext(request))

def nuevocomentario(request, id_entrada):
	entry=Entry.objects.get(pk=id_entrada)
	usuario = request.user
	if usuario.is_authenticated():
		usuario = request.user
	else:
		usuario = None
	if request.method=='POST':
		formulario=ComentarioForm(request.POST)
		if formulario.is_valid():
			comment = formulario.save(commit=False)
			comment.entry=entry
			comment.user=usuario
			comment.save()
			return HttpResponseRedirect('/entry/%s' % entry.slug)
	else:
		formulario=ComentarioForm()
	return render_to_response('comentarioform.html', {'formulario':formulario, 'entrada':entry}, context_instance=RequestContext(request))

def panel_usuario(request, id_usuario):
	usuario = User.objects.filter(pk=id_usuario)


	return render_to_response('panel_usuario.html', {'usuario':usuario})

@login_required(login_url='/usuario/nuevo')
def nuevaentrada(request):
	usuario = request.user
	if usuario.is_staff:
		if request.method=='POST':
			formulario=EntradaForm(request.POST)
			if formulario.is_valid():
				entrada=formulario.save(commit=False)
				entrada.author=usuario
				entrada.publish=True
				entrada.slug=slugify(entrada.title)
				entrada.save()
				return HttpResponseRedirect('/')
		else:
			formulario=EntradaForm()
		return render_to_response('entradaform.html', {'formulario':formulario}, context_instance=RequestContext(request))
	else:
		return render_to_response('noautorizado.html', {"usuario":usuario}, context_instance=RequestContext(request))

def ingresar(request):
	if request.method == 'POST':
		formulario = AuthenticationForm(request.POST)
		if formulario.is_valid:
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username=usuario, password=clave)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return HttpResponseRedirect('/')
				else:
					return render_to_response('noactivo.html', context_instance=RequestContext(request))
			else:
				return render_to_response('nousuario.html', context_instance=RequestContext(request))
	else:
		formulario = AuthenticationForm()
	return render_to_response('ingresar.html', {'formulario':formulario}, context_instance=RequestContext(request))

@login_required(login_url='/usuario/nuevo')
def creartags(request):
	if request.method == 'POST':
		formulario = TagsForm(request.POST)
		if formulario.is_valid:
			formulario.save()
			return HttpResponseRedirect('/publicar/')
	else:
		formulario = TagsForm()
	return render_to_response('creartags.html', {'formulario':formulario}, context_instance=RequestContext(request))

@login_required(login_url='/usuario/nuevo/')
def cerrarsesion(request):
	logout(request)
	return HttpResponseRedirect('/')

@login_required(login_url='/usuario/nuevo/')
def mensajes(request):
	usuario=request.user
	if usuario.is_superuser:
		mensajes=Mensaje.objects.all()

		return render_to_response('mensajes.html', {'mensajes':mensajes, 'usuario':usuario}, context_instance=RequestContext(request))
	else:
		return render_to_response('noautorizado.html', context_instance=RequestContext(request))

@login_required(login_url='/usuario/nuevo/')
def enviarmensaje(request):
	usuario = request.user
	if request.method == 'POST':
		formulario = MensajeForm(request.POST)
		if formulario.is_valid():
			mensaje = formulario.save(commit=False)
			mensaje.user=usuario
			mensaje.save()
			return HttpResponseRedirect('/')
	else:
		formulario = MensajeForm()
	return render_to_response('nuevomensaje.html', {'formulario':formulario}, context_instance=RequestContext(request))

def eliminarmensaje(request, id_mensaje):
	usuario=request.user
	if usuario.is_superuser:
		mensaje=Mensaje.objects.get(pk=id_mensaje)
		mensaje.delete()
		return render_to_response('mensajeliminado.html', context_instance=RequestContext(request))
	else:
		return render_to_response('noautorizado.html', context_instance=RequestContext(request))

def editarentrada(request, id_entrada):
	usuario = request.user
	entrada = Entry.objects.get(pk=id_entrada)
	if usuario == entrada.author:
		if request.method == 'POST':
			formulario = EntradaForm(request.POST, instance=entrada)
			if formulario.is_valid():
				formulario.save()
				return HttpResponseRedirect('/entry/%s' % entrada.slug)
		else:
			formulario = EntradaForm(instance=entrada)
		return render_to_response('entradaform.html', {'formulario':formulario}, context_instance=RequestContext(request))
	else:
		return render_to_response('noautorizado.html', context_instance=RequestContext(request))

def delete_comment(request, id_entrada, pk=None):
	entrada=Entry.objects.get(pk=id_entrada)
	if request.user.is_superuser:
		if not pk: pklst = request.POST.getlist("delete")
		else: pklst = [pk]

		for pk in pklst:
			Comentario.objects.get(pk=pk).delete()
		return HttpResponseRedirect('/entry/%s' % entrada.slug)

class EntradasDia(DayArchiveView):
	queryset=Entry.objects.order_by('created')
	template_name='entradas_dia.html'
	date_field = 'created'
	context_object_name='entradas'
	month_format = '%m'

def eliminarentrada(request, id_entrada):
	entrada=Entry.objects.get(pk=id_entrada)
	usuario = request.user
	if usuario==entrada.author or usuario.is_superuser:
		entrada.delete()
		return HttpResponseRedirect('/')
	else:
		return render_to_response('noautorizado.html', context_instance=RequestContext(request))

def confirmacioneliminar(request, id_entrada):
	entrada=Entry.objects.get(pk=id_entrada)
	usuario=request.user
	if usuario==entrada.author or usuario.is_superuser:
		return render_to_response('confirmacion.html', {'entrada':entrada}, context_instance=RequestContext(request))
	else:
		return render_to_response('noautorizado.html', context_instance=RequestContext(request))