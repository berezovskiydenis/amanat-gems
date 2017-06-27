# -*- coding: UTF-8 -*-

from flask import Blueprint

counsil = Blueprint('counsil', __name__)

from . import views
