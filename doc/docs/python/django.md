# Django

## `orchestrator.py`

??? example "orchestrator.py"

    ```py title=""
    from time import sleep
    from os import environ, system, listdir
    from os.path import isdir
    from sys import argv


    environ['DEBUG'] = 'True'
    environ['ALLOWED_HOSTS'] = '* 127.0.0.1'
    environ['DJANGO_SETTINGS_MODULE'] = '*****.settings.base'

    environ['EMAIL_HOST_USER'] = '*****'
    environ['EMAIL_HOST_PASSWORD'] = '*****'


    system('black -S .')
    # system('find -name "*.pyc" -type f -delete')
    system('rm -rf `find -type d -name __pycache__`')


    def collectstatic():
        system('python3 manage.py collectstatic --noinput')

    def makemigrations():
        exclude_list = ['.git', '.github', '.vscode', 'templates', 'static', 'CORE', 'LIPSUM', 'requirements', 'staticfiles', 'env']
        apps = [d for d in listdir('.') if isdir(d) and d not in exclude_list]
        system('python3 manage.py makemigrations ' + ' '.join(apps))

    def migrate():
        system('python3 manage.py migrate')    

    def test():
        makemigrations()
        migrate()
        environ['DEBUG'] = 'False'
        system('python3 manage.py collectstatic --noinput')

    def cleardb():
        system('rm -rf `find -type d -name migrations -not -path "./env/*"`')
        system('find -name "*.sqlite3" -type f -delete')
        exit(0)

    def populatedb():
        makemigrations()
        migrate()
        system(...)

    def docker():
        system(...)

    if argv[1] == 'runserver' and environ.get('DEBUG') == 'False': collectstatic()
    elif argv[1] == 'makemigrations': makemigrations(); exit()
    elif argv[1] == 'test': test()
    elif argv[1] == 'cleardb': cleardb()
    elif argv[1] == 'populatedb': populatedb(); exit()
    elif argv[1] == 'docker': docker(); system('python3 manage.py ' + ' '.join([i for i in argv[1:]])); exit()


    sleep(10)
    system('python3 manage.py ' + ' '.join([i for i in argv[1:]]))
    ```

---

## MEDIA and STATIC

??? example "settings.py"

    ```py title=""
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    STATICFILES_DIRS = [
        BASE_DIR / 'static',
    ]
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    ```

??? example "urls.py"

    ```py title=""
    urlpatterns += static(settings.MEDIA_URL, documemt_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, documemt_root=settings.STATIC_ROOT)
    ```

---

## Custom User

??? example "models.py"

    ```py title=""
    from django.contrib.auth.models import AbstractUser
    from django.db import models


    # Create your models here.
    class User(AbstractUser):
        first_name = models.CharField(max_length=150, blank=True)
        last_name = models.CharField(max_length=150, blank=True)
        email: object = models.EmailField(unique=True)


    class ActivationAccountToken(models.Model):
        value: object = models.CharField(max_length=128)
        used: object = models.BooleanField(default=False, verbose_name='Usado?')
        created: object = models.DateTimeField(auto_now_add=True)

        class Meta:
            verbose_name = 'Token de Ativação'
            verbose_name_plural = 'Tokens de Ativação'

        def __str__(self) -> str:
            return f'{self.value}'
    ```

??? example "forms.py"

    ```py title=""
    from django.contrib.auth import forms

    from .models import User


    class UserChangeForm(forms.UserChangeForm):
        class Meta(forms.UserChangeForm.Meta):
            model = User


    class UserCreationForm(forms.UserCreationForm):
        class Meta(forms.UserCreationForm.Meta):
            model = User
    ```

??? example "admin.py"

    ```py title=""
    from django.contrib import admin
    from django.contrib.auth import admin as auth_admin

    from .models import User, ActivationAccountToken
    from .forms import UserChangeForm, UserCreationForm


    # Register your models here.
    @admin.register(User)
    class UserAdmin(auth_admin.UserAdmin):
        add_fieldsets = (
            (
                None,
                {
                    'classes': ('wide',),
                    'fields': (
                        'username',
                        'first_name',
                        'last_name',
                        'email',
                        'password1',
                        'password2',
                    ),
                },
            ),
        )
        form = UserChangeForm
        add_form = UserCreationForm


    admin.site.register(ActivationAccountToken)
    ```

