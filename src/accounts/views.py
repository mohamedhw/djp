from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Profile
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, UserProfileForm
from django.contrib import messages
from Articels.models import Article
from django.contrib.auth.models import User
# Create your views here.

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            #log the user in
            return redirect("articles:list")
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form':form})




def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            #log in the user
            user = form.get_user()
            login(request, user)
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return redirect("articles:list")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form':form})




def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("articles:list")


@login_required
def profile(request):

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            print(p_form)
            messages.success(request, f'Your account has been updated!')
            return redirect('accounts:profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileForm(instance=request.user)
    context = {
        'u_form': u_form,   
        'p_form': p_form,
    }
    
    return render(request, 'accounts/profile.html', context)