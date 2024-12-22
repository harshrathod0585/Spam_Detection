from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
from sklearn.feature_extraction.text import CountVectorizer
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the ML model and vectorizer
model = pickle.load(open('SpamClassifier.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

# Initialize NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
ps = PorterStemmer()

def text_transformer(text):
    text=text.lower()
    text = nltk.word_tokenize(text)
    y=[]
    for i in text:
        if i.isalnum() and i not in stopwords.words('english') and i not in string.punctuation :
            y.append(ps.stem(i))
    return " ".join(y)

@app.route('/predict', methods=['POST'])
def predict():
        data = request.json
        
        transformed_message = text_transformer(data['message'])

        print(transformed_message)
        # Transform input message
        vectorized_message = vectorizer.transform([transformed_message]).toarray()

        # Predict spam or ham
        prediction = model.predict(vectorized_message)[0]
        result = "Spam" if prediction == 1 else "Not Spam"
        print(result)
        return jsonify({"prediction": result})

if __name__ == '__main__':
    app.run(debug=True,port=5000)
