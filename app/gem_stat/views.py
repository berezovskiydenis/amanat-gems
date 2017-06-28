# -*- coding: UTF-8 -*-

from flask import render_template, abort
from flask_login import login_required
from sqlalchemy import func, desc, join, asc
from .import gem_stat
from .. import db
from ..models import Gem, User


# ---------------------------------------------------------------------------- #
# ------------------------ Helper functions ---------------------------------- #
# ---------------------------------------------------------------------------- #
def query_all_gems():
    result = db.session.query(
        Gem.author,  # author id
        User.username,  # author name
        func.count(Gem.author).label('cnt')  # count authors
        ).group_by(
            Gem.author,
            User.username
        ).order_by(
            desc('cnt'),  # order from more gems to less gems
            asc(User.username)
        )
    result = result.join(User)[:15]  # limit 15 rows
    return result

def query_closed_gems():
    result = db.session.query(
            Gem.author,  # author
            User.username,
            func.count(Gem.author).label('cnt')  # count authors
        ).filter(
            Gem.closed_at != None
        ).group_by(
            Gem.author,
            User.username
        ).order_by(
            desc('cnt'),  # order from more gems to less gems
            asc(User.username)
        )
    result = result.join(User)[:15]  # limit 15 rows
    return result


# ---------------------------------------------------------------------------- #
# ------------------------ Routs --------------------------------------------- #
# ---------------------------------------------------------------------------- #
@gem_stat.route('/statistics', methods=['GET', 'POST'])
@login_required
def show_stat_all():
    """Show statistics."""
    return render_template('gem_stat/stat.html', all_gems=query_all_gems(), closed_gems=query_closed_gems())
