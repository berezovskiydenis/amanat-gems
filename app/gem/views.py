# -*- coding: UTF-8 -*-

from datetime import datetime
from flask import render_template, redirect, abort, url_for, flash, current_app, request
from flask_login import login_required, current_user
from sqlalchemy import or_, and_, desc
from sqlalchemy.exc import IntegrityError
from . import gem
from .. import db
from ..models import User, Department, Gem, Comment, Team
from .forms import GemEditForm, CommentAddForm, EditTeamForm



# ---------------------------------------------------------------------------- #
# ------------------------------ Gems ---------------------------------------- #
# ---------------------------------------------------------------------------- #

@gem.route('/gems/all', methods=['GET', 'POST'])
@gem.route('/gems/all/<int:page>', methods=['GET', 'POST'])
@login_required
def gems(page=1):
    """Show all the gems."""    
    gems = db.session.query(Gem).filter().order_by(
        desc(Gem.created)
    ).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False
    )
    return render_template('gem/gems.html', gems=gems)


@gem.route('/gems/my')
@gem.route('/gems/my/<int:page>', methods=['GET', 'POST'])
@login_required
def gems_my(page=1):
    """Show gems of current user."""
    gems = db.session.query(Gem).filter(
        Gem.author==current_user.id
    ).order_by(desc(Gem.created)).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False
    )
    return render_template('gem/gems_my.html', gems=gems)


@gem.route('/gems/<int:id>', methods=['GET', 'POST'])
@login_required
def a_gem(id):
    """Show the Gem with id and all the corresponding data."""
    _gem = Gem.query.get_or_404(id)
    _comments = db.session.query(Comment).filter(Comment.gem_id==_gem.id).order_by(desc(Comment.created))
    _team = db.session.query(Team).filter(Team.gem_id==id).order_by(Team.user_id)
    _team_ids = [x.user_id for x in _team]
    form = CommentAddForm()
    if form.validate_on_submit():
        new_comment = Comment(
            created=datetime.utcnow(),
            comment=form.comment.data,
            author=current_user.id,
            gem_id=_gem.id
        )
        db.session.add(new_comment)
        try:
            db.session.commit()
            flash(u"Новый комментарий добавлен!", 'success')
        except IntegrityError:
            db.session.rollback()
            flash(u"Ошибка добавления комментария.", 'danger')
        return redirect(url_for('gem.a_gem', id=_gem.id))
    return render_template('gem/gem.html', gem=_gem, comments=_comments, form=form, team=_team, team_ids=_team_ids)


@gem.route('/gems/<int:gem_id>/edit', methods=['GET', 'POST'])
@login_required
def gems_edit(gem_id):
    """Edit the gem with id."""
    gem = Gem.query.get_or_404(gem_id)
    form = GemEditForm(obj=gem)
    if form.validate_on_submit():
        gem.name = form.name.data
        gem.cause = form.cause.data
        gem.description = form.description.data
        gem.plan = form.plan.data
        db.session.add(gem)
        try:
            db.session.commit()
            flash(u"Информация о бриллианте успешно изменена!", 'success')
        except IntegrityError:
            db.session.rollback() 
            flash(u"Ошибка изменения информации о бриллианте.", 'danger')
        return redirect(url_for('gem.gems'))
    return render_template('gem/gem_edit.html', form=form, _gem=gem)


@gem.route('/gems/<int:id>/close', methods=['GET', 'POST'])
@login_required
def gems_close(id):
    """Close the Gem with id as completed successfully."""
    if current_user.role == 0:
        abort(403)
    gem = Gem.query.get_or_404(id)
    gem.closed_at = datetime.utcnow()
    db.session.add(gem)
    try:
        db.session.commit()
        flash(u"Биллиант успешно завершен!", 'success')
    except IntegrityError:
        db.session.rollback()
        flash(u"Ошибка завершения бриллианта.", 'danger')
    return redirect(url_for('gem.gems'))


@gem.route('/gems/<int:gemid>/team', methods=['GET', 'POST'])
@login_required
def edit_team(gemid):
    """Add a new team member to the Gem with id."""
    _gem = Gem.query.get_or_404(gemid)

    _users = db.session.query(User).filter(User.active==1).order_by(User.username)
    users_lst = [(str(user.id), str(user.username)) for user in _users]

    form = EditTeamForm()
    form.member.choices = users_lst
    if form.validate_on_submit():
        for k in form.member.data:
            team_member = Team(
                gem_id=gemid,
                user_id=int(k)
            )
            db.session.add(team_member)
        try:
            db.session.commit()
            flash(u"Новые члены команды добавлены.", 'success')
        except IntegrityError:
            db.session.rollback()
            flash(u"Ошибка добавления членов команды.", 'danger')
        return redirect(url_for('gem.a_gem', id=gemid))
    return render_template('gem/team_edit.html', form=form)


@gem.route('/gems/<int:gemid>/team/<int:member_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_team_member(gemid, member_id):
    """Deletion the User member_id from Gem team."""
    _team = db.session.query(Team).filter(Team.gem_id==gemid, Team.user_id==member_id).first()
    if _team:
        try:
            db.session.delete(_team)
            db.session.commit()
            flash(u"Член команды исключен.", 'success')
        except IntegrityError:
            db.session.rollback()
            flash(u"Ошибка исключения члена команды.", 'danger')
    return redirect(url_for('gem.a_gem', id=gemid))


@gem.route('/gems/participation', methods=['GET', 'POST'])
@login_required
def gems_participation():
    """Show gems where user participates."""
    _participation = db.session.query(Team).filter(Team.user_id==current_user.id).group_by(Team.gem_id).all()
    gems = []
    if _participation:
        gem_ids = [x.gem_id for x in _participation]
        gems = db.session.query(Gem).filter(
            Gem.id.in_(gem_ids)
        ).order_by(
            desc(Gem.created)
        ).all()
    return render_template('gem/gems_participation.html', gems=gems)
