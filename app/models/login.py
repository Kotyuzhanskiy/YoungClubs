from app import login
from models import User

@login.user_loader
def load_user(id):
    return User.query.get(int(id))