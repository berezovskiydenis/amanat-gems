# -*- coding: UTF-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import Email, Length, EqualTo, Required
from wtforms import ValidationError
from ..models import User, Department


msg_required = u"Это поле обязательно для заполнения."
msg_max = u"Максимальное количество символов не должно превышать {}."


class UserRegistrationForm(FlaskForm):
    """User registration form."""
    email = StringField(
        label='Email',
        validators=[
            Required(message=msg_required),
            Length(max=99, message=msg_max.format(99)),
            Email(message=u"Поле должно содержать email адрес.")
        ],
        id="email"
    )
    username = StringField(
        label=u'Имя пользователя',
        validators=[
            Required(message=msg_required),
            Length(max=200, message=msg_max.format(200))
        ],
        id='username'
    )
    department = SelectField(
        label=u'Подразделение',
        validators=[Required(message=msg_required)],
        id='department'
    )
    role = SelectField(
        label=u'Роль',
        choices=[('0', 'User'), ('1', 'Moderator'), ('2', 'Admin')],
        id='role'
    )
    password = PasswordField(
        label=u'Пароль',
        validators=[
            Required(message=msg_required),
            Length(min=5, max=50, message=u"Пароль должен содержать от 5 до 50 символов."),
            EqualTo('confirm_password', message=u"Пароли должны совпадать.")
        ],
        id='password'
    )
    confirm_password = PasswordField(
        label=u"Повторить пароль",
        validators=[Required(message=msg_required)],
        id='confirm_password'
    )
    submit = SubmitField(label=u'Создать')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(message=u"Указанный email уже зарегистрирован.")


class UserEditForm(FlaskForm):
    """User editing form."""
    username = StringField(
        label=u'Имя пользователя',
        validators=[
            Required(message=msg_required),
            Length(max=200, message=msg_max.format(200))
        ],
        id='username'
    )
    department = SelectField(
        label=u'Подразделение',
        validators=[Required(message=msg_required)],
        id='department'
    )
    role = SelectField(
        label=u'Роль',
        choices=[('0', 'User'), ('1', 'Moderator'), ('2', 'Admin')],
        id='role'
    )
    active = SelectField(
        label=u'Активен',
        choices=[('0', 'Блокировать'), ('1', 'Разблокировать')],
        id='act'
    )
    submit = SubmitField(label=u'Сохранить')


class UserChangeEmailForm(FlaskForm):
    """Change Email for User."""
    email = StringField(
        label=u'Новый Email',
        validators=[
            Required(message=msg_required),
            Length(max=99, message=msg_max.format(99)),
            Email(message=u"Поле должно содержать email адрес.")
        ],
        id="email"
    )
    submit = SubmitField(label=u'Сохранить')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(message=u"Указанный email уже зарегистрирован.")


class UserChangePasswordForm(FlaskForm):
    """Change Password for User."""
    password = PasswordField(
        label=u'Новый пароль',
        validators=[
            Required(message=msg_required),
            Length(min=5, max=50, message=u"Пароль должен содержать от 5 до 50 символов."),
            EqualTo('confirm_password', message=u"Пароли должны совпадать.")
        ],
        id='password'
    )
    confirm_password = PasswordField(
        label=u"Повторить пароль",
        validators=[Required(message=msg_required)],
        id='confirm_password'
    )
    submit = SubmitField(label=u'Сохранить')


# ---------------------------------------------------------------------------- #
# ------------------------ Departments --------------------------------------- #
# ---------------------------------------------------------------------------- #

class DepartmentRegistrationForm(FlaskForm):
    """Department registration form."""
    depname = StringField(
        label=u'Подразделение',
        validators=[
            Required(message=msg_required),
            Length(max=249, message=msg_max.format(249))
        ],
        id='depname'
    )
    submit = SubmitField(label=u'Создать')

    def validate_depname(self, field):
        if Department.query.filter_by(depname=field.data).first():
            raise ValidationError(message=u"Указанное подразделение уже существует.")


class DepartmentEditForm(FlaskForm):
    """Department editing form."""
    depname = StringField(
        label=u'Подразделение',
        validators=[
            Required(message=msg_required),
            Length(max=249, message=msg_max.format(249))
        ],
        id='depname'
    )
    submit = SubmitField(label=u'Сохранить')

    def validate_depname(self, field):
        if Department.query.filter_by(depname=field.data).first():
            raise ValidationError(message=u"Указанное подразделение уже существует.")
