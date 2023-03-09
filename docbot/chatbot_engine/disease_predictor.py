import os
import pickle
import pathlib
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

# current_directory = os.getcwd()
# chatbot_engine = os.path.abspath(os.path.join(current_directory, os.pardir))
# sub_directory = "ml_model"
# file_name = "knn_model.sav"
# file_path = pathlib.PurePath(chatbot_engine, sub_directory, file_name)
file_path_model = os.path.abspath('docbot/chatbot_engine/ml_model/knn_model.sav')

def load_dataset():
    """
    Clean and return the diseases & symptoms dataset in a dataframe.
    
    Returns
        df (dataframe): diseases & symptoms in a dataframe
    """
    df = pd.read_csv('raw_dataset/symptom_disease.csv')
    # remove hyphen
    for column in df.columns:
        df[column] = df[column].str.replace('_',' ')
    #remove trailing spaces
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    return df


def reformat_dataset():
    """
    Reformat and return the diseases & symptoms dataset into binary format

    Returns
        df (dataframe): diseases & symptoms dataset in binary format
    """
    df = load_dataset()
    n, m = df.shape

    # create a new dataframe having columns as unique values from old dataframe
    select_df = df.iloc[:, 1:]
    new_columns = pd.unique(select_df.values.ravel())
    new_columns = [x for x in new_columns if str(x) != 'nan']

    # the symptom list contains the symptoms for each disease
    symptoms_list = []
    for i in range(n):
        val = select_df.iloc[i].values
        val = val.tolist()
        val = [x for x in val if str(x) != 'nan']
        symptoms_list.append(val)
    
    new_df = pd.DataFrame(columns=new_columns, index=df.index)
    new_df["symptoms_list"] = symptoms_list
    new_df['disease'] = df['Disease']

    for col in new_columns:
        new_df[col] = new_df["symptoms_list"].apply(lambda x:1 if col in x else 0)
    
    df = new_df.drop("symptoms_list", axis=1)
    df.to_csv("processed_dataset/symptom_disease.csv", encoding='utf-8', index=False)

    return df

def train_model():
    """
    Train and save a knn model.

    """
    if not os.path.exists("processed_dataset/symptom_disease.csv"):
        df = reformat_dataset()
    else:
        df = pd.read_csv("processed_dataset/symptom_disease.csv")
    
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]


    knn = KNeighborsClassifier(n_neighbors=3, weights='uniform')
    knn.fit(X, y)
    pickle.dump(knn, open(file_path_model, "wb"))


def get_prediction(input):
    """
    Compute and return the prediction based on the knn model.
    
    Args
        input (ndarry): An array that represents the input symptoms from the user. 
    
    Returns
        prediction (string): A name of the disease that the model outputs based on the input.
    """
    if not os.path.exists(file_path_model):
        train_model()
    
    model = pickle.load(open(file_path_model, 'rb'))
    prediction = model.predict(input)
    
    return prediction

