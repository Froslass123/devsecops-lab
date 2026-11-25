import sqlite3

from flask import Flask, render_template, request
app = Flask(__name__)

#a small database in memory, recreated at every start
db = sqlite3.connect(":memory:", check_same_thread=False)
db.execute("CREATE TABLE notes (text TEXT)")
db.executemany("INSERT INTO notes VALUES (?)", [("hello there",), ("learn devsecops",), ("walk the dog",)])
db.commit()

@app.get("/")
def home():
    search = request.args.get("search", "") #what comes after ?search= in the URL
    #the ? keeps the input as data, so it can never become part of the SQL command
    notes = db.execute("SELECT text FROM notes WHERE text LIKE ?", (f"%{search}%",)).fetchall()
    return render_template("home.html", search=search, notes=notes)

@app.after_request
def add_security_headers(response):
    #what the page may load: nothing. also no forms, and nobody may show it in a frame
    response.headers["Content-Security-Policy"] = "default-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'"
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