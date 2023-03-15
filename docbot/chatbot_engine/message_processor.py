import os
import pandas as pd
import numpy as np
from .disease_predictor import get_prediction
from .message_predictor import get_response
from .nltk_utils import tokenize_words, stem

file_path_processed_dataset = os.path.abspath('docbot/chatbot_engine/datasets/processed_dataset/symptom_disease.csv')
df = pd.read_csv(file_path_processed_dataset)
symptoms = df.columns[:-1]
symptoms = [symptom for symptom in symptoms]
symptoms_len = len(symptoms)

def handle_input(input_text):
    """
    """
    sentence_words = tokenize_words(input_text)
    sentence_words = [word.lower() for word in sentence_words]
    symptoms_from_input = []

    for word in sentence_words:
        if word in symptoms:
            symptoms_from_input.append(word)

    if len(symptoms_from_input) != 0:
        response = predict_disease(symptoms_from_input)
    else:
        response = get_response(input_text)
    
    return response

def predict_disease(input_symptoms):
    """
    """
    idxs = []
    for symptom in input_symptoms:
        idxs.append(symptoms.index(symptom))

    input = np.array([[0 for i in range(symptoms_len)]])

    for idx in idxs:
        input[0][idx] = 1

    prediction = "The predicted disease is: " + get_prediction(input)[0]
    return prediction

