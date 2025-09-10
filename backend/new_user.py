from app import create_app, db, bcrypt
from app.models import User

app = create_app()

with app.app_context():
    username = "Dishant"
    password = "dishant"
    role = "employ"

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        print(f"User {username} already exists.")
    else:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        print(f"User {username} added successfully!")
