
from app import create_app, db
from app.models import User
from flask_bcrypt import Bcrypt

app = create_app()
bcrypt = Bcrypt(app)

with app.app_context():
    password = bcrypt.generate_password_hash("dishant").decode("utf-8")
    new_user = User(
        username="sahil",
        email="sahil@gmail.com",
        password=password,
        role="analyst",
        region=""
    )
    db.session.add(new_user)
    db.session.commit()
    print("✅ User created successfully!")

# docker exec -it dashboard-backend python create_user.py

