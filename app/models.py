from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from dataclasses import dataclass
import datetime

@dataclass
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    full_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True,nullable=False)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    time:so.Mapped[datetime.datetime] = so.mapped_column(sa.DateTime,default=datetime.datetime.utcnow)
    user_info:so.Mapped[list['UserInfo']]=relationship(back_populates="user")
    personal_meal_data:so.Mapped[list['PersonalMealData']]=relationship(back_populates="user")

    def __repr__(self):
        pwh= 'None' if not self.password_hash else f'...{self.password_hash[-5:]}'
        return f'User(id={self.id}, full_name={self.full_name}, email={self.email}, pwh={pwh})'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class UserInfo(db.Model):
    __tablename__ = 'user_info'
    __table_args__ = (sa.UniqueConstraint('user_id'),)
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'), index=True)
    age: so.Mapped[int]
    gender: so.Mapped[str]
    height: so.Mapped[int]
    weight: so.Mapped[int]
    diet_type: so.Mapped[str]
    allergies: so.Mapped[Optional[str]]
    health_conditions: so.Mapped[Optional[str]]
    primary_goal: so.Mapped[str]
    activity_level: so.Mapped[str]
    user: so.Mapped['User'] = relationship(back_populates='user_info')

    def __repr__(self):
        return f'UserInfo(id={self.id},user_id={self.user_id}, age={self.age}, gender={self.gender}, height={self.height},weight={self.weight},diet_type={self.diet_type},allergies={self.allergies},health_conditions={self.health_conditions},primary_goal={self.primary_goal},activity_level={self.activity_level})'

class MealData(db.Model):
    __tablename__ = 'meal_data'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    meal_type: so.Mapped[str]=so.mapped_column(sa.String(60),nullable=False)
    meal_name:so.Mapped[str] = so.mapped_column(sa.String(100),nullable=False)
    calories:so.Mapped[int]=so.mapped_column(sa.Integer,nullable=False)
    recipe: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    diet_type: so.Mapped[str] = so.mapped_column(sa.Text, nullable=False)
    allergens: so.Mapped[str]=so.mapped_column(sa.Text, nullable=True)
    health_conditions: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)

    def __repr__(self):
        return f'MealData(id={self.id},meal_type={self.meal_type}, meal_name={self.meal_name}, calories={self.calories},recipe={self.recipe},diet_type={self.diet_type},allergens={self.allergens},health_conditions={self.health_conditions})'


class PersonalMealData(db.Model):
    __tablename__ = 'personal_meal_data'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id:so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'), index=True)
    meal_type: so.Mapped[str] = so.mapped_column(sa.String(60), nullable=False)
    meal_name: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=False)
    calories: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    recipe: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)

    user: so.Mapped['User'] = relationship(back_populates='personal_meal_data')
    def __repr__(self):
        return f'PersonalMealData(id={self.id},user_id={self.user_id},meal_type={self.meal_type}, meal_name={self.meal_name}, calories={self.calories},recipe={self.recipe})'
