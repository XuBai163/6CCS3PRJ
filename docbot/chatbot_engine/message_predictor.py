import os
import json
import random
import pickle
import numpy as np
from keras.layers import Dense
from keras.optimizers import SGD
from keras.models import Sequential
from .nltk_utils import tokenize_words, stem, bag_of_words

file_path_model = os.path.abspath('docbot/chatbot_engine/ml_model/nn_model.sav')

def load_data():
    """
    """
    file_path_data = os.path.abspath('docbot/chatbot_engine/datasets/intents.json')
    with open(file_path_data, 'r') as file:
        data = json.load(file)
    return data

def create_tokenize():
    data = load_data()

    words = []
    labels = []
    docs_x = []
    docs_y = []
    ignore_words = ["?", ".", "!"]

    for intent in data['intents']:
        for pattern in intent['patterns']:
            wrds = tokenize_words(pattern)

            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent['tag'])

        if intent['tag'] not in labels:
            labels.append(intent['tag'])

    labels = sorted(list(set(labels)))
    words = [stem(w.lower()) for w in words if w not in ignore_words]
    words = list(set(words))

    return words, labels, docs_x, docs_y

def create_training_data():
    words, labels, docs_x, docs_y = create_tokenize()

    training = []
    output = []
    out_empty = [0] * len(labels)

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stem(w.lower()) for w in doc]
        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)

    return training, output

def train_model():
    training, output = create_training_data()

    model = Sequential()
    model.add(Dense(128, input_shape=(len(training[0]),), activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(len(output[0]), activation='softmax'))

    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

    model.fit(training, output, epochs=200, batch_size=8, verbose=1)
    
    pickle.dump(model, open(file_path_model, "wb"))
    
def get_response(input_text, threshold=0.1):
    if not os.path.exists(file_path_model):
        train_model()
        print("THE MODEL IS TRAINED")

    intents = load_data()
    words, classes, docs_x, docs_y = create_tokenize() 

    sentence_words = tokenize_words(input_text)
    sentence_words = [stem(word.lower()) for word in sentence_words]

    input_bag = bag_of_words(sentence_words, words)
    input_bag = np.array(input_bag).reshape(1, -1)

    model = pickle.load(open(file_path_model, 'rb'))

    results = model.predict([input_bag])[0]
    results = [[i, r] for i, r in enumerate(results) if r > threshold]
    results.sort(key=lambda x: x[1], reverse=True)

    response = "I'm sorry, I didn't understand that. Could you please try again?"

    if results:
        for result in results:
            tag = classes[result[0]]
            for intent in intents['intents']:
                if tag == intent["tag"]:
                    return random.choice(intent['responses'])
        
    return response