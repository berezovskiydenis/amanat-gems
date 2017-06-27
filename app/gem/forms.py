# -*- coding: UTF-8 -*-

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectMultipleField
from wtforms.validators import Length, Required


msg_required = u"Это поле обязательно для заполнения."
msg_max = u"Количество символов не должно превышать {}."


class GemEditForm(FlaskForm):
    name = TextAreaField(
        label=u'Название',
        validators=[
            Required(message=msg_required),
            Length(max=299, message=msg_max.format(299))
        ],
        id='name'
    )

    cause = TextAreaField(
        label=u'Причина',
        validators=[
            Required(message=msg_required),
            Length(max=999, message=msg_max.format(999))
        ],
        id='cause'
    )

    description = TextAreaField(
        label=u'Описание',
        validators=[
            Required(message=msg_required),
            Length(max=2999, message=msg_max.format(2999))
        ],
        id='description'
    )

    plan = TextAreaField(
        label=u'План',
        validators=[
            Required(message=msg_required),
            Length(max=2999, message=msg_max.format(2999))
        ],
        id='plan'
    )

    submit = SubmitField(label=u'Сохранить')


class CommentAddForm(FlaskForm):
    comment = TextAreaField(
        label=u'Комментарий',
        validators=[
            Required(message=msg_required),
            Length(max=499, message=msg_max.format(499))
        ],
        id='comment'
    )
    submit = SubmitField(label=u'Добавить комментарий')


class EditTeamForm(FlaskForm):
    member = SelectMultipleField(label=u'Выбирите члена группы')
    submit = SubmitField(label=u'Сохранить')
