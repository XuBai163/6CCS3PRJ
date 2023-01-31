from django.shortcuts import render
from django.http import JsonResponse
# from .chatbot_engine import process_message

def home(request):
    return render(request, 'home.html')
    
def chatbot(request):
    return render(request, 'chatbot.html')

def getResponse(request):
    text = request.GET.get('text')
    response_text = "Hello World, your input text is: " + text
    return JsonResponse({'text': response_text, 'user': False, 'chatbot': True})
