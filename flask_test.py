from unittest import TestCase

from app import app
from models import User, db

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

with app.app_context():
    db.drop_all()
    db.create_all()


class UserModelTestCase(TestCase):


    def setUp(self):
        with app.app_context():
            User.query.delete()
            user1 = User(first_name='Spike',last_name='Lee')
            db.session.add(user1)
            db.session.commit()
            self.user_id = user1.id

    def tearDown(self):
        with app.app_context():
            db.session.rollback()

    def test_home_route(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertIn('Spike Lee',html)
            self.assertEqual(resp.status_code, 200)


    def test_user_page(self):
        with app.test_client() as client:
            resp = client.get(f"/user/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertIn('<h4>Spike Lee</h4>',html)
            self.assertEqual(resp.status_code, 200)

    def test_add_page(self):
        with app.test_client() as client:
            resp = client.get("/adduser")
            html = resp.get_data(as_text=True)

            self.assertIn('<input type="text" name="first_name" id="first" placeholder="John">',html)
            self.assertEqual(resp.status_code, 200)

    def test_add_to_db(self):
        with app.test_client() as client:
            new_user = {'first_name':'Ryan','last_name':'Gosling','profile_pic':'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png'}
            resp = client.post("/adduser",data=new_user, follow_redirects=True)   
            html = resp.get_data(as_text=True)

            self.assertIn('<h4>Ryan Gosling</h4>',html)
            self.assertEqual(resp.status_code, 200)