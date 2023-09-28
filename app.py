from flask import Flask, render_template, request, jsonify
from pinecone_embed import get_answer

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['user_message']

    # Llama a la función get_answer para obtener la respuesta del chatbot
    #bot_response = get_answer(user_message)
    bot_response = "Esto es una prueba"
    return jsonify({'bot_response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)