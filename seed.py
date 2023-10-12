from random import randint, choice as rc
from faker import Faker
from app import app
from database import db
from models import User

fake = Faker()

def create_users():
    users = []
    for _ in range(10):
        u = User(name = fake.name(), username = fake.name(), clerkID = fake.name())
        users.append(u)
    return users 

if __name__ == '__main__':
    with app.app_context():
        print("Clearing db...")
        User.query.delete()
        print("Seeding users...")
        users = create_users()
        db.create_all()
        db.session.add_all(users)
        db.session.commit()
        print("Done seeding!")
    