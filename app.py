# -*- coding: utf-8 -*-

# Import des librairies
from flask import Flask, jsonify
import sklearn
import pandas as pd
import pickle
from lightgbm import LGBMClassifier

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

app = Flask(__name__)

#Chargement de la base de données
#data = pd.read_csv('Clients_test.csv')
data = pd.read_csv('Clients_test_dashboard.csv')

#Chargement du modèle
model = pickle.load(open('model_best_lgb.pkl', 'rb'))


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/prediction/<identifiant>')
def prediction(identifiant):
    print('identifiant du client = ', identifiant)

    # Récupération des données du client en question
    ID = int(identifiant)
    X = data[data['SK_ID_CURR'] == ID]

    X_sans_id = X.drop(columns='SK_ID_CURR')
    proba = model.predict_proba(X_sans_id)
    pred = model.predict(X_sans_id)

    # DEBUG
    # print('id_client : ', id_client)

    dict_final = {
        'prediction': int(pred),
        'proba': float(proba[0][0])
    }

    print('Nouvelle Prédiction : \n', dict_final)

    return jsonify(dict_final)


# lancement de l'application
if __name__ == "__main__":
    app.run(debug=True)
