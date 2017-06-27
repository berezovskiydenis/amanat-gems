# -*- coding: UTF-8 -*-

from flask import Blueprint

proposal = Blueprint('proposal', __name__)

from . import views
