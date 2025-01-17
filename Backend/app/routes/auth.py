from flask import Blueprint, request, jsonify
from app.models import *

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    """
    Only for testing. Auth can only be implement after CAS.
    """
    if not request.json:
        user = User(username="test", sid="12311145")
        db.session.add(user)
        db.session.commit()
        return jsonify({'msg': 'Success', 'sid': user.sid})

    user = User.query.filter_by(username=request.json.get('username')).first()
    if user is None:
        user = User(username=request.json.get('username'), sid="12311145")
        db.session.add(user)
        db.session.commit()
        return jsonify({'msg': 'Success', 'sid': user.sid})

    return jsonify({'msg': 'Success', 'sid': user.sid})


# Utility functions
def check_privilege(user_id, poll_id):
    """
    Check if the user has the privilege to access the poll.
    """
    poll = Polls.query.filter_by(id=poll_id).first()
    if poll is None:
        return False

    if poll.user_id == user_id:
        return True

    owner = User.query.filter_by(id=user_id).first()
    user_group = UserGroup.query.filter_by(user_id=user_id).all()

    for group in user_group:
        if group.group_id == owner.group_id:
            return True

    return False
