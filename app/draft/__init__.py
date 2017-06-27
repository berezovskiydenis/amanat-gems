# -*- coding: UTF-8 -*-

from flask import Blueprint

draft = Blueprint('draft', __name__)

from . import views
