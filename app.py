from flask import Flask
app = Flask(__name__)

@app.get("/")
def home():
    return "hello"

@app.after_request
def add_security_headers(response):
    #what the page may load: nothing. also no forms, and nobody may show it in a frame
    response.headers["Content-Security-Policy"] = "default-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'"
    response.headers["X-Content-Type-Options"] = "nosniff" #the browser must not guess the file type
    response.headers["X-Frame-Options"] = "DENY" #no frames, for old browsers that ignore frame-ancestors
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()" #nobody may use these
    #keep other websites separated from ours
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    return response

if __name__ == "__main__":
    app.run(port=5000)