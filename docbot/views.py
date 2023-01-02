import time
from django.shortcuts import render
from django.conf import settings

def chatbot(request):
    if request.method == 'POST':
        message = request.POST['message']
        messages = request.session.get('messages', [])
        messages.append(message)
        # Add a delay before the chatbot responds
        time.sleep(1)
        response = "This is the chatbot's response."
        messages.append(response)
        request.session['messages'] = messages
    else:
        messages = request.session.get('messages', [])
    return render(request, 'chatbot.html', {'messages': messages})
