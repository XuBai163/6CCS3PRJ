import os
import pickle
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

file_path_model = os.path.abspath('docbot/chatbot_engine/ml_model/knn_model.sav')
file_path_raw_datset = os.path.abspath('docbot/chatbot_engine/datasets/raw_dataset/symptom_disease.csv')
file_path_processed_dataset = os.path.abspath('docbot/chatbot_engine/datasets/processed_dataset/symptom_disease.csv')

def load_dataset():
    df = pd.read_csv(file_path_raw_datset)
    # remove hyphen
    for column in df.columns:
        df[column] = df[column].str.replace('_',' ')
    #remove trailing spaces
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    return df


def reformat_dataset():
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
    df.to_csv(file_path_processed_dataset, encoding='utf-8', index=False)

    return df

def train_model():
    if not os.path.exists(file_path_processed_dataset):
        df = reformat_dataset()
    else:
        df = pd.read_csv(file_path_processed_dataset)
    
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]


    knn = KNeighborsClassifier(n_neighbors=3, weights='uniform')
    knn.fit(X, y)
    pickle.dump(knn, open(file_path_model, "wb"))


def get_prediction(input):
    if not os.path.exists(file_path_model):
        train_model()
    
    model = pickle.load(open(file_path_model, 'rb'))
    prediction = model.predict(input)
    
    return prediction

