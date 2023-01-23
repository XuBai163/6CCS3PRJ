from django.shortcuts import render, redirect
from django.http import JsonResponse
# from .chatbot_engine import process_message

def home(request):
    return render(request, 'home.html')
    
def chatbot(request):
    # if request.method == 'POST':
    #     message = request.POST['message']
    #     # response = process_message(message)
    #     response = "Hello World!"
    #     return JsonResponse({'response': response})
    return render(request, 'chatbot.html')