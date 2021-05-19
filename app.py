from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for,abort,g,flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret-key-goes-here'

from models import Posts, Users, db


@app.route("/")
def index():
    return render_template("index.html", title="Главная")


@app.route('/profile')
def profile():
    return render_template("profile.html", title="Профиль")

@app.route('/logout')
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))

# @app.route("/post/<alias>")
# #@login_required
# def showPost(alias):
#     title, post = db.getPost(alias)
#     if not title:
#         abort(404)
#
#     return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)


@app.route("/add_post", methods=("POST", "GET"))
def add_post():
    if request.method == "POST":
        try:
            p = Posts(name=request.form['name'], text=request.form['postes'])
            db.session.add(p)
            db.session.flush()

            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")

        return redirect(url_for('index'))

    return render_template("add_post.html", title="Регистрация")


@app.route("/register", methods=("POST", "GET"))
def register():
    if request.method == "POST":
        # здесь должна быть проверка корректности введенных данных
        try:
            hash = generate_password_hash(request.form['psw'])
            u = Users(email=request.form['email'], psw=hash, name=request.form['name'],surname=request.form['surname'],login=request.form['login'])
            db.session.add(u)
            db.session.flush()

            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")

        return redirect(url_for('register.html'))

    return render_template("register.html", title="Регистрация")


if __name__ == "__main__":
    app.run(debug=True)
