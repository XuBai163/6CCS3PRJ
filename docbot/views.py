from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .chatbot_engine.message_processor import handle_input
from .forms import SignUpForm, LogInForm

def home(request):
    """
    """
    return render(request, 'home.html')
    
def chatbot(request):
    """
    """
    return render(request, 'chatbot.html')

def getResponse(request):
    """
    """
    text = request.GET.get('text')
    response = handle_input(text)
    return JsonResponse({'text': response, 'user': False, 'chatbot': True})

def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('chatbot')
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    form = LogInForm()
    return render(request, 'registration/login.html', {'form': form})

def log_out(request):
    logout(request)
    return render(request, 'home.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chatbot')
    else:
        form = SignUpForm()
    return render(request, 'registration/sign_up.html', {'form': form})
