from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.




#index view
def index(request):
    return render(request, 'shop/index.html')

#create the register view using shop/register.html template
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})
#create a login view using shop/login.html template
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('index')  
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})
#create logout 
@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')
