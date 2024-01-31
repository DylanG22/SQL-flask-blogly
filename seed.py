from models import db, User



#create all tables
def seed_db():

    db.drop_all()
    db.create_all()


    User.query.delete()

    user1 = User(first_name='Spike',last_name='Lee')
    user2 = User(first_name='Dylan',last_name='Gooch')
    user3 = User(first_name='Christopher',last_name='Nolan')
    user4 = User(first_name='Ryan',last_name='Gosling')


    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)


    db.session.commit()