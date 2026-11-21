from flask import Flask
app = Flask(__name__)
AWS_KEY = "AKIAIOSFODNN7ABCDEFG"

@app.get("/")
def home():
    return "hello"

if __name__ == "__main__":
    app.run(port=5000)