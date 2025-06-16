from app import app, db
# creates a blank database
def create_database():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_database()