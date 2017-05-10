# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect

from forms import SignUpForm

turno = {
        'farmacia': 0,
        'obra_social': 0,
        'pami': 0,
        'particular': 0,
}

@login_required()
def home(request):
    return render(request, 'atencion.html', {'user': request.user})


# Create your views here.
def main(request):
    return render(request, 'main.html', {})


def totem(request):
    return render(request, 'totem.html', {})


def data(request):
    import ipdb; ipdb.set_trace()
    if len(request.POST.values()) > 0:
        turno[str(request.POST['turno'])] = turno[str(request.POST['turno'])] + 1

    return render(request, 'totem.html', {})


def signup(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = SignUpForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass

            # Process the data in form.cleaned_data
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            # At this point, user is a User object that has already been saved
            # to the database. You can continue to change its attributes
            # if you want to change other fields.
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name

            # Save new user attributes
            user.save()

            return HttpResponseRedirect(reverse('main'))  # Redirect after POST
    else:
        form = SignUpForm()

    data = {
        'form': form,
    }
    return render(request, 'signup.html', data)
