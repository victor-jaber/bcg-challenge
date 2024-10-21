from flask import Flask, render_template, request, redirect, url_for
from functions.get_message import process_input_with_retrieval
from database import init_db, insert_message, get_messages, sqlite3
import markdown

app = Flask(__name__, static_url_path='/public', static_folder='public')
app.secret_key = 'your_secret_key'  # Set a secret key for sessions

# Initialize the database
init_db()


@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_query = request.form["pergunta"]

        # Store the user's message in the database
        insert_message("user", user_query)
        print(f"User message stored: {user_query}")

        # Process the input and get the response using the retrieval function
        response = process_input_with_retrieval(user_query)
        print(f"Response from process_input_with_retrieval: {response}")  # Log the response

        # Store the bot's response in the database
        insert_message("bot", response)
        print(f"Bot message stored: {response}")

        # Convert user query and bot response to Markdown
        user_query_md = markdown.markdown(user_query)
        response_md = markdown.markdown(response)

        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Return only the HTML of the chat history as a response
            return render_template("chat_history.html", historico_chat=get_messages(), user_query=user_query_md, bot_response=response_md)
        else:
            # Render the full page if it's a normal request
            return render_template("index.html", historico_chat=get_messages(), user_query=user_query_md, bot_response=response_md)

    return render_template("index.html", historico_chat=get_messages())

@app.route("/clear_history", methods=["POST"])
def clear_history():
    # Clear the chat history from the database
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM messages')
    conn.commit()
    conn.close()
    return redirect(url_for('chat'))  # Redirect to the main page

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