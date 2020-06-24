from flask import Flask, render_template

app = Flask(__name__, template_folder= '/Users/hansoochang/SumoPY')

@app.route('/')
def index():
    greeting = None
    return render_template("index.html", greeting=greeting)

if __name__ == "__main__":
    app.run()
