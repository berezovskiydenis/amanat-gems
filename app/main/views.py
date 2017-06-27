# -*- coding: UTF-8 -*-

from flask import render_template, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from . import main
from .. import db
from ..models import Draft, Proposal, Trash, Gem, Team, User
from .forms import FindGemForm


# ---------------------------------------------------------------------------- #
# --------------------------- Routs ------------------------------------------ #
# ---------------------------------------------------------------------------- #
@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    total_proposals = db.session.query(Proposal).count()
    total_participation = db.session.query(Team).filter(Team.user_id==current_user.id).count()
    total_gems = db.session.query(Gem).filter(Gem.closed_at == None).count()
    return render_template(
        'index.html',
        total_proposals=total_proposals,  # total open proposals
        total_participation=total_participation,  # gems where user is participating
        total_gems=total_gems  # total number of open gems
    )


@main.route('/find', methods=['GET', 'POST'])
@login_required
def find_gem():
    form = FindGemForm()
    if form.validate_on_submit():
        _number = form.number.data

        # Look for gem
        result = db.session.query(Gem).filter(Gem.number==_number).first()
        if result:
            return redirect(url_for('gem.a_gem', id=result.id))
        
        # Look for proposal
        result = db.session.query(Proposal).filter(Proposal.number==_number).first()
        # If found and current user is author or current user is moderator / admin
        if result and (current_user.id == result.author or current_user.role > 0 ):
            return redirect(url_for('proposal.a_proposal', id=result.id))
        
        # Look for draft for current user
        result = db.session.query(Draft).filter(Draft.number==_number).first()
        if result and current_user.id == result.author:  # if found and current user is author
            return redirect(url_for('draft.a_draft', id=result.id))
        
        # Not found
        flash(u'Номер не найден среди ваших черновиков, заявок и бриллиантов.', 'info')

    return render_template('find.html', form=form)


@main.route('/help')
@login_required
def documentation():
    return render_template('help/help.html')


@main.route('/user/<int:user_id>')
@login_required
def user(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    return render_template('user.html', user=user)
