from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

class AdminSeller(UserMixin):
    def __init__(self, username):
        self.id = username
        self.username = username
        self.role = 'admin_seller'
