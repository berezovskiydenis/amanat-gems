# -*- coding: UTF-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length


class LoginForm(FlaskForm):
    email = StringField(
        label='Email',
        validators=[
            Required(message=u"Это поле является обязательным."),
            Length(max=99, message=u"Количество символов не должно быть более 99."),
            Email(message=u"Поле должно сожердать email адрес.")
        ],
        id='email'
    )
    
    password = PasswordField(
        label='Password',
        validators=[Required(message=u"Это поле является обязательным.")],
        id='password'
    )
    
    remember_me = BooleanField(
        label=u"Запомнить меня"
    )

    submit = SubmitField(label=u"Войти")
