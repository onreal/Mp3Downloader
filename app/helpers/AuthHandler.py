from app.model.pgsql.User import User


class AuthHandler:

    @staticmethod
    def authenticate(email, password):

        # find user with email
        user = User.query.filter_by(email=email).first()
        # compare user password with the hashed password
        if user and user.verify_password(password):
            return user

    @staticmethod
    def identity(payload):
        # custom processing. the same as authenticate. see example in docs
        user_id = payload['identity']
        return None
