import json
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)
bootstrap = Bootstrap(app)


with open('users.json', 'r') as file:
    users = json.load(file)

with open('sms.json', 'r') as file:
    sms = json.load(file)["sms"]


logn = ''


@app.route("/")
@app.route("/index")
@app.route("/feed")
def index():
    return render_template("index.html", h1="Новости")


@app.route("/unlogin")
def unlogin():
    global logn
    if logn == '':
        return redirect(url_for('index'))
    else:
        logn = ''
        return redirect(url_for('login'))


@app.route("/books")
def books():
    if logn == '':
        return redirect(url_for('login'))
    return render_template("books.html", h1="Книги")


@app.route("/chat", methods=['GET', 'POST'])
def chat():
    if logn == '':
        return redirect(url_for('login'))
    if request.method == 'POST':
        now = datetime.now()
        sms.insert(0, {'header': logn, 'body': request.form['say'], 'date': str(now)[:]})
        with open('sms.json', 'w') as file:
            json.dump({"sms": sms}, file, indent=2)
    return render_template("chat.html", h1="Чат", sms=sms)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global logn
    if logn != '':
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user in users:
            if username == user:
                if users[username] == password:
                    logn = username
                    return redirect(url_for('index'))
                else:
                    return render_template('login.html', h1='Введён неверный пароль')
        return render_template('login.html', h1='Пользователя с таким логином не существует')
    else:
        return render_template('login.html')


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    global logn
    if logn != '':
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        for user in users:
            if username == user:
                return render_template('reg.html', h1='Пользователь с таким логином уже существует')
        if password1 == password2:
            users[username] = password1
            with open('users.json', 'w') as file:
                json.dump(users, file, ensure_ascii=False,
                          indent=2, sort_keys=True)
            logn = username
            return redirect(url_for('index'))
        else:
            return render_template('reg.html', h1='Введённые пароли не совпадают')
    else:
        return render_template('reg.html')


if __name__ == "__main__":
    app.run(debug=True)
