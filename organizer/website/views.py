from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#from django.core.mail import send_mail
import re
from website.send_new_password import generate_new_password, send_reset_password

# Create your views here.


def organizer_logout(request):
    logout(request)
    return redirect("index")


def register(request):
    if request.user.is_authenticated():
        return redirect("organizer")

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if _validate_register(username, email, password) != True:
            password_error = _validate_register(username, email, password)
            return redirect("register")

        user = User.objects.create_user(username, email, password)
        return redirect("login")

    else:
        return render(request, "register.html", locals())


def _validate_register(username, email, password):
    if username is None or username.strip() == "":
        return False

    if email is None or email.strip() == "":
        return False

    if password is None or password.strip() == "":
        return False

    if len(password) < 8:
        password_error = "Password too short! Must be at least 8 symbols."
        return password_error

    if not re.search('[a-zA-Z]', password):
        password_error = "Your password must contain upper and lower case characters!"
        return password_error

    if not re.search('[0-9]', password):
        password_error = "Your password must contain digits!"
        return password_error

    return True


def index(request):
    if request.user.is_authenticated():
        return redirect("organizer")

    return render(request, "index.html", locals())


def user_login(request):
    if request.user.is_authenticated():
        return redirect("organizer")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("organizer")
        else:
            # TODO: Make some message for this
            login_error = "Wrong username or password!"
            return redirect("register")

    else:
        return render(request, "login.html", locals())


def password_reset(request):
    if request.user.is_authenticated():
        return redirect("organizer")

    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.get(email=email)
        if user is not None:
            new_password = generate_new_password()
            send_reset_password(email, new_password)
            user.set_password(new_password)
            user.save()
            return redirect("login")
        else:
            reset_password_error = "Wrong E-mail!!"
            return redirect("password_reset")

    else:
        return render(request, "password_reset.html", locals())


@login_required(login_url="login")
def organizer(request):
    return render(request, "organizer.html", locals())


def contact(request):
    return render(request, "contact.html", locals())
