from django.shortcuts import render
from basic_app.forms import UseInfo, UserProfileInfoForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')

# in order to logout the user, the user first must me logged in
# and because of that we are adding this decorator here
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    # check if someone is registered on the site
    registered = False

    if request.method == "POST":

        user_form = UseInfo(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # check if the forms (user,profile) are valid
        if user_form.is_valid() and profile_form.is_valid():

            # get the user_form and save it in the DB
            user = user_form.save()

            # hash the password
            user.set_password(user.password)

            # then save the hash password to the DB
            user.save()

            # deal whit the extra information definded in the model (website link and profile_pic)
            # commit=false --> to avoid colision whit the DB, NOT to override the user definded above
            profile = profile_form.save(commit=False)

            # 1:1 relation
            profile.user = user

            # check if the user provide profile_pic
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            # if both forms are valid, they need to be registered
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UseInfo()
        profile_form = UserProfileInfoForm()
    # the last one in render is context dictionary
    return render(request, 'basic_app/registration.html',
                  {'user_form':user_form,
                   'profile_form':profile_form,
                   'registered':registered})

def user_login(request):

    if request.method == 'POST':
        # get the username and password
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate the user, using the authenticate method imported from django library
        user = authenticate(username=username, password=password)

        # if the user is authenticated
        if user:
            # check if the account is still active
            if user.is_active:
                # login the user
                login(request,user)
                # send the user to some page
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account not active.")
        else:
            print("someone tried to login and failed")
            print("Username: {} and password: {}".format(username,password))
            return HttpResponse("invalid login detailes supplied!")
    else:
        return render(request, 'basic_app/login.html',{})
