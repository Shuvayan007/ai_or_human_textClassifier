import streamlit as st
import PyPDF2
import pickle
import re

# For text preprocessing (if necessary)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
import tensorflow as tf

# Dummy function to detect if text is AI generated (Replace with actual model predictions)
def predict_text_type(text, model_type='Logistic Regression'):
    # This is where you'd load your pre-trained model and vectorizer
    if model_type == 'Naive Bayes':
        model = pickle.load(open('naive_bayes.pkl', 'rb'))  # Load your Naive Bayes model
    elif model_type == 'Logistic Regression':
        model = pickle.load(open('logistic_regression.pkl', 'rb'))  # Load your Logistic Regression model
    else:
        # model_file = pickle.load(open('RNN.pkl', 'rb'))  # Load your RNN model
        model = tf.keras.models.load_model('RNN.h5')
        # with open("RNN.pkl", "rb") as f:
        #     model = pickle.load(f)

    # Example preprocessing of text
    vectorizer = pickle.load(open('tf_idf.pkl', 'rb'))  # Load the vectorizer for the model
    processed_text = vectorizer.transform([text]).toarray()     

    if not model_type == 'RNN':
        # Get the prediction
        prediction = model.predict(processed_text)
        
        # Example confidence score (modify according to your model output)
        confidence = model.predict_proba(processed_text)[0]

        return 'AI Generated' if prediction == 1 else 'Human Written', max(confidence) * 100

    else:
        processed_text_reshaped = processed_text.reshape(processed_text.shape[0], 1, processed_text.shape[1])
        prediction = model.predict(processed_text_reshaped)

        return 'AI Generated' if prediction > 0.5 else 'Human Written', prediction.item()*100 if prediction > 0.5 else (1-prediction.item())*100

    
# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# Streamlit Interface
st.title("AI vs Human Text Detector")

# Option to upload PDF or input text
option = st.selectbox("Choose input method:", ("Write Text", "Upload PDF"))

# If PDF upload is selected
if option == "Upload PDF":
    text = ""
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
        st.write("Extracted Text from PDF:")
        st.write(text)

# If text input is selected
else:
    text = st.text_area("Enter your text here:")

# Choose the model for detection
model_choice = st.selectbox("Choose a model for prediction:", ("Naive Bayes", "Logistic Regression", "RNN"))

# Once text is available, proceed with prediction
if not text == "":
    if st.button("Detect Text Type"):
        result, confidence = predict_text_type(text, model_choice)
        st.write(f"Prediction: {result}")
        st.write(f"Confidence: {confidence:.2f}%")
else:
    pass

