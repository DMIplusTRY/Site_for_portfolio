from django import forms
from .models import Client
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .apps import user_registered

class ChangeUserInfoForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('username', 'mail', 'telephone_number', 'send_messages', 'first_name', 'last_name')


class RegisterUserForm(forms.ModelForm):
    mail = forms.EmailField(required=True, label='Адрес электронной почты')
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль(повторно)',
                                widget=forms.PasswordInput,
                                help_text='Введите тот же самый параль')

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2 and password1 and password2:
            errors = {'password2': ValidationError('Введенные пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registered.send(RegisterUserForm, isinstance=user) # Регистрация не работает так как
        # это не прописано в apps.py пакета приложения
        return user

    class Meta:
         model = Client
         fields =('username','mail','password1',
                  'password2', 'first_name', 'last_name', 'send_messages')