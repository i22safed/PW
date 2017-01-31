from django.shortcuts import render

# Create your views here.
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

import time
from calendar import month_name

from trueque.models import *

from django.forms import ModelForm
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from trueque.models import SingUpForm
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        widgets = {
            'password': forms.PasswordInput(),
        }
        
class FormularioComentario (ModelForm):
	class Meta:
		model = Comentario
		exclude = ["identrada"]
		
def poncomentario(request,pk):
	"""Add a new comment."""
	p = request.POST
	
	if 'mensaje' in p:
		autor = "Anonymous"
		if p["autor"]: autor = p["autor"]
		
		comentario = Comentario(identrada = Entrada.objects.get (pk=pk))
		cf = FormularioComentario(p, instance = comentario)
		cf.fields["autor"].required = False
		
		comentario = cf.save(commit=False)
		comentario.autor = autor
		comentario.save()
	return HttpResponseRedirect (reverse("trueque.views.entrada", args=[pk]))
	
class FormularioEntrada (ModelForm):
	class Meta:
		model = Entrada
		exclude = ["vendedor"]

def ponentrada(request):
	if request.method == "POST":
		form = FormularioEntrada(request.POST)
		if form.is_valid():
			entrada = form.save(commit=False)
			entrada.vendedor = request.user
			entrada.save()
			return HttpResponseRedirect('trueque.views.home')
	else:
		form = PostForm()
	return render(request, 'home.html', {'form': form})


def mkmonth_lst():
	if not Entrada.objects.count(): return[]
	
	year, month = time.localtime()[:2]
	first = Entrada.objects.order_by("fecha")[0]
	fyear = first.fecha.year
	fmonth = first.fecha.month
	months = []
	
	for y in range(year,fyear-1,-1):
		start,end = 12,0
		if y == year:start = month
		if y == fyear: end = fmonth -1
		
		for m in range(start,end,-1):
			months.append((y,m,month_name[m]))
	return months

def month(request,year,month):
	entrada = Entrada.objects.filter(fecha__year=year,fecha__month=month)
	return render_to_response("listado.html",dict(entrada_list=entrada, user=request.user,month=mkmonth_lst(),archive=True))

def entrada(request, pk):
		identrada = Entrada.objects.get(pk=int(pk))
		comentario = Comentario.objects.filter(identrada = identrada)
		d = dict(entrada= identrada,comentario = comentario, form=FormularioComentario(), usuario=request.user)
		d.update(csrf(request))
		return render_to_response("entrada.html",d)
		
def signup(request):
    if request.method == 'POST':
    	form = SignUpForm(request.POST)
    	if form.is_valid():
    		username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        email = form.cleaned_data["email"]
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
 
        return HttpResponseRedirect("/")  # Redirect after POST
    else:
        form = SignUpForm()
 
    data = {
        'form': form,
    }
    return render_to_response('register.html', data, context_instance=RequestContext(request))

@login_required()
def home(request):
    return render_to_response('home.html', {'user': request.user}, context_instance=RequestContext(request))
    
def main(request):
		entrada = Entrada.objects.all().order_by("-fecha") #ordenar por fecha descendente
		paginator = Paginator(entrada,3) #cada pagina tiene 3 entradas
		
		try: pagina = int(request.GET.get("page", '1'))
		except ValueError: pagina = 1
		
		try:
				entrada = paginator.page(pagina)
		except (InvalidPage, EmptyPage):
				entrada = paginator.page(paginator.num_pages)
				
		return render_to_response("listado.html", dict(entrada = entrada, usuario=request.user, entrada_list = entrada.object_list, months = mkmonth_lst()))
