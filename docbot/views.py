from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
# from .chatbot_engine import process_message

def home(request):
    return render(request, 'home.html')
    
def chatbot(request):
    return render(request, 'chatbot.html')

def get_response(request):
    text = request.GET.get('text')
    response_text = "Hello World, your input text is: " + text
    print(response_text)
    return JsonResponse({'response': response_text})