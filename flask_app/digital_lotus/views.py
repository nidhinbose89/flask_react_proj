"""View Functions."""
from flask import request, jsonify
from flask_restful import Resource as BaseResource
from flask_login import (login_user, current_user,
                         login_required, logout_user)

from digital_lotus import app, db, login_manager
from digital_lotus.models import User
EXCLUDE_AUTH_VIEWS = ['login', 'logout']


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object or None."""
    user = User.query.get(user_id)
    if user:
        return user


class ResourceViews(BaseResource):
    pass


class LoginViews(BaseResource):
    """Login views."""

    def post(self):
        """Login the user."""
        try:
            # fetch the user data
            user = User.query.filter_by(
                email=request.form.get('email'),
            ).first()
            if user and user.check_password(request.form.get('password')):
                login_user(user, remember=True)
                auth_token = user.encode_auth_token()
                if auth_token:
                    response = {
                        'status': 'success',
                        'id': user.id,
                        'email': user.email,
                        'quota': user.quota,
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode()
                    }
                    return response, 200
            else:
                return {'message': 'User not found for the provided credentials.'}, 200
        except Exception as e:
            response = {
                'message': 'Error occured. {message}. Try again'.format(message=e)
            }
            return response, 500


class RegisterViews(BaseResource):
    """Register views."""

    def post(self):
        """Register user."""
        __request_data = request.json
        first_name = __request_data.get('first_name')
        last_name = __request_data.get('last_name')
        username = __request_data.get('username')
        email = __request_data.get('email')
        password = __request_data.get('password')
        if not all([first_name, last_name, email, password]):
            return {
                "message": "Missing parameters for registration.",
            }, 500
        db.session.add(
            User(**__request_data)
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
        if not current_user.is_authenticated:
            return {
                "message": "No user logged-in.",
            }, 403
        logout_user()
        return {
            "message": "User logged out successfully.",
        }, 200
