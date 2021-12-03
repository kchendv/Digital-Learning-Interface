from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email 電子郵件', validators=[DataRequired(), Email()])
    password = PasswordField('Password 密碼', validators=[DataRequired()])
    remember = BooleanField("Remember Me 記住帳號")

    submit = SubmitField("Login 登入")
