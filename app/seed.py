from faker import Faker
import random

from app import models, db


# Create random users and profiles on app startup
def seed_users():
    fake = Faker()
    users = []
    for _ in range(10):  # Create 10 random users
        username = fake.user_name()
        password = "password"  # Default password for all users
        name = fake.name()
        email = fake.email()
        photo = None  # No photo for simplicity

        user = models.User(
            username=username, password=password, name=name, email=email, photo=photo
        )
        db.session.add(user)
        db.session.commit()
        users.append(user)

        # Create random profile for each user
        profile = models.Profile(
            user_id_fk=user.id,
            description=fake.sentence(),
            parish=fake.city(),
            biography=fake.text(),
            sex=random.choice(["Male", "Female"]),
            race=random.choice(["Caucasian", "Black", "Asian", "Latino"]),
            birth_year=random.randint(1980, 2000),
            height=random.uniform(1.5, 2.0),
            fav_cuisine=random.choice(["Italian", "Chinese", "Indian", "Jamaican"]),
            fav_colour=random.choice(["Red", "Blue", "Green", "Yellow"]),
            fav_school_subject=random.choice(
                ["Math", "Science", "History", "Geography"]
            ),
            political=random.choice([True, False]),
            religious=random.choice([True, False]),
            family_oriented=random.choice([True, False]),
        )
        db.session.add(profile)

        # Add some random favourites
        if random.random() > 0.5:  # 50% chance to create a favourite relationship
            fav_user = random.choice(users)  # Pick a random user from the list
            if fav_user.id != user.id:
                favourite = models.Favourite(
                    user_id_fk=user.id, fav_user_id_fk=fav_user.id
                )
                db.session.add(favourite)

    db.session.commit()
