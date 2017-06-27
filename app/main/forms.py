# -*- coding: UTF-8 -*-

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import Length, Required


class FindGemForm(FlaskForm):
    """Find draft, proposal or gem by number."""
    number = StringField(
        label=u'Номер',
        validators=[
            Required(message=u"Это поле обязательно для заполнения."),
            Length(max=10, message="Номер не можен превышать 10 символов.")
        ],
        id='number'
    )
    submit = SubmitField(label=u'Найти')
