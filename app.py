from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/AdaptLLM/finance-chat"  # Example model
HEADERS = {"Authorization": "Bearer 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"}  # Dummy token

def query_huggingface(message):
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
    HEADERS = {"Authorization": "Bearer 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"}  # Dummy token

    prompt = f"You are a financial assistant. Answer concisely:\nUser: {message}\nAssistant:"
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 150, "temperature": 0.7}
    }
    
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
                ai_response = data[0]["generated_text"]
                
                # Remove any repeated prompt text
                if "Assistant:" in ai_response:
                    ai_response = ai_response.split("Assistant:")[-1].strip()

                return ai_response
            else:
                return "Error: Unexpected response format from AI."
        else:
            return f"Error: {response.status_code} - {response.text}"

    except requests.exceptions.RequestException as e:
        return f"Error connecting to AI: {str(e)}"


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    """Endpoint to handle user queries and return AI-generated responses."""
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Please enter a valid question."})

    ai_response = query_huggingface(user_message)
    return jsonify({"response": ai_response})

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
