from flask import Flask, request, jsonify, session, send_from_directory
import openai
import os

app = Flask(__name__)
app.secret_key = "some_secret_key"  

client = openai.OpenAI(api_key="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") 

def ask_gpt(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content

@app.route('/chat', methods=["POST"])
def chat():
    user_msg = request.json.get("message")
    
    if "conversation" not in session:
        session["conversation"] = [
            {"role": "system", "content": "You are a helpful Travel Assistant."}
        ]
    
    conversation = session["conversation"]
    conversation.append({"role": "user", "content": user_msg})
    
    reply = ask_gpt(conversation)
    conversation.append({"role": "assistant", "content": reply})
    
    session["conversation"] = conversation
    
    return jsonify({"reply": reply})

@app.route('/')
def home():
    return send_from_directory(os.getcwd(), 'index.html') 

if __name__ == "__main__":
    app.run(debug=True)
