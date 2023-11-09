from flask import Flask, render_template, request, jsonify, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
from pinecone_embed import get_answer

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('chat.html')

unanswered_conversations = []

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['user_message']

    # Llama a la función get_answer para obtener la respuesta del chatbot
    bot_response = get_answer(user_message)
    #bot_response = "Esto es una prueba"
    if bot_response == "No tengo la información que me pides en este momento." or "Solo puedo responder preguntas sobre ABET en la E3T.":  # Cambia esto con la lógica real de tu bot
        # Si el bot no sabe la respuesta, registra la conversación
        unanswered_conversations.append({"user_message": user_message, "bot_response": bot_response})
   
    return jsonify({'bot_response': bot_response})

@app.route("/unanswered_conversations", methods=["GET"])
def get_unanswered_conversations():
    # Devuelve las conversaciones no respondidas como JSON
    return render_template("admin.html", unanswered=unanswered_conversations)


@app.route("/delete_question", methods=["POST"])
def delete_question():
    question_to_delete = request.form.get("question")  # Obtiene la pregunta a eliminar desde el formulario
    
    # Busca la pregunta en la lista de preguntas no contestadas y elimínala
    for conversation in unanswered_conversations:
        if conversation["user_message"] == question_to_delete:
            unanswered_conversations.remove(conversation)
            break

    return redirect("/unanswered_conversations") 

if __name__ == '__main__':
    app.run(debug=True)