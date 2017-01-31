from django import forms
from ablog1.models import comentario, articulo, categoria, blog
from django.contrib.auth.models import User


class ComentarioForm(forms.ModelForm):
	class Meta:
		model=comentario
		fields=['texto']

class ArticuloForm(forms.ModelForm):
	class Meta:
		model=articulo
		fields=['titulo','cuerpo','categoria','imagen']

class categoriaForm(forms.ModelForm):
	class Meta:
		model=categoria

class blogForm(forms.ModelForm):
	class Meta:
		model=blog

class registroUsuario(forms.Form):
	username=forms.CharField(label="Nombre Usuario",widget=forms.TextInput())
	email=forms.EmailField(label="Email",widget=forms.TextInput())
	password1=forms.CharField(label="Password",widget=forms.PasswordInput(render_value=False))
	password2=forms.CharField(label="Confirmar Password",widget=forms.PasswordInput(render_value=False))

	def clean_username(self):
		username=self.cleaned_data['username']
		try:
			user=User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError('Nombre de usuario ya existente')

	def clean_email(self):
		email=self.cleaned_data['email']
		try:
			user=User.objects.get(email=email)
		except User.DoesNotExist:
			return email
		raise forms.ValidationError('Email ya existente')

	def clean_password2(self):
		password1=self.cleaned_data['password1']
		password2=self.cleaned_data['password2']
		if password1==password2:
			pass
		else:
			raise forms.ValidationError('Password no coincide')