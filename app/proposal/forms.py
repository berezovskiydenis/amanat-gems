# -*- coding: UTF-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Length, Required


msg_required = u"Это поле является обязательным."
msg_max = u"Количество символов не должно превышать {}."


class ProposalEditForm(FlaskForm):
    """Edit draft form."""
    name = TextAreaField(
        label=u'Название',
        validators=[
            Required(message=msg_required),
            Length(max=299, message=msg_max.format(299))
        ],
        id="draft_name"
    )
    cause = TextAreaField(
        label=u'Причина',
        validators=[
            Required(message=msg_required),
            Length(max=999, message=msg_max.format(999))
        ],
        id="draft_cause"
    )
    description = TextAreaField(
        label=u'Описание ситуации',
        validators=[
            Required(message=msg_required),
            Length(max=2999, message=msg_max.format(2999))
        ],
        id="description"
    )
    plan = TextAreaField(
        label=u'План действий',
        validators=[Length(max=2999, message=msg_max.format(2999))],
        id="plan"
    )
    submit = SubmitField('Сохранить изменения')


class ProposalDenyForm(FlaskForm):
    """Deny proposal form."""
    reason = TextAreaField(
        label=u'Причина отказа',
        validators=[
            Required(message=msg_required),
            Length(max=299, message=msg_max.format(299))
        ],
        id="reason"
    )
    submit = SubmitField('Отказать')
