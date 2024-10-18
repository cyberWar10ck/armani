from app import app, db

# ایجاد زمینه برنامه
with app.app_context():
    db.create_all()
    print("Database tables created.")
