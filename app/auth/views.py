# -*- coding: UTF-8 -*-

from datetime import datetime
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            
            if user.active == 0:  # user is blocked
                flash(u'Ваша учетная запись заблокирована администратором!', 'danger')
                return render_template('auth/login.html', form=form)            
            
            login_user(user, form.remember_me.data)
            
            user.last_login = datetime.utcnow()
            try:
                db.session.add(user)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
            
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'Неверный логин или пароль.', 'danger')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'До свидания!', 'success')
    return redirect(url_for('auth.login'))
