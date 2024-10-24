from flask import Flask, render_template, request, redirect, url_for
from database import init_db, insert_message, get_messages, sqlite3
import markdown

app = Flask(__name__, static_url_path='/public', static_folder='public')
app.secret_key = 'your_secret_key'  # Defina uma chave secreta para sessões

# Inicializa o banco de dados
init_db()

@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_query = request.form["pergunta"]

        # Armazena a mensagem do usuário no banco de dados
        insert_message("user", user_query)
        print(f"User message stored: {user_query}")

        # Retorna uma resposta fixa em vez de processar com a função ausente
        response = "Sorry, I don't have a response for that yet."
        print(f"Response: {response}")  # Exibe a resposta fixa no log

        # Armazena a resposta do bot no banco de dados
        insert_message("bot", response)
        print(f"Bot message stored: {response}")

        # Converte a pergunta e a resposta para Markdown
        user_query_md = markdown.markdown(user_query)
        response_md = markdown.markdown(response)

        # Verifica se a requisição é AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Retorna apenas o histórico do chat como resposta
            return render_template("chat_history.html", historico_chat=get_messages(), user_query=user_query_md, bot_response=response_md)
        else:
            # Renderiza a página completa se for uma requisição normal
            return render_template("index.html", historico_chat=get_messages(), user_query=user_query_md, bot_response=response_md)

    # Renderiza a página inicial com o histórico do chat
    return render_template("index.html", historico_chat=get_messages())

@app.route("/clear_history", methods=["POST"])
def clear_history():
    # Limpa o histórico do chat no banco de dados
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM messages')
    conn.commit()
    conn.close()
    return redirect(url_for('chat'))  # Redireciona para a página principal

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/help")
def help():
    return render_template("help.html")

if __name__ == '__main__':
    app.run(debug=True)
