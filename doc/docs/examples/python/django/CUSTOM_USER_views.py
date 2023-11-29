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
