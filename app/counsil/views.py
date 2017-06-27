# -*- coding: UTF-8 -*-

from flask import render_template
from flask_login import login_required
from . import counsil
from .. import db
from ..models import User


@counsil.route('/counsil')
@login_required
def counsil():
    """Return users who's role is counsil (role == 1)."""
    members = db.session.query(User).filter(User.role==1).order_by(User.username)
    return render_template('counsil/counsil.html', members=members)