??? example "app/urls.py"

    ```py title=""
    from django.urls import path, URLPattern

    from . import views


    app_name = 'account'

    urlpatterns: list[URLPattern] = [
        path('registrar', views.register_view, name='register'),
        path('ativar/<uidb64>/<token>', views.activate_account, name='activate'),
        path('entrar', views.login_view, name='login'),
        path('sair', views.logout_view, name='logout'),
    ]
    ```

??? example "views.py"

    ```py title=""
    from django.shortcuts import get_object_or_404
    from django.utils.encoding import force_str
    from django.utils.http import urlsafe_base64_decode
    from django.urls import reverse
    from django.shortcuts import render
    from django.contrib.auth import authenticate, login, logout
    from django.contrib.auth.models import AbstractBaseUser
    from django.contrib.auth.decorators import login_required
    from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
    from django.forms import Form, CharField, TextInput, EmailField, PasswordInput
    from django.contrib import messages

    from .models import User, ActivationAccountToken
    from mail.views import send_activate_account_token, send_activate_account_done


    # Create your views here.
    class RegisterForm(Form):
        username: object = CharField(
            label='',
            max_length=50,
            required=True,
            widget=TextInput(
                attrs={
                    'placeholder': 'Username (nome de usuário)*',
                    'class': 'py-2',
                    'style': 'text-align: center;',
                    'autofocus': 'autofocus',
                }
            ),
            help_text='50 caracteres ou menos. Letras, números e @/./+/-/_ apenas.',
        )
        first_name: object = CharField(
            label='',
            required=True,
            widget=TextInput(
                attrs={
                    'placeholder': 'Nome*',
                    'class': 'mt-3 py-2',
                    'style': 'text-align: center;',
                }
            ),
        )
        last_name: object = CharField(
            label='',
            required=True,
            widget=TextInput(
                attrs={
                    'placeholder': 'Sobrenome*',
                    'class': 'py-2',
                    'style': 'text-align: center;',
                }
            ),
        )
        email: object = EmailField(
            label='',
            required=True,
            widget=TextInput(
                attrs={
                    'placeholder': 'Email*',
                    'class': 'mt-3 py-2',
                    'style': 'text-align: center;',
                }
            ),
        )
        password: object = CharField(
            label='',
            required=True,
            widget=PasswordInput(
                attrs={
                    'placeholder': 'Senha*',
                    'class': 'mt-3 py-2',
                    'style': 'text-align: center;',
                }
            ),
        )
        password2: object = CharField(
            label='',
            required=True,
            widget=PasswordInput(
                attrs={
                    'placeholder': 'Confirmação de senha*',
                    'class': 'mb-5 py-2',
                    'style': 'text-align: center;',
                }
            ),
        )


    class LogInForm(Form):
        username = CharField(
            label='',
            required=True,
            widget=TextInput(
                attrs={
                    'placeholder': 'Username*',
                    'class': 'py-2',
                    'style': 'text-align: center;',
                    'autofocus': 'autofocus',
                }
            ),
        )
        password: object = CharField(
            label='',
            required=True,
            widget=PasswordInput(
                attrs={
                    'placeholder': 'Pass*',
                    'class': 'mt-3 py-2',
                    'style': 'text-align: center;',
                }
            ),
        )


    def register_view(r: HttpRequest) -> HttpResponse | HttpResponseRedirect:
        if r.user.is_authenticated:
            return HttpResponseRedirect(reverse('home:index'))

        elif r.method == 'POST':
            form: Form = RegisterForm(r.POST)

            if form.is_valid():
                password: str = form.cleaned_data.get('password')
                password2: str = form.cleaned_data.get('password2')

                if not password or not password2 or password != password2:
                    messages.error(r, 'Senhas não compatíveis')
                    return render(r, 'account/register.html', {'form': form})

                username: str = form.cleaned_data.get('username')
                email: str = form.cleaned_data.get('email')

                if (
                    User.objects.filter(username=username).exists()
                    or User.objects.filter(email=email).exists()
                ):
                    messages.error(r, 'Username e/ou e-mail indisponível')
                    return render(r, 'account/register.html', {'form': form})

                first_name: str = form.cleaned_data.get('first_name')
                last_name: str = form.cleaned_data.get('last_name')

                user: User = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    is_active=False,
                )

                send_activate_account_token(r.get_host(), user, password)

                messages.success(
                    r, 'Conta criada. Acesse seu e-mail para ativar sua conta.'
                )
                return HttpResponseRedirect(reverse('account:login'))

            return render(r, 'account/register.html', {'form': form})

        form: Form = RegisterForm()
        return render(r, 'account/register.html', {'form': form})


    def activate_account(r: HttpRequest, uidb64: str, token: str) -> HttpResponseRedirect:
        token_obj: ActivationAccountToken = get_object_or_404(
            ActivationAccountToken, value=token, used=False
        )

        user: User | None = None

        try:
            id: int = int(force_str(urlsafe_base64_decode(uidb64)))
            user = get_object_or_404(User, pk=id)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None:
            user.is_active = True
            user.save()

            token_obj.used = True
            token_obj.save()

            login(r, user)

            send_activate_account_done(str(user.email))

            return HttpResponseRedirect(reverse('home:index'))

        raise Http404()


    def login_view(r: HttpRequest) -> HttpResponse | HttpResponseRedirect:
        if r.user.is_authenticated:
            return HttpResponseRedirect(reverse('home:index'))

        elif r.method == 'POST':
            form: Form = LogInForm(r.POST)

            if not form.is_valid():
                return render(r, 'account/login.html', {'form': form})

            username: str = str(form.cleaned_data.get('username')).strip()
            password: str = str(form.cleaned_data.get('password')).strip()

            user: AbstractBaseUser | None = authenticate(
                username=username, password=password
            )

            if user is None:
                messages.error(r, 'Username e/ou senha inválida')
                return render(r, 'account/login.html', {'form': form})

            login(r, user)
            return HttpResponseRedirect(reverse('home:index'))

        return render(r, 'account/login.html', {'form': LogInForm()})


    @login_required(login_url='/conta/entrar')
    def logout_view(r: HttpRequest) -> HttpResponse | HttpResponseRedirect:
        if r.method == 'POST':
            logout(r)
            return HttpResponseRedirect(reverse('account:login'))

        return render(r, 'account/logout.html')
    ```

