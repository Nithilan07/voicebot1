from flask import Flask, render_template, request, jsonify
import openai
import pdfplumber
from dotenv import load_dotenv  # Import load_dotenv function
import os

app = Flask(__name__)
load_dotenv()  # Load environment variables from .env file
openai.api_key ='OPENAI_API_KEY'  # Get OpenAI API key from environment variable

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to answer questions using OpenAI
def answer_question(question, context, max_tokens=100):
    shortened_context = context[:4000]  # Limit prompt length if necessary

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=shortened_context + "\nQuestion: " + question + "\nAnswer:",
        max_tokens=max_tokens
    )
    return response.choices[0].text.strip()

# Route to handle the form submission and generate answer
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            pdf_file = request.files['pdf']
            question = request.form['question']

            # Ensure a file is uploaded
            if pdf_file.filename == '':
                return jsonify({'error': 'No file selected'})

            # Extract text from the PDF file
            pdf_text = extract_text_from_pdf(pdf_file)

            # Answer the question using OpenAI
            answer = answer_question(question, pdf_text)

            return jsonify({'answer': answer})
        except Exception as e:
            return jsonify({'error': str(e)})

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
