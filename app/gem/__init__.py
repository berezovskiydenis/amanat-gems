# -*- coding: UTF-8 -*-

from flask import Blueprint

gem = Blueprint('gem', __name__)

from . import views
