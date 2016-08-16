
from project import db
from project.models import User

# insert data
db.session.add(User("BeerShed_Admins", "BeerShed@mail.com", "foundingFathers2?", 'admin'))
db.session.add(User("Guest", "guest@guest.com", "guest_user", 'guest'))

# commit the changes
db.session.commit()
