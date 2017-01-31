#encoding:utf-8 
from django.forms import ModelForm #usar los modelos ya declarados
from django import forms #nuevas reglas para un formulario
from wajosh.models import UserProfile, Anuncio,Comentario, Mensaje, Distribucion #modelos de nuestra aplicacion

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.localflavor.es.forms import ESIdentityCardNumberField


#formaulario contacto
class contactoForm(forms.Form):
	correo =forms.EmailField(label='Tu correo')
	mensaje =forms.CharField(widget=forms.Textarea)


class anuncioForm(ModelForm):
    class Meta:
        model = Anuncio
        exclude = ['fecha', 'propietario']


class SingUpForm(UserCreationForm):
#        password = forms.CharField(widget=forms.PasswordInput(render_value = False), required = True) 
	class Meta:
		model = UserProfile
#		fields = ['username', 'password', 'first_name', 'avatar', 'provincia','ciudad']	
		#fields = ['first_name','last_name','email', 'avatar', 'provincia','ciudad','codigo_postal','nif','telefono','username']
		fields = ['first_name','last_name','email', 'avatar', 'provincia','ciudad','username']		
#		widgets = {
#			'password': forms.PasswordInput(),		
	#		}


	def __init__(self, *args, **kwargs):
		super(SingUpForm, self).__init__(*args, **kwargs)
#		self.fields['password'].label = "Password"
		self.fields['first_name'].label = "Nombre"
		self.fields['last_name'].label = "Apellidos"
		self.fields['email'].label = "E-mail"
		self.fields['avatar'].label = "Avatar"
		self.fields['provincia'].label = "Provincia"
		self.fields['ciudad'].label = "Ciudad"
		self.fields['username'].label = "Usuario"


	def save(self, commit=True):
		user = super(SingUpForm, self).save(commit=False)
#		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user


class comentarioForm(ModelForm):
    class Meta:
        model = Comentario
        exclude = ('fecha', 'anuncio', 'propietario')


class nuevoMensaje(ModelForm):
	class Meta:
		model = Mensaje
		fields = ['texto','to', 'fromu']
		exclude = ('fecha',)

class distribucionForm(ModelForm):
	class Meta:
		model = Distribucion

#class distribucionForm(forms.Form):
#	correo= forms.EmailField(label='Correo@domino.xXx')

class ActualizarForm(ModelForm):
#        password = forms.CharField(widget=forms.PasswordInput(render_value = False), required = True) 
	class Meta:
		model = UserProfile
		fields = ['first_name','last_name','email', 'avatar', 'provincia','ciudad']		

	def __init__(self, *args, **kwargs):
		super(ActualizarForm, self).__init__(*args, **kwargs)
#		self.fields['password'].label = "Password"
		self.fields['first_name'].label = "Nombre"
		self.fields['last_name'].label = "Apellidos"
		self.fields['email'].label = "E-mail"
		self.fields['avatar'].label = "Avatar"
		self.fields['provincia'].label = "Provincia"
		self.fields['ciudad'].label = "Ciudad"
#		self.fields['password'].label = "Contraseña"


#	def save(self, commit=True):
#		user = super(ActualizarForm, self).save(commit=False)
#		user.set_password(self.cleaned_data["password"])
#		if commit:
#			user.save()
#		return user