from bmc import bmc_app
from bmc.library import Library
from bmc.forms import LoginForm
from werkzeug.utils import secure_filename
from flask import render_template
from flask import request, flash, redirect, url_for

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@bmc_app.route('/hello', methods = ['POST', 'GET'])
def index():
    name = request.args.get('name', 'Nobody')

    if (request.method == 'POST'):
        name = request.form['name']
        greet = request.form['greet']
        greeting = f'{greet}, {name}'
        return render_template("index.html", greeting = greeting)
    else:
        return render_template("hello_form.html")

def good_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bmc_app.route('/file', methods = ['POST', 'GET'])
def potato():
    if (request.method == 'POST'):
        file = request.files['file']
        name = request.form['name']
        
        filename = secure_filename(name)

        if file and good_file(file.filename):
            file.save("images/" + filename + ".png")
            return render_template("uploaded.html")
    else:
        return render_template("file_upload.html")

@bmc_app.route('/bmc_start')
def enter():
    return render_template("bmc_books.html")

@bmc_app.route('/bmc_trial')
def memory():
    global book
    global library
    library = Library()
    try:
        book = request.args.get("book")
        return render_template('bmc_form.html', length = len(library.get(book)))
    except TypeError:
        return render_template('error.html')

@bmc_app.route('/bmc_final', methods = ['GET', 'POST'])
def result():
    if (request.method == 'POST'):
        correct = 0
        try:
            for x in range(0, len(library.get(book))):
                input = request.form[f"{x}"]
                if (input.lower() == library.get(book)[x].lower()):
                    correct += 1
            return render_template('bmc_result.html', result=correct)
        except TypeError:
            return render_template('error.html')
    else:
        return render_template('error.html')

@bmc_app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if (form.validate_on_submit()):
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('potato'))
    return render_template('login.html', form = form)
