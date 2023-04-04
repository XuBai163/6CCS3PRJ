import os
import re
import pandas as pd
import numpy as np
from .disease_predictor import get_prediction
from .message_predictor import get_response
from .nltk_utils import tokenize_words
from docbot.models import User, Symptom, Message, Disease


file_path_processed_dataset = os.path.abspath('docbot/chatbot_engine/datasets/processed_dataset/symptom_disease.csv')
disease_description = os.path.abspath('docbot/chatbot_engine/datasets/processed_dataset/symptom_description.csv')
disease_precautions = os.path.abspath('docbot/chatbot_engine/datasets/processed_dataset/precaution.csv')

df = pd.read_csv(file_path_processed_dataset)
df_description = pd.read_csv(disease_description)
df_precaution = pd.read_csv(disease_precautions)

symptoms = df.columns[:-1]
symptoms = [symptom for symptom in symptoms]
symptoms_len = len(symptoms)
command_words = ["clear", "info", "symptoms", "precaution"]
help_message = ''' 
            CLEAR: Clean chat, symptoms, and diseases. \n 
            INFO: Get infomation about the predicted disease. \n 
            SYMPTOMS: View inputted symptoms. \n 
            PRECAUTION: View precaution actions for the predicted disease. 
            '''

def get_multi_word_symptoms(symptoms_list):
    multi_word_symptoms = []
    
    for symptom in symptoms_list:
        if ' ' in symptom:
            multi_word_symptoms.append(symptom)
    
    return multi_word_symptoms

def check_command_words(input_text, user):
    sentence_words = tokenize_words(input_text)
    sentence_words = [word.lower() for word in sentence_words]
    response = None
    for word in sentence_words:
        if word == "help":
            return help_message
        if word == "clear":
            user.symptoms.clear()
            user.disease = None
            user.save()
            Message.objects.filter(user=user).delete()
            response = "Symptoms, disease, and chat history are cleared. Please refresh the page."
        elif word == "info":
            response = get_disease_info(user)
        elif word == "symptoms":
            user_symptoms = user.symptoms.all()
            user_symptoms = [sym.name for sym in user_symptoms]
            if len(user_symptoms) > 0:
                response = "You have inputted: "
                for sym in user_symptoms:
                    response += sym + "   "
            else:
                response = "You have not yet inputted any symptoms."
        elif word == "precaution":
            response = get_disease_precautions(user)
    return response

def handle_input(input_text, user):
    # first check for command word
    response = check_command_words(input_text, user)
    if response:
        return response 

    symptoms_from_input = []

    # then check for multi words symptoms
    multi_words_symptoms = get_multi_word_symptoms(symptoms)
    for symptom in multi_words_symptoms:
        if re.search(symptom, input_text):
            symptoms_from_input.append(symptom)

    # then check for single word symptoms
    sentence_words = tokenize_words(input_text)
    sentence_words = [word.lower() for word in sentence_words]
    for word in sentence_words:
        if word in symptoms:
            symptoms_from_input.append(word)

    # decide on which model to use
    if len(symptoms_from_input) != 0:
        response = predict_disease(symptoms_from_input, user)
    else:
        response = get_response(input_text)
    
    return response

def predict_disease(input_symptoms, user):
    idxs = []

    for symptom in input_symptoms:
        if user.symptom_exists(symptom):
            break
        symptom = Symptom.objects.create(name=symptom)
        user.symptoms.add(symptom)

    user_symptoms = user.symptoms.all()

    for symptom in user_symptoms:
        idxs.append(symptoms.index(symptom.name))

    input = np.array([[0 for i in range(symptoms_len)]])

    for idx in idxs:
        input[0][idx] = 1

    output_disease = get_prediction(input)[0]
    prediction = "Based on the symptoms that you have inputted. It is mostly likely that you have: " + output_disease
    current_user_disease = user.disease

    if user.disease is None or current_user_disease.name != output_disease:
        disease = Disease.objects.create(name=output_disease)
        user.disease = disease
        user.save()

    return prediction

def get_disease_info(user):
    disease_name = user.disease 
    if disease_name is not None:
        disease_name = disease_name.name
        description = df_description.loc[df_description['Disease'] == disease_name.lower(), 'Description'].values[0]
        return description
    return "You do not have a predicted disease yet. Input your symptoms to get a prediction."

def get_disease_precautions(user):
    disease_name = user.disease 
    if disease_name is not None:
        disease_name = disease_name.name
        disease_name = disease_name.lower()
        precautions = df_precaution.query(f"Disease == '{disease_name}'").iloc[0, 1:].tolist()

        response = "Precaution actions for " + disease_name + ": "
        for p in precautions:
            response += p + ", "
        return response
    return "You do not have a predicted disease yet. Input your symptoms to get a prediction."