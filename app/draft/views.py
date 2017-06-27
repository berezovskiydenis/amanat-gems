# -*- coding: UTF-8 -*-

from datetime import datetime
from flask import render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from sqlalchemy import or_, and_, desc
from sqlalchemy.exc import IntegrityError
from . import draft
from .. import db
from ..models import Draft, Proposal
from .forms import DraftRegistrationForm, DraftEditForm


# ---------------------------------------------------------------------------- #
# ---------------------- Helper functions ------------------------------------ #
# ---------------------------------------------------------------------------- #

def show_drafts(page):
    """Return drafts for current user."""
    _drft = db.session.query(Draft).filter(
        Draft.author==current_user.id
    ).order_by(
        desc(Draft.id)
    ).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False
    )
    return _drft

# ---------------------------------------------------------------------------- #
# ------------------------- Drafts ------------------------------------------- #
# ---------------------------------------------------------------------------- #

@draft.route('/drafts/all', methods=['GET', 'POST'])
@draft.route('/drafts/all/<int:page>', methods=['GET', 'POST'])
@login_required
def drafts(page=1):
    """Show all drafts for current user."""
    _drafts = show_drafts(page)
    return render_template('draft/drafts.html', drafts=_drafts)


@draft.route('/drafts/<int:id>', methods=['GET', 'POST'])
@login_required
def a_draft(id):
    """Show a draft with id."""
    _draft = Draft.query.get_or_404(id)
    return render_template('draft/draft.html', draft=_draft)


@draft.route("/drafts/add", methods=['GET', 'POST'])
@login_required
def drafts_add():
    """Create a new draft."""
    form = DraftRegistrationForm()
    if form.validate_on_submit():
        _draft = Draft(
            created=datetime.utcnow(),
            author=current_user.id,
            name=form.name.data,
            cause=form.cause.data,
            description=form.description.data,
            plan=form.plan.data,
            number=Draft._generate_number()
        )
        db.session.add(_draft)
        try:
            db.session.commit()
            flash(u"Новый черновик создан!", 'success')
        except IntegrityError:
            db.session.rollback()
            flash(u"Ошибка: черновик не создан!", 'danger')
        return redirect(url_for('draft.drafts'))
    return render_template('draft/drafts_add.html', form=form)


@draft.route("/drafts/<int:id>/delete")
@login_required
def drafts_delete(id):
    """Delete draft."""
    _draft = Draft.query.get_or_404(id)
    db.session.delete(_draft)
    try:
        db.session.commit()
        flash(u"Черновик удален!", 'success')
    except IntegrityError:
        db.session.rollback()
        flash(u"Ошибка: черновик не удален!", 'danger')
    return redirect(url_for('draft.drafts'))
    

@draft.route("/drafts/<int:id>/edit", methods=['GET', 'POST'])
@login_required
def drafts_edit(id):
    """Edit a draft with id."""
    _draft = Draft.query.get_or_404(id)
    form = DraftEditForm(obj=_draft)
    if form.validate_on_submit():
        _draft.name = form.name.data
        _draft.cause = form.cause.data
        _draft.description = form.description.data
        _draft.plan = form.plan.data
        db.session.add(_draft)
        try:
            db.session.commit()
            flash(u"Черновик изменен!", 'success')
        except IntegrityError:
            db.session.rollback()
            flash(u"Ошибка: черновик не изменен!", 'danger')
        return redirect(url_for('draft.drafts'))
    return render_template('draft/drafts_edit.html', form=form)


@draft.route("/drafts/<int:id>/make_proposal")
@login_required
def drafts_make_proposal(id):
    """Make a proposal from draft."""
    _draft = Draft.query.get_or_404(id)
    new_proposal = Proposal(
        author=_draft.author,
        name=_draft.name,
        cause=_draft.cause,
        description=_draft.description,
        plan=_draft.plan,
        number=_draft.number
    )
    db.session.add(new_proposal)  # create new proposal
    db.session.delete(_draft)  # delete a draft
    try:
        db.session.commit()
        flash(u"Вы успешно подали заявку на бриллиант. Ожидайте одобрения заявки.", 'success')
    except IntegrityError:
        db.session.rollback()
        flash(u"Ошибка подачи заявки на бриллиант!", 'danger')
    return redirect(url_for('draft.drafts'))
