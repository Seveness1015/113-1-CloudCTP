from flask import Flask, render_template, redirect, url_for, request, jsonify, session, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, User, DiaryEntry
from forms import LoginForm, DiaryEntryForm, RegisterForm
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)

@app.before_request
def require_login():
    allowed_routes = ['login', 'instructions', 'register']
    if 'username' not in session and request.endpoint not in allowed_routes:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('註冊成功，請登入！')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:  # 比對密碼
            session['username'] = user.username
            return redirect(url_for('index'))
        flash('帳號或密碼錯誤')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    entries = DiaryEntry.query.all()
    return render_template('index.html', entries=entries)

@app.route('/new', methods=['GET', 'POST'])
def new_entry():
    form = DiaryEntryForm()
    if form.validate_on_submit():
        entry = DiaryEntry(
            title=form.title.data,
            mood=form.mood.data,
            content=form.content.data[:300],
            date_created=datetime.datetime.now()
        )
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_entry.html', form=form)

@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    entry = DiaryEntry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    flash('日記已刪除')
    return redirect(url_for('index'))

@app.route('/instructions')
def instructions():
    return jsonify({
        "使用說明": [
            "請先進行登入再使用本日記系統～",
            "1. 首頁可查看所有日記，點擊可返回",
            "2. 點選新增日記即可記錄新內容",
            "3. 此按鈕為操作題式按鈕✨",
            "4. 登出按鈕位於右上角，點擊後即可登出帳號",
            "若仍有疑慮請聯繫信箱: youguesswhat@gmail.com，謝謝"
        ]
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
