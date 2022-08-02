from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from cms.settings import EMAIL_HOST_USER
from .models import Article


class UserRegisterForm(UserCreationForm):
	username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
	email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
	password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
	username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
	password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class AddArticleForm(forms.ModelForm):
	class Meta:
		model = Article
		fields = ['title', 'content', 'is_published', 'category', 'tags']

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control'}),
			'content': forms.Textarea(attrs={'class': 'form-control'}),
			'category': forms.Select(attrs={'class': 'form-control'}),
			'tags': forms.SelectMultiple(attrs={'class': 'form-control'})
		}


class ContactForm(forms.Form):
	subject = forms.CharField(label='Тема сообщения', widget=forms.TextInput(attrs={'class': 'form-control'}))
	message = forms.CharField(label='Текст сообщения', widget=forms.Textarea(attrs={'class': 'form-control'}))

	def send_email(self):
		# mail = send_mail(
		# 	self.cleaned_data['subject'],
		# 	self.cleaned_data['message'],
		# 	EMAIL_HOST_USER,
		# 	['who_we_send_email@gmail.com'],
		# 	fail_silently=False,
		# )
		# if mail:
		# 	return True
		# else:
		# 	return False
		# Для теста отправляем всегда True, без реальной отправки email
		return True