??? example "&lt;project&gt;/urls.py"

    ```py title=""
    from django.contrib.auth.views import (
        PasswordResetView,
        PasswordResetDoneView,
        PasswordResetConfirmView,
        PasswordResetCompleteView,
    )

    urlpatterns += [
        path('reset', PasswordResetView.as_view(template_name='account/password_reset.html'), name='password_reset',),
        path('reset-enviado', PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name='password_reset_done',),
        path('reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html' ), name='password_reset_confirm',),
        path('reset-concluido', PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html' ), name='password_reset_complete',),
    ]
    ```

??? example "Reset password HTML snippet"

    ```html
    <form method="post" autocomplete="off">
        {% csrf_token %}

        <h1>Redefinir Senha</h1>
        <h6>Lorem ipsum dolor sit amet</h6>

        <br>

        {{ form|crispy }}

        <form method="post" autocomplete="off">
        {% csrf_token %}

        <h1>Redefinir Senha</h1>
        <h6>Certifique-se de inserir a mesma senha nos dois campos</h6>

        <br>

        {{ form|crispy }}

        {% if messages %}
        {% for message in messages %}
        <div class='alert {{ message.tags }} mt-3 py-2' role='alert'>{{ message }}</div>
        {% endfor %}
        {% endif %}

        <div>
            <input id="confirm-btn" class="btn btn-primary mt-4" type="submit" value="Enviar e-mail">
        </div>

    </form>{% endif %}

        <div>
            <input id="confirm-btn" class="btn btn-primary mt-4" type="submit" value="Enviar e-mail">
        </div>

    </form>
    ```

