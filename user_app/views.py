from django.shortcuts import render
from user_app.forms import UserForm, UserProfileInfoForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def index(request):
    return render(request, 'user_app/index.html')


# require user login with decorator for special login notification function and logout function
@login_required
def special(request):
    return HttpResponse("You're logged in!")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    # check if user is registered
    registered = False

    if request.method == 'POST':
        # grab information from user form
        user_form = UserForm(data=request.POST)
        # grab information from profile info form
        profile_form = UserProfileInfoForm(data=request.POST)

        # check if both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # grab user form and save it to database
            user = user_form.save()
            # hash password with set method
            user.set_password(user.password)
            # save hashed password
            user.save()

            profile = profile_form.save(commit=False)
            # define one to one relationship
            profile.user = user

            # check for proile picture
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            # save model
            profile.save()
            # set user as registered
            registered = True

        else:
            # if either form is invalid print error
            print(user_form.errors, profile_form.errors)
    # if user never posts any information to forms, set user and profile forms
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    # return forms
    return render(request, 'user_app/registration.html', {'user_form': user_form, 'profile_form': profile_form, 'registered' : registered})


def user_login(request):

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            # automatic user authentication
            user = authenticate(username=username, password=password)

            if user:
                # if account is active redirect user to homepage index
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                # if account is inactive respond with account not active
                else:
                    return HttpResponse("ACCOUNT NOT ACTIVE")
            else:
                print("Someone tried to login and failed!")
                print("Username: {} and password {}".format(username, password))
                return HttpResponse("INVALID LOGIN DETAILS")
        # if user submits nothing return login page
        else:
            return render(request, 'user_app/login.html', {})
