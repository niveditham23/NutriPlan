from app import db
from app.models import User
import datetime


def reset_db():
    db.drop_all()
    db.create_all()

    users =[
        {'full_name': 'Amy Green',   'email': 'amy@b.com', 'pw': 'Amy@7890'},
        {'full_name': 'Tom Holland',   'email': 'tom@b.com', 'pw': 'Tom@7890'},
        {'full_name': 'Yin Guang',   'email': 'yin@b.com', 'pw': 'Yin@7890'},
        {'full_name': 'Sarah Shines', 'email': 'sarah@b.com', 'pw': 'Sarah@7890'},
        {'full_name': 'Joe Keery',    'email': 'joe@b.com',  'pw': 'Joe@7890'},
    ]

    for u in users:
        pw = u.pop('pw')
        user = User(**u)
        user.set_password(pw)
        db.session.add(user)
    db.session.commit()
