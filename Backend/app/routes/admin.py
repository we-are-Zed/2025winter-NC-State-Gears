from flask import Blueprint, request, jsonify
from app.models import *

admin = Blueprint('admin', __name__)

# TODO: Add delete uesr with cascade delete of vote_count
