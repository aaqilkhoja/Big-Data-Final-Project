from flask import Flask
from flask import request
from pymongo import MongoClient
from flask_cors import CORS, cross_origin
from flask import jsonify, Response
from flask import render_template, request, url_for, redirect
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from bson.objectid import ObjectId

app = Flask(__name__)

#mongo code
client = MongoClient('localhost', 27017)
db = client.flask_db
todos = db.todos

model = pickle.load(open('../model.pkl', 'rb'))
vectorizer = pickle.load(open('../tfidf.pkl','rb'))
CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

# @app.route("/add", methods=["POST"], strict_slashes=False)
# @cross_origin()
def predict_val(to_pred):
    to_predict = []
    to_predict.append(to_pred)
    prediction = model.predict(vectorizer.transform(to_predict))
    
    output = prediction[0]
    if int(output) == 0:
        output_result = " Is Real News"
    else:
        output_result = " Is Fake News"

    return output_result 


@app.route('/', methods=("GET", "POST"))
def index():
    if request.method=='POST':
        content = request.form['content']
        degree = request.form['degree']
        todos.insert_one({'content': content, 'degree': degree})
        return redirect(url_for('index'))

    all_todos = todos.find()
    return render_template('index.html', todos=all_todos)


@app.post('/<id>/delete/')
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

@app.route("/result", methods=['POST'], strict_slashes=False)
@cross_origin()
def result():
    text = request.json.get('usertext')
    predicted = predict_val(text)
    print(predicted)
    # print(type(text))
    return jsonify("The Given News '" + text  + "'" + predicted)

if __name__ == "__main__":
    app.run(debug=True)

