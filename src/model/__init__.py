from .auth import Auth, User
from .comment import Comment

# init admin
from flask_admin.contrib.sqla import ModelView
from src.middleware import admin
from src.middleware import db

admin.add_view(ModelView(Auth, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Comment, db.session))