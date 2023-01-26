from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
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

@csrf_exempt
def hello_world(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = {"message": "Hello World!"}
        return JsonResponse(response)