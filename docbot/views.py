from django.shortcuts import render
from django.http import JsonResponse
from .chatbot_engine.message_predictor import get_response

def home(request):
    return render(request, 'home.html')
    
def chatbot(request):
    return render(request, 'chatbot.html')

def getResponse(request):
    text = request.GET.get('text')
    response_text = get_response(text)
    return JsonResponse({'text': response_text, 'user': False, 'chatbot': True})

# from django.views.generic.edit import FormView
# from django.urls import reverse_lazy
# from .forms import ChatbotForm
# from .machine_learning import predict_disease

# class ChatbotView(FormView):
#     template_name = 'chatbot.html'
#     form_class = ChatbotForm
#     success_url = reverse_lazy('chatbot')

#     def form_valid(self, form):
#         user_input = form.cleaned_data.get('input')
#         prediction = predict_disease(user_input)
#         self.extra_context = {'message': f'You may have {prediction}.'}
#         return super().form_valid(form)