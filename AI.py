from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
import google.generativeai as genai
import logging

app = Flask(__name__)
Bootstrap(app)

# Configure the generative AI API key
genai.configure(api_key="AIzaSyCw6H_31O2-MiZjdmxGj2ZUmVwT5ubBH-o")

# Create a generative model
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat()

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST', 'GET'])
def ask():
    try:
        if request.method == 'POST':
            user_input = request.form['user_input']
            # response = chat.send_message(user_input)
            response = model.generate_content(user_input)
            
            # Log the user input and response
            logging.info(f"User Input: {user_input}, Response: {response.text}")

            return render_template('index.html', user_input=user_input, response=response.text)
        else:
            # Redirect to the home page if the /ask route is accessed directly through a browser
            return redirect(url_for('index'))
    except Exception as e:
        # Log any exceptions that occur
        logging.error(f"Error occurred: {str(e)}")
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
