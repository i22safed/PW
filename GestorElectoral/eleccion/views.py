from django.shortcuts import render, redirect
from eleccion.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic.base import View
from eleccion.models import *
from django.utils.decorators import method_decorator

# Create your views here.

def userLogin(request):
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            user = request.POST['username']
            passwd = request.POST['password']
            access = authenticate(username=user, password=passwd)
            if access is not None:
                if access.is_active:
                    login(request, access)
                    return redirect('/')
                else:
                    return render(request, 'inactive.html')
            else:
                return render(request, 'nouser.html')
    else:
        formulario = AuthenticationForm()
    context = {'formulario': formulario}
    return render(request, 'login.html', context)

@login_required(login_url='/login')
def userLogout(request):
    logout(request)
    return redirect('/')

class listCircunscripciones(View):
    template_name = 'circunscripciones.html'

    def get(self, request, *args, **kwargs):
        circunscripciones = Circunscripcion.objects.all()
        return render(request, self.template_name, {'circunscripciones': circunscripciones})

def is_supervisor(user):
    return user.groups.filter(name='supervisor').exists()

class addCircunscripcion(View):
    form_class = CircunscripcionForm
    template_name = 'addCircunscripcion.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_supervisor))
    def get(self, request, *args, **kwargs):
        formulario = self.form_class()
        return render(request, self.template_name, {'formulario': formulario})

    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_supervisor))
    def post(self, request, *args, **kwargs):
        formulario = self.form_class(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('/')
        return render(request, self.template_name, {'formulario': formulario})

class updateCircunscripcion(View):
    form_class = CircunscripcionForm
    template_name = 'updateCircunscripcion.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_supervisor))
    def get(self, request, *args, **kwargs):
        formulario = self.form_class()
        circunscripcion = Circunscripcion.objects.get(nombre=self.kwargs.get('nombre'))
        return render(request, self.template_name, {'formulario': formulario, 'circunscripcion': circunscripcion})

    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_supervisor))
    def post(self, request, *args, **kwargs):
        formulario = self.form_class(request.POST, request.FILES)
        if formulario.is_valid():
            circunscripcion = Circunscripcion.objects.get(nombre=self.kwargs.get('nombre'))
            circunscripcion.escanos = request.POST['escanos']
            circunscripcion.nombre = request.POST['nombre']
            circunscripcion.save()
            return redirect('/')
        return render(request, self.template_name, {'formulario': formulario})

class deleteCircunscripcion(View):
    template_name = 'deleteCircunscripcion.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_supervisor))
    def get(self, request, *args, **kwargs):
        circunscripcion = Circunscripcion.objects.get(nombre=self.kwargs.get('nombre'))
        return render(request, self.template_name, {'circunscripcion': circunscripcion})

    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_supervisor))
    def post(self, request, *args, **kwargs):
        circunscripcion = Circunscripcion.objects.get(nombre=self.kwargs.get('nombre'))
        circunscripcion.delete()
        return redirect('/')

def listMesas(request, nombre):
    if Circunscripcion.objects.filter(nombre=nombre).exists():
        circunscripcion = Circunscripcion.objects.get(nombre=nombre)
        mesas = circunscripcion.mesa_set.all()
        return render(request, 'mesas.html', {'circunscripcion': circunscripcion, 'mesas': mesas})
    else:
        return redirect('/notfound')

def mesa(request, nombre):
    if Mesa.objects.filter(nombre=nombre).exists():
        mesa = Mesa.objects.get(nombre=nombre)
        return render(request, 'mesa.html', {'mesa': mesa})
    else:
        return redirect('/notfound')

@login_required
@user_passes_test(is_supervisor)
def addMesa(request):
    if request.method == 'POST':
        formulario = MesaForm(request.POST, Mesa())
        if formulario.is_valid():
            formulario.save()
            return redirect('/')
    else:
        formulario = MesaForm()
    return render(request, 'addMesa.html', {'formulario': formulario})

@login_required
@user_passes_test(is_supervisor)
def updateMesa(request, nombre):
    if Mesa.objects.filter(nombre=nombre).exists():
        mesa = Mesa.objects.get(nombre=nombre)
        if request.method == 'POST':
            formulario = MesaForm(request.POST, Mesa())
            if formulario.is_valid():
                mesa.circunscripcion = Circunscripcion.objects.get(pk=request.POST['circunscripcion'])
                mesa.nombre = request.POST['nombre']
                mesa.save()
                return redirect('/')
        else:
            formulario = MesaForm()
        return render(request, 'updateMesa.html', {'formulario': formulario, 'mesa': mesa})
    else:
        return redirect('/notfound')

def is_gestor(user):
    return user.groups.filter(name='gestor').exists()

@login_required
@user_passes_test(is_gestor)
def addResultado(request):
    if request.method == 'POST':
        formulario = ResultadoForm(request.POST, Resultado())
        if formulario.is_valid():
            formulario.save()
            return redirect('/')
    else:
        formulario = ResultadoForm()
    return render(request, 'addResultado.html', {'formulario': formulario})

def asignacion(request, nombre):
    votos = []
    circunscripcion = Circunscripcion.objects.get(nombre=nombre)
    for x in range(2):
        maxPartido = ""
        maxVotos = 0
        for partido in Partido.objects.all():
            if not partido.nombre in votos:
                total = 0
                for mesa in circunscripcion.mesa_set.all():
                    for resultado in mesa.resultado_set.all():
                        if resultado.partido == partido:
                            total += resultado.votos
                if total > maxVotos:
                    maxVotos = total
                    maxPartido = partido.nombre
        votos.append(maxPartido)
    votos.insert(1, circunscripcion.escanos -1)
    votos.insert(3, 1)
    return render(request, 'asignaciones.html', {'circunscripcion': circunscripcion, 'votos': votos})
