from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.views.generic import ListView, DetailView, FormView, UpdateView, DeleteView, FormView
from django.http import HttpResponse, HttpResponseRedirect
from .models import Circunscripcion, Mesa
from .forms import CircunscripcionForm, MesaForm
from django.template import RequestContext

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator

#####################################################clases

class CirListView(ListView):

	model = Circunscripcion
	template_name = 'listaCircunscripcion.html'


class FormCircunscripcion(FormView):

	form_class = CircunscripcionForm
	template_name = 'addCircunscripcion.html'
	success_url = '/'

	def form_valid(self, form):

		form.save()
		return super(FormCircunscripcion, self).form_valid(form)

	def form_invalid(self, form):
		return super(FormCircunscripcion, self).form_invalid(form)

	@method_decorator(login_required(login_url='/usuario/nuevo/'))
	def dispatch(self, *args, **kwargs):
		return super(FormCircunscripcion, self).dispatch(*args,**kwargs)



class EditarCircunscripcion(UpdateView):

	model = Circunscripcion
	template_name = 'editarCircunscripcion.html'
	success_url = '/'
	fields = ['nombreCir', 'nEscanos']

	@method_decorator(login_required(login_url='/usuario/nuevo/'))
	def dispatch(self, *args, **kwargs):
		return super(EditarCircunscripcion, self).dispatch(*args,**kwargs)


class BorrarCircunscripcion(DeleteView):

	model = Circunscripcion
	success_url = '/'
	template_name = 'borrarCircunscripcion.html'

	@method_decorator(login_required(login_url='/usuario/nuevo/'))
	def dispatch(self, *args, **kwargs):
		return super(BorrarCircunscripcion, self).dispatch(*args,**kwargs)

##########################################################funciones

@login_required(login_url='/usuario/nuevo/')
def AddMesa(request):

		if request.method=="POST":
			modelform = MesaForm(request.POST)
			if modelform.is_valid():
				modelform.save()
				return redirect("/") 
		else:
			modelform = MesaForm()

		return render(request,"addMesa.html", {"form": modelform})
	

def ListaMesa(request):
		listaMesa = Mesa.objects.prefetch_related('circunscripcion').order_by('circunscripcion') 
	

		return render(request, "listaMesa.html",{ "listaMesa": listaMesa})

def DetallesMesa(request, idmesa):
		detalle = Mesa.objects.get(pk=idmesa)

		return render(request, 'detallesMesa.html', {'detalle': detalle})

############################################################login

def Logearse(request):

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
			formulario = AuthenticationForm()
		return render_to_response('login.html', {'formulario':formulario}, context_instance=RequestContext(request))


	
@login_required(login_url='/usuario/nuevo/')
def LogOut(request):
	logout(request)
	return redirect('/')

########################################################cont_funciones

@login_required(login_url='/usuario/nuevo/')
def editarMesa(request, idmesa):
	
		entrada = Mesa.objects.get(pk=idmesa)
		if request.method == 'POST':
				formulario = MesaForm(request.POST, instance=entrada)
				if formulario.is_valid():
					formulario.save()
					return HttpResponseRedirect('/')
		else:
				formulario = MesaForm(instance=entrada)
		return render_to_response('editarMesa.html', {'formulario':formulario}, context_instance=RequestContext(request))
	
