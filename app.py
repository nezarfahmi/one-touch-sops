from flask import Flask, render_template, request, Response
from assistant.ask import ask_ai

app = Flask(__name__)

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/ask", methods=["GET","POST"])
def ask():
    answer = ""
    question = ""
    sources = []
    
    if request.method == "POST":
        question = request.form["question"]
        answer, sources = ask_ai(question)
    return render_template("ask.html", answer=answer, sources=sources, question=question)

if __name__ == "__main__":
  app.run(host='0.0.0.0',debug=True)