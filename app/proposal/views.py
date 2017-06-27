# -*- coding: UTF-8 -*-

from datetime import datetime
from flask import render_template, redirect, url_for, abort, flash, current_app
from flask_login import login_required, current_user
from sqlalchemy import desc, and_
from sqlalchemy.exc import IntegrityError
from . import proposal
from .. import db
from ..models import Proposal, Gem, Trash
from .forms import ProposalEditForm, ProposalDenyForm

# ---------------------------------------------------------------------------- #
# ---------------------- Helper function ------------------------------------- #
# ---------------------------------------------------------------------------- #
def show_proposals_all(page):
    """Return all proposals."""
    _proposals = db.session.query(Proposal).filter(

    ).order_by(
        desc(Proposal.id)
    ).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False
    )
    return _proposals

def show_proposals_my_open(page):
    """Return my proposals."""
    _proposals = db.session.query(Proposal).filter(
        Proposal.author==current_user.id
    ).order_by(
        desc(Proposal.id)
    ).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False
    )
    return _proposals

def show_proposals_my_closed(page):
    """Return closed proposals."""
    _proposals = db.session.query(Trash).filter(
        Trash.author==current_user.id
    ).order_by(
        desc(Trash.id)
    ).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False
    )
    return _proposals


# ---------------------------------------------------------------------------- #
# ------------------ Routes -------------------------------------------------- #
# ---------------------------------------------------------------------------- #
@proposal.route('/proposals/my/open/<int:page>', methods=['GET', 'POST'])
@login_required
def proposals_my_open(page=1):
    """Show my open proposals."""
    _proposals = show_proposals_my_open(page)
    return render_template('proposal/proposals_my.html', prpls=_proposals)


@proposal.route('/proposals/my/closed/<int:page>', methods=['GET', 'POST'])
@login_required
def proposals_my_closed(page=1):
    """Show my closed proposals."""
    _proposals = show_proposals_my_closed(page)
    return render_template('proposal/proposals_my_closed.html', prpls=_proposals)


@proposal.route('/proposals/all/<int:page>', methods=['GET', 'POST'])
@login_required
def proposals_all(page=1):
    """Show all proposals."""
    _proposals = show_proposals_all(page)
    return render_template('proposal/proposals_all.html', prpls=_proposals)


@proposal.route('/proposals/<int:id>')
@login_required
def a_proposal(id):
    """Show only one proposal with id."""
    _prpl = Proposal.query.get_or_404(id)
    return render_template('proposal/proposal.html', prpl=_prpl)


@proposal.route('/proposals/closed/<int:id>')
@login_required
def a_proposal_closed(id):
    """Show only one closed proposal with id."""
    _prpl = Trash.query.get_or_404(id)
    return render_template('proposal/proposal_closed.html', prpl=_prpl)


@proposal.route('/proposals/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def proposals_edit(id):
    """Edit proposal with id."""
    _proposal = Proposal.query.get_or_404(id)
    form = ProposalEditForm(obj=_proposal)
    if form.validate_on_submit():
        _proposal.name = form.name.data
        _proposal.cause = form.cause.data
        _proposal.description = form.description.data
        _proposal.plan = form.plan.data

        db.session.add(_proposal)
        try:
            db.session.commit()
            flash(u"Заявка на бриллиант изменена.", 'success')
        except IntegrityError as int_error:
            db.session.rollback()
            flash(u"Ошибка изменения заявки на бриллиант.", 'danger')
        return redirect(url_for('proposal.proposals_my_open', page=1))
    return render_template('proposal/proposals_edit.html', form=form)


@proposal.route('/proposals/<int:id>/accept', methods=['GET', 'POST'])
@login_required
def proposals_accept(id):
    """Accept proposal - make it a Gem."""
    if current_user.role == 0:
        abort(403)
    _proposal = Proposal.query.get_or_404(id)
    new_gem = Gem(
        created=datetime.utcnow(),
        author=_proposal.author,
        name =_proposal.name,
        cause=_proposal.cause,
        description=_proposal.description,
        plan=_proposal.plan,
        number=_proposal.number
    )
    db.session.add(new_gem)
    db.session.delete(_proposal)
    try:
        db.session.commit()
        flash(u"Заявка на бриллиант одобрена!", 'success')
    except IntegrityError:
        db.session.rollback()
        flash(u"Ошибка одобрения заявки на бриллиант.", 'danger')
    return redirect(url_for('proposal.proposals_all', page=1))


@proposal.route('/proposals/<int:id>/deny', methods=['GET', 'POST'])
@login_required
def proposals_deny(id):
    """Deny proposal."""
    _proposal = Proposal.query.get_or_404(id)
    form = ProposalDenyForm()
    if form.validate_on_submit():
        user_signature = "\n\n __(" + str(current_user.username) + ")__"
        _trash = Trash(
            created=datetime.utcnow(),
            author=_proposal.author,
            name =_proposal.name,
            cause=_proposal.cause,
            description=_proposal.description,
            plan=_proposal.plan,
            number=_proposal.number,
            trash_reason=form.reason.data+user_signature
        )
        db.session.add(_trash)
        db.session.delete(_proposal)
        try:
            db.session.commit()
            flash(u"В заявке на бриллиант отказано.", 'success')
        except IntegrityError:
            db.session.rollback()
            flash(u"Ошибка в отказе заявке на бриллиант.", 'danger')
        if current_user.role > 0:
            return redirect(url_for('proposal.proposals_all', page=1))
        return redirect(url_for('proposal.proposals_my_open', page=1))
    return render_template('proposal/proposals_deny.html', form=form, prpl=_proposal)


@proposal.route('/proposals/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def proposals_delete(id):
    """Delete proposal."""
    _proposal = Proposal.query.get_or_404(id)
    try:
        db.session.delete(_proposal)
        db.session.commit()
        flash(u"Заявка на бриллиант удалена.", 'success')
    except IntegrityError:
        db.session.rollback()
        flash(u"Ошибка удаления заявки на бриллиант.", 'danger')
    return redirect(url_for('proposal.proposals_my_open', page=1))


@proposal.route('/proposals/<int:id>/delete_from_trash', methods=['GET', 'POST'])
@login_required
def proposals_crean_trash(id):
    """Delete denied proposal from trash."""
    _trash = Trash.query.get_or_404(id)
    try:
        db.session.delete(_trash)
        db.session.commit()
        flash(u"Отказанная заявка на бриллиант удалена.", 'success')
    except IntegrityError:
        db.session.rollback()
        flash(u"Ошибка удаления отказанной заявки на бриллиант.", 'danger')
    return redirect(url_for('proposal.proposals_my_closed', page=1))
