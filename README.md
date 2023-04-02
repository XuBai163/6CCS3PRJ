# 6CCS3PRJ Individual Undergraduate Project in Computer Science

### Project:
DocBot: A Web-Based Medical Chatbot for Disease Prediction using K-Nearest Neighbors and Neural Networks

### Installation instructions:

1. Download ** docbot ** file as a ZIP

2. Unzip the file

3. Go to ** docbot ** file in command prompt

```
$ cd docbot
```
4. Install all required packages:

```
$ pip3 install -r requirements.txt
```
5. Migrate the database:

```
$ python3 manage.py makemigrations
$ python3 manage.py migrate --run-syncdb
```

### Machine Learning Models Installation:

1. K-Nearest Neighbors:
The knn model is pre-trained and saved inside the "ml_model" folder. To retrain the knn model, delete the "knn_model.sav" in the folder and the knn model will be retrained once the user asks for a new prediction on the disease.

2. Artificial Neural Network:
The ann model is pre-tarined on the "intenst.json" file and saved inside the "ml_model" folder. To retrain the ann model, delete the "ann_model.sav" in the folder and the ann model will be retrained once the user sends a message to the chatbot.

### Sources


