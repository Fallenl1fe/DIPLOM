from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for,abort,g,flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'iuhiuh'
from models import db
import models
from common import get_tests_for_user, dostup_k_test

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(models.Users).filter(models.Users.id == user_id).first()


@app.errorhandler(404)
def page_not_found():
    return render_template('404page.html'), 404


#@app.errorhandler(401)
#def page_not_dostupa():
#    return redirect('login')


@app.route("/")
def index():
    posts = db.session.query(models.Posts).all()
    return render_template("index.html", title="Главная", posts=posts ,zaloginen=current_user.is_authenticated)


@app.route("/post/<id>")
@login_required
def showPost(id):
    name, post = db.session.query(models.Posts.name, models.Posts.text).filter(id == models.Posts.id).first()
    if not name:
        abort(404)

    return render_template('post.html',  zagolovok=name, text=post,zaloginen=current_user.is_authenticated)


@app.route("/add_post", methods=("POST", "GET"))
def add_post():
    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['postes']) > 10:
            if current_user.role == True:
                try:
                    p = models.Posts(name=request.form['name'], text=request.form['postes'], user_id=current_user.id)
                    db.session.add(p)
                    db.session.flush()

                    db.session.commit()
                except:
                    db.session.rollback()
                    print("Ошибка добавления в БД")
                flash("Пост создан", category='success')
                return redirect(url_for('add_post'))
            flash("У вас нет прав", category='error')
        else:
            flash('Ошибка добавления статьи', category='error')
    return render_template("add_post.html", title="Регистрация",zaloginen=current_user.is_authenticated)


@app.route("/register", methods=("POST", "GET"))
def register():
    if request.method == "POST":
        if len(request.form['name']) > 1 and len(request.form['psw']) > 5:
            try:
                hash = generate_password_hash(request.form['psw'])
                u = models.Users(email=request.form['email'], psw=hash, name=request.form['name'],
                          surname=request.form['surname'], login=request.form['login'])
                db.session.add(u)
                db.session.flush()

                db.session.commit()
            except:
                db.session.rollback()
                print("Ошибка добавления в БД")
            flash("Готово!", category='success')
            return redirect(url_for('register'))
        else:
            flash('Ошибка регистрации', category='error')
    return render_template("register.html", title="Регистрация",zaloginen=current_user.is_authenticated)


@app.route('/profile')
def profile():
    return render_template("profile.html", title="Профиль",zaloginen=current_user.is_authenticated)


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    if request.method == "POST":
        user = db.session.query(models.Users).filter(models.Users.email == request.form['email']).first()
        if user and check_password_hash(user.psw, request.form['psw']):
            rm = True if request.form.get('remainme') else False
            login_user(user, remember=rm)
            return redirect(request.args.get("next") or url_for("profile"))

        flash("Неверная пара логин/пароль", "error")

    return render_template("login.html", title="Авторизация",zaloginen=current_user.is_authenticated)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


@app.route('/test_list')
@login_required
def test_list():
    tests_user = get_tests_for_user(current_user.id, db.session)
    #print(tests_user)
    return render_template("test_list.html", massiv_testov=tests_user, zaloginen=current_user.is_authenticated)


@app.route("/test/<test_id>/testing")
@login_required
def testing(test_id):
    if not dostup_k_test(current_user.id, test_id, db.session):
        abort(403)

    return render_template('testing.html', zaloginen=current_user.is_authenticated)





if __name__ == "__main__":
    app.run(debug=True)

#проверка коммита
#123