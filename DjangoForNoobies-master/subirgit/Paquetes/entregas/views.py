from entregas.models import * 
from django.shortcuts import render
from django.http import HttpResponseRedirect
from entregas.forms import NewDestForm, NewPaqueteForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def DestinatariosView(request):
	destinatarios = Destinatario.objects.all()
	return render(request, 'destinatarios.html',{'destinatarios': destinatarios, })

@login_required(login_url = '/login')
def NewDestView(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/')
	if request.method=='POST':
		form = NewDestForm(request.POST)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/')
	else:
		form = NewDestForm()
	return render(request, 'newDest.html', {'form':form, })

def DetallesDest(request, id_dest):
	dest = Destinatario.objects.get(pk=id_dest)
	return render(request, 'detallesDest.html', {'dest': dest, })

def PaquetesView(request):
	paquetes = Paquete.objects.all()
	return render(request, 'paquetes.html',{'paquetes': paquetes, })

@login_required(login_url = '/login')
def NewPaqueteView(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/')
	if request.method=='POST':
		form = NewPaqueteForm(request.POST)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/')
	else:
		form = NewPaqueteForm()
	return render(request, 'newPaquete.html', {'form':form, })

def DetallesPaquete(request, id_paquete):
	paquete = Paquete.objects.get(pk=id_paquete)
	return render(request, 'detallesPaquete.html', {'paquete': paquete, })

@login_required(login_url = '/login')
def EditarPaquete(request, id_paquete):
	paquete = Paquete.objects.get(pk=id_paquete)
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/')
	if request.method == 'POST':
		form = NewPaqueteForm(request.POST, instance = paquete)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/')
	else:
		form = NewPaqueteForm(instance = paquete)

	return render(request, 'editarPaquete.html',{'form':form, })

def login_view(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/')
	if request.method == 'POST':
		form = AuthenticationForm(request.POST)
		if form.is_valid:
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect('/')
				else:
					return render(request, 'banned.html')
			else:
				return render(request, 'not_exist.html')
	else:
		form = AuthenticationForm()
	return render(request,'login.html', {'form': form, })

def newUser(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/')
	if request.method=='POST':
		form = UserCreationForm(request.POST)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/')
	else:
		form = UserCreationForm()
	return render(request, 'register.html', {'form': form, })

@login_required(login_url = '/login')
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')