??? example "settings.py"

    ```py title=""
    # User Model
    AUTH_USER_MODEL = 'account.User'
    LOGOUT_REDIRECT_URL = 'conta/entrar'
    ```

---

## E-mail

??? example "settings.py"

    ```py title=""
    # E-mail configs
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD')
    ```

??? example "Send activation and confirm e-mails with `.py`"

    ```py title=""
    from typing import Final
    from hashlib import sha256

    from django.urls import reverse
    from django.utils.encoding import force_bytes
    from django.utils.http import urlsafe_base64_encode
    from django.http import HttpRequest, HttpResponseRedirect
    from django.core.mail import EmailMessage
    from django.conf import settings
    from django.contrib import messages

    from <user_app>.models import User, ActivationAccountToken
    from secret.models import Card, LoginCredential, SecurityNote


    # Create your views here.
    ACTIVATE_ACCOUNT_TOKEN_SEND: Final = """
    Sua conta foi criada com sucesso, contudo, você deve ativá-la. Para fazer isso, clique no link abaixo:

    {domain}/conta/ativar/{uidb64}/{token}


    Equipe Lipsum
    """

    ACTIVATE_ACCOUNT_CONFIRM_DONE: Final = """
    A partir de agora a sua conta está ativa e você pode utilizar dos recursos do sistema para armazenar seus dados sensíveis.


    Equipe Lipsum
    """


    def export_secrets(r: HttpRequest, secret_type: str) -> HttpResponseRedirect:
        csvfile: StringIO = StringIO()
        csvwriter = writer(csvfile, delimiter='¬', doublequote=True)

        email: EmailMessage = EmailMessage(
            subject='Exportação de Segredos | Lipsum',
            body=f'Aqui estão seus segredos armazenados em "{secret_type}" no Lipsum.\n\n\nEquipe Lipsum',
            from_email=settings.EMAIL_HOST_USER,
            to=[r.user.email],
        )

        if secret_type == 'Credenciais':
            if not LoginCredential.objects.filter(owner=r.user).exists():
                messages.error(r, 'Não há credenciais para exportar.')
                return HttpResponseRedirect(reverse('secret:credential_list_view'))

            csvwriter.writerow(
                ['Serviço', 'Apelido', 'Login 3rd', 'Apelido Login 3rd', 'Login', 'Senha']
            )

            for i in LoginCredential.objects.filter(owner=r.user):
                csvwriter.writerow(
                    [
                        i.get_service_display(),
                        i.name,
                        i.thirdy_party_login,
                        i.thirdy_party_login_name,
                        i.login,
                        i.password,
                    ]
                )

            email.attach('credenciais.csv', csvfile.getvalue(), 'text/csv')
            email.send()

            messages.success(r, 'Credenciais exportadas com sucesso.')
            return HttpResponseRedirect(reverse('secret:credential_list_view'))

        elif secret_type == 'Cartões':
            if not Card.objects.filter(owner=r.user).exists():
                messages.error(r, 'Não há cartões para exportar.')
                return HttpResponseRedirect(reverse('secret:card_list_view'))

            csvwriter.writerow(
                [
                    'Apelido',
                    'Tipo',
                    'Número',
                    'Expiração',
                    'CVV',
                    'Banco',
                    'Bandeira',
                    'Titular',
                ]
            )

            for i in Card.objects.filter(owner=r.user):
                csvwriter.writerow(
                    [
                        i.name,
                        i.get_card_type_display(),
                        i.number,
                        i.expiration,
                        i.cvv,
                        i.get_bank_display(),
                        i.get_brand_display(),
                        i.owners_name,
                    ]
                )

            email.attach('cartoes.csv', csvfile.getvalue(), 'text/csv')
            email.send()

            messages.success(r, 'Cartões exportados com sucesso.')
            return HttpResponseRedirect(reverse('secret:card_list_view'))

        elif secret_type == 'Anotações':
            if not SecurityNote.objects.filter(owner=r.user).exists():
                messages.error(r, 'Não há anotações para exportar.')
                return HttpResponseRedirect(reverse('secret:note_list_view'))

            csvwriter.writerow(['Título', 'Conteúdo'])

            for i in SecurityNote.objects.filter(owner=r.user):
                csvwriter.writerow([i.title, i.content])

            email.attach('anotacoes.csv', csvfile.getvalue(), 'text/csv')
            email.send()

            messages.success(r, 'Anotações exportadas com sucesso.')
            return HttpResponseRedirect(reverse('secret:note_list_view'))

        else:
            return HttpResponseRedirect(reverse('home:index'))


    def send_activate_account_token(domain: str, user: User, password: str) -> None:
        token_hash = sha256(f'{user.username}{password}'.encode()).hexdigest()
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        ActivationAccountToken.objects.create(value=token_hash, used=False)

        email: EmailMessage = EmailMessage(
            subject='Ativação de Conta | Lipsum',
            body=ACTIVATE_ACCOUNT_TOKEN_SEND.format(
                domain=domain, uidb64=uidb64, token=token_hash
            ),
            from_email=settings.EMAIL_HOST_USER,
            to=[str(user.email)],
        )
        email.send()


    def send_activate_account_done(user_email: str) -> None:
        email: EmailMessage = EmailMessage(
            subject='Ativação de Conta | Lipsum',
            body=ACTIVATE_ACCOUNT_CONFIRM_DONE,
            from_email=settings.EMAIL_HOST_USER,
            to=[user_email],
        )
        email.send()
    ```

