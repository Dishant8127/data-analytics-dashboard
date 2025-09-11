# # new_user,py

# from app import create_app, db, bcrypt
# from app.models import User

# app = create_app()

# with app.app_context():
#     username = "Dishant"
#     password = "dishant"
#     role = "employ"
#     email = "dishantpatel@gmail.com"  # ✅ define email

#     existing_user = User.query.filter_by(username=username).first()
#     if existing_user:
#         print(f"User {username} already exists.")
#     else:
#         hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

#         # ✅ include email here
#         new_user = User(username=username, email=email, password=hashed_password, role=role)
#         db.session.add(new_user)
#         db.session.commit()
#         print(f"User {username} added successfully!")




# Drop all tables and recreate:

# from app import create_app, db

# # Create the app instance
# app = create_app()

# # Run inside application context
# with app.app_context():
#     db.drop_all()
#     db.create_all()
#     print("✅ Database reset successful")


from app import create_app, db
from app.models import User
from app import bcrypt

app = create_app()

with app.app_context():
    # Drop and recreate all tables
    # db.drop_all()
    # db.create_all()

    # Add a default admin user
    username = "dk"
    email = "2203051050937@paruluniversity.ac.in"
    password = "dk"
    role = "manager"

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(username=username, email=email, password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()

    print("✅ Database reset and default admin user created successfully!")
