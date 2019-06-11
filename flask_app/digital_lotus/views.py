#!/usr/bin/env python3

"""View Functions."""
from flask import request, jsonify
from flask_restful import Resource as BaseResource
from flask_login import (login_user, current_user,
                         login_required, logout_user)

from digital_lotus import app, db, login_manager
from digital_lotus.models import User
from digital_lotus.notebook import data_analysis

EXCLUDE_AUTH_VIEWS = ['login', 'logout']


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object or None."""
    user = User.query.get(user_id)
    if user:
        return user


class ResourceViews(BaseResource):
    """Resource views."""

    def get(self, graph_name):
        """Get the graph data and type as per name."""
        pass


class LoginViews(BaseResource):
    """Login views."""

    def post(self):
        """Login the user."""
        try:
            # fetch the user data
            _request_data = request.json
            user = User.query.filter_by(
                username=_request_data.get('username'),
            ).first()
            if user and user.check_password(_request_data.get('password')):
                res = login_user(user, remember=True)
                if res:
                    response = {
                        'status': 'success',
                        'id': user.id,
                        'email': user.email,
                        'username': user.username,
                        'message': 'Successfully logged in.',
                    }
                    return response, 200
                else:
                    return {'message': 'Wrong Credentials. Please try again.'}, 204
            else:
                return {'message': 'Wrong Credentials. Please try again.'}, 204
        except Exception as e:
            response = {
                'message': 'Error occured. {message}. Try again'.format(message=e)
            }
            return response, 500


class RegisterViews(BaseResource):
    """Register views."""

    def post(self):
        """Register user."""
        _request_data = request.json
        first_name = _request_data.get('first_name')
        last_name = _request_data.get('last_name')
        username = _request_data.get('username')
        email = _request_data.get('email')
        password = _request_data.get('password')
        if not all([first_name, last_name, email, password]):
            return {
                "message": "Missing parameters for registration.",
            }, 500
        db.session.add(
            User(**_request_data)
        )
        try:
            db.session.commit()
        except Exception as e:
            return {
                "message": f"User creation failed with message: {e}",
            }, 500
        else:
            return {
                "message": "User created successfully.",
            }, 200


class LogoutViews(BaseResource):
    """Logout views."""

    def post(self):
        """Logout user."""
        logout_user()
        return {
            "message": "User logged out successfully.",
        }, 200
