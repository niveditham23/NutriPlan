from app import db
from app.models import User,UserInfo
import datetime

# from app.views import user_info


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

    user_infos = [
        {'age': 28, 'gender': 'female', 'height': 165, 'weight': 60, 'diet_type': 'vegan', 'allergies': 'gluten,nuts','health_conditions': 'pcos', 'primary_goal': 'maintain', 'activity_level': 'lightlyactive'},
        {'age': 35, 'gender': 'male', 'height': 180, 'weight': 80, 'diet_type': 'non-veg', 'allergies': None,'health_conditions': 'diabetes', 'primary_goal': 'lose', 'activity_level': 'moderatelyactive'},
        {'age': 42, 'gender': 'male', 'height': 170, 'weight': 70, 'diet_type': 'keto', 'allergies': 'soya','health_conditions': 'thyroid', 'primary_goal': 'gain', 'activity_level': 'sedentary'},
        {'age': 30, 'gender': 'female', 'height': 175, 'weight': 75, 'diet_type': 'mediterranean', 'allergies': 'peanuts','health_conditions': None, 'primary_goal': 'maintain', 'activity_level': 'very_active'},
        {'age':37, 'gender': 'male', 'height': 175, 'weight': 75, 'diet_type': 'mediterranean', 'allergies': 'peanuts','health_conditions':None, 'primary_goal': 'maintain', 'activity_level': 'very_active'}

    ]

    for u,info in zip(users,user_infos):
        pw = u.pop('pw')
        user = User(**u)
        user.set_password(pw)
        db.session.add(user)
        db.session.flush()
        info_obj=UserInfo(user_id=user.id,**info)
        db.session.add(info_obj)
    db.session.commit()
