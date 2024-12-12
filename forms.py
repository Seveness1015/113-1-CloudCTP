from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class DiaryEntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    mood = StringField('Mood')  # Emoji
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Add Entry')

class RegisterForm(FlaskForm):
    username = StringField('使用者名稱', validators=[DataRequired()])
    password = PasswordField('密碼', validators=[DataRequired()])
    confirm_password = PasswordField('確認密碼', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('註冊')