from django.shortcuts import render, redirect, get_object_or_404
from eleccion.models import *
from eleccion.forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
def usuarioLogin(request):
    if request.method=='POST':
        formulario=AutenticacionForm(request.POST)
        if formulario.is_valid:
            usuario=request.POST['username']
            clave=request.POST['password']
            acceso=authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request,acceso)
                    return redirect('/')
                else:
                    return render(request, 'errorLogin.html')
            else:
                return render(request, 'errorLogin.html')
    else:
        formulario=AutenticacionForm()
    contexto={'formulario':formulario,
              'navbar': "login"}
    return render(request,'login.html',contexto)


# Funcion para cerrar sesion en la pagina
@login_required(login_url='/login')
def usuarioLogout(request):
    logout(request)
    return redirect('/')

class listarCir(ListView):
    model = circunscripcion
    template_name = 'listarCir.html'

class crearCir(CreateView):
	model = circunscripcion
	fields = ['nombre','mesas']
	template_name = 'addCir.html'
	success_url="/circunscripciones"

class CirUpdate(UpdateView):
	model = circunscripcion
	fields = ['nombre','mesas']
	template_name = 'updateCir.html'
	success_url="/"

class DeleteCir(DeleteView):
	model = circunscripcion
	template_name = 'circunscripcion_confirm_delete.html'
	success_url="/circunscripciones"

def verCir(request,circunscripcion_id):
	cir = circunscripcion.objects.get(pk = circunscripcion_id)
	contexto = {'cir':cir}
	return render(request,'verCir.html',contexto)

def verMesa(request,mesa_id):
	mes = mesa.objects.get(pk = mesa_id)
	contexto = {'mes':mes}
	return render(request,'verMesa.html',contexto)

def editarMesa(request,mesa_id):
    mess = get_object_or_404(mesa, pk = mesa_id)

    if request.method == 'POST':
        formulario = mesaForm(request.POST,instance=mess)
        if formulario.is_valid():
            formulario.save()
            return redirect('/mesa/' + mesa_id)
    else:
        formulario = mesaForm(instance=mess)
    contexto = {'formulario': formulario}
    return render(request, 'editarMesa.html', contexto)
	
@staff_member_required
def borrarMesa(request,mesa_id):
	mes = get_object_or_404(mesa, pk = mesa_id)
	mes.delete()
	return redirect('/circunscripciones')

def editarCir(request,circunscripcion_id):
    cirr = get_object_or_404(circunscripcion, pk =circunscripcion_id)

    if request.method == 'POST':
        formulario = CirForm(request.POST,instance=cirr)
        if formulario.is_valid():
            formulario.save()
            return redirect('/circunscripcion/' + circunscripcion_id)
    else:
        formulario = CirForm(instance=cirr)
    contexto = {'formulario': formulario}
    return render(request, 'addMesa.html', contexto)