---

## Messages

??? example "settings.py"

    ```py title=""
    from django.contrib.messages import constants as messages


    # Messages configs
    MESSAGE_TAGS = {
        messages.DEBUG: 'alert-primary',
        messages.ERROR: 'alert-danger',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
    }
    ```

??? example "Usage `.py` and `.html`"

    ```py title=""
    from django.contrib import messages


    messages.debug(r, 'Message content')
    messages.error(r, 'Message content')
    messages.info(r, 'Message content')
    messages.success(r, 'Message content')
    messages.warning(r, 'Message content')
    ```

    ```html title=""
    {% if messages %}
        {% for message in messages %}
            <div class='alert {{ message.tags }} mt-3 py-2' role='alert'>{{ message }}</div>
        {% endfor %}
    {% endif %}
    ```

---

## DB Integration

??? example "Connection"

    ```py title=""
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': environ.get('DATABASE_NAME'),
            'USER': environ.get('DATABASE_USER'),
            'PASSWORD': environ.get('DATABASE_PASSWORD'),
            'HOST': environ.get('DATABASE_HOST'),
            'PORT': '5432',
        }
    }
    ```

---

## `deploy.py`

??? example "deploy.py"

    ```py title=""
    from <project_name>.settings.base import *


    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': environ.get('DATABASE_NAME'),
            'USER': environ.get('DATABASE_USER'),
            'PASSWORD': environ.get('DATABASE_PASSWORD'),
            'HOST': environ.get('DATABASE_HOST'),
            'PORT': '5432',
        }
    }

    DEBUG = bool(environ.get('DEBUG', 'False'))
    SECRET_KEY = environ.get('SECRET_KEY')
    ALLOWED_HOSTS = str(environ.get('ALLOWED_HOSTS')).split(' ')


    # http -> https redirect
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    ```

---

## Custom err pages

??? example "&lt;project&gt;/urls.py"

    ```py title=""
    handler403 = '<err_app>.views.handle403'
    handler404 = '<err_app>.views.handle404'
    handler500 = '<err_app>.views.handle500'
    ```

??? example "&lt;err_app&gt;/views.py"

    ```py title=""
    from typing import Any

    from django.shortcuts import render
    from django.http import HttpRequest, HttpResponse


    # Create your views here.
    def handle<code: int>(r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return render(
            r,
            'err/error_template.html',
            {...}
        )
    ```

## Security

??? example "settings.py"

    ```py title=""
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    ```
