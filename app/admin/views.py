# -*- coding: UTF-8 -*-

from datetime import datetime
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_required, current_user
from sqlalchemy import desc, asc
from sqlalchemy.exc import IntegrityError
from . import admin
from .. import db
from ..models import User, Department
from .forms import UserRegistrationForm, UserEditForm, UserChangeEmailForm, UserChangePasswordForm
from .forms import DepartmentRegistrationForm, DepartmentEditForm
    

# ---------------------------------------------------------------------------- #
# -- Helper functions ----------------------------------------------------------
# ---------------------------------------------------------------------------- #
def dep_iterator():
    """Iterate over Departments and construct list of tuples."""
    deps = Department.query.all()
    l = []
    for dep in deps:
        l.append((str(dep.id), str(dep.depname)))
    return l


# ---------------------------------------------------------------------------- #
# ------------------------- Departments -------------------------------------- #
# ---------------------------------------------------------------------------- #
@admin.route('/admin/deps')
@login_required
def deps():
    """Show all departments."""
    deps = Department.query.all()
    return render_template('admin/deps.html', deps=deps)


@admin.route('/admin/deps/add', methods=['GET', 'POST'])
@login_required
def deps_add():
    """Add new department."""
    form = DepartmentRegistrationForm()
    if form.validate_on_submit():
        dep = Department(depname=form.depname.data)
        db.session.add(dep)
        try:
            db.session.commit()
            flash(u"Новое подразделение добавлено!", 'success')
        except IntegrityError:
            db.session.rollback()
            flash(u"Ошибка: обратитесь к администратору.", 'danger')
        return redirect(url_for('admin.deps'))
    return render_template('admin/deps_add.html', form=form)


@admin.route('/admin/deps/<int:id>/edit', methods=['POST', 'GET'])
@login_required
def deps_edit(id):
    """Edit existing department by id."""
    dep = Department.query.get(id)
    form = DepartmentEditForm(obj=dep)
    if form.validate_on_submit():
        dep.depname = form.depname.data
        db.session.add(dep)
        try:
            db.session.commit()
            flash(u"Информация о подразделении изменена!", 'success')
        except IntegrityError:
            db.session.rollback()
            flash(u"Ошибка: не удалось обновить информацию о подразделении. Обратитесь к администратору.", 'danger')
        return redirect(url_for('admin.deps'))
    return render_template('admin/deps_edit.html', form=form)


# ---------------------------------------------------------------------------- #
# ------------------------- Users -------------------------------------------- #
# ---------------------------------------------------------------------------- #
@admin.route('/admin/users')
@login_required
def users():
    """Show all users."""
    users = db.session.query(User).order_by(asc(User.username))
    # users = User.query.all().oreder_by()
    return render_template('admin/users.html', users=users)


@admin.route('/admin/users/add', methods=['POST', 'GET'])
@login_required
def users_add():
    """Register a new user."""
    if current_user.role == 0:
        abort(403)
    form = UserRegistrationForm()
    form.department.choices = dep_iterator()
    if form.validate_on_submit():
        user = User(
            created = datetime.utcnow(),
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=1,
            dep_id=form.department.data,
            role=form.role.data
        )
        db.session.add(user)
        try:
            db.session.commit()
            flash(u"Новый пользователь создан!", 'success')
        except IntegrityError:
            db.session.rollback()
            flash(u"Ошибка: обратитесь к администратору!", 'danger')
        return redirect(url_for('admin.users'))
    return render_template('admin/users_add.html', form=form)


@admin.route('/admin/users/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def users_edit(id):
    """Edit existing user by id.
    
    Fields to be edited are: username, active, department, role.
    """
    if current_user.role == 0:
        abort(403)
    _user = User.query.get(id)
    form = UserEditForm(obj=_user)
    form.department.choices = dep_iterator()
    if form.validate_on_submit():
        _user.username = form.username.data
        _user.active = form.active.data
        _user.dep_id = form.department.data
        _user.role = form.role.data
        db.session.add(_user)
        try:
            db.session.commit()
            flash(u"Информация о пользователе изменена!", 'success')
        except IntegrityError:
            db.session.rollback()
            flash(u"Ошибка: обновить информацию о пользователе не удалось!", 'danger')
        return redirect(url_for('admin.users'))
    return render_template('admin/users_edit.html', form=form)


@admin.route('/admin/users/<int:id>/changeemail', methods=['GET', 'POST'])
@login_required
def users_change_email(id):
    """Edit email for user with id."""
    if current_user.role == 0:
        abort(403)
    _user = User.query.get(id)
    form = UserChangeEmailForm(obj=_user)
    if form.validate_on_submit():
        _user.email = form.email.data
        db.session.add(_user)
        try:
            db.session.commit()
            flash(u"Email пользователя изменен!", 'success')
        except IntegrityError:
            db.session.rollback()
            flash(u"Ошибка: обновить информацию о пользователе не удалось!", 'danger')
        return redirect(url_for('admin.users'))
    return render_template('admin/users_change_email.html', form=form)


@admin.route('/admin/users/<int:id>/changepassword', methods=['GET', 'POST'])
@login_required
def users_change_password(id):
    """Edit password for user by id."""
    if current_user.role == 0:
        abort(403)
    _user = User.query.get_or_404(id)
    form = UserChangePasswordForm(obj=_user)
    if form.validate_on_submit():
        _user.password = form.password.data
        db.session.add(_user)
        try:
            db.session.commit()
            flash(u"Пароль пользователя изменен!", 'success')
        except IntegrityError:
            db.session.rollback()
            flash(u"Ошибка: обновить информацию о пользователе не удалось!", 'danger')
        return redirect(url_for('admin.users'))
    return render_template('admin/users_change_password.html', form=form)


@admin.route('/admin/users/<int:id>/block', methods=['GET', 'POST'])
@login_required
def users_block(id):
    """Block user to make him unable to enter the system."""
    if current_user.role == 0:
        abort(403)
    _user = User.query.get_or_404(id)
    _user.active = 0
    db.session.add(_user)
    try:
        db.session.commit()
        flash(u"Пользователь заблокирован!", 'success')
    except IntegrityError:
        db.session.rollback()
        flash(u"Ошибка: заблокировать пользователя не удалось!", 'danger')
    return redirect(url_for('admin.users'))


@admin.route('/admin/users/<int:id>/unblock', methods=['GET', 'POST'])
@login_required
def users_unblock(id):
    """Unblock user to make him able to enter the system."""
    if current_user.role == 0:
        abort(403)
    _user = User.query.get_or_404(id)
    _user.active = 1
    db.session.add(_user)
    try:
        db.session.commit()
        flash(u"Пользователь разблокирован!", 'success')
    except IntegrityError:
        db.session.rollback()
        flash(u"Ошибка: разблокировать пользователя не удалось!", 'danger')
    return redirect(url_for('admin.users'))
