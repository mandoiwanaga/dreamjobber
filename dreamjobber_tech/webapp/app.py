import random
import pandas as pd
import pickle
from flask import Flask, request, render_template, jsonify
#from recommend import *


#with open('.pkl', 'rb') as f:
 #   model = pickle.load(f)
app = Flask(__name__, static_url_path="")

@app.route('/')
def index():
    """Return the main page."""
    return render_template('index.html')


#@app.route('/predict', methods=['GET', 'POST'])
#def predict():
 #   """Return a random prediction."""
  #  data = request.json
   # prediction = model.predict_proba([data['user_input']])
    #return jsonify({'probability': prediction[0][1]})

