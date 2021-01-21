from flask import Flask
from flask import request
from flask import render_template


app = Flask(__name__)


@app.route("/")
def hello():
    '''Главная страница с описанием сервиса'''
    return render_template("index.html")


@app.route("/form")
def form():
    '''Страница с формой запроса'''
    return render_template("form.html")


@app.route("/contacts")
def contacts():
    '''Страница с контактами'''
    return render_template("contacts.html")


# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         do_not_login
#     else:
#         show_the_login_form()


# #@app.route("/hello/")
# @app.route("/hello/<name>")
# def hello(name=None):
#     return render_template(
#         "hello.html",
#         name=name
#     )



# @app.route('/upload', method=['GET' 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         f = request.files['the_file']
#         f.save('./uploaded_file.txt')
#

# def login():
#     error = None
#     if request.method == 'POST':
#         if valid_login(request.form['username'],
#             request.form['password']):
#             return log_the_user_in(
#                 request.form['username'])
#         else:
#             error = 'Invalid username/password'
#


# @app.route("/status")
# def status():
#     return "Сделано на flask"


# @app.route('/user/<username>')# <>переменная часть
# def show_user_profile(username):
#     return 'User ' + username
#
# @app.route('/post/<int:post_id>') #п равило <converter:variable_name>
# def show_post(post_id):
#     return 'Post ' + post_id


if __name__ == '__main__':
    app.run()



