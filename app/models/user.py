class User:
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username
        self.role = 'customer'

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

class AdminSeller:
    def __init__(self, username, role='seller'):
        self.username = username
        self.role = role

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return f'admin_seller_{self.username}'
