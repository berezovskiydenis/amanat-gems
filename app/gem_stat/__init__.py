# -*- coding: UTF-8 -*-

from flask import Blueprint

gem_stat = Blueprint('gem_stat', __name__)

from . import views
