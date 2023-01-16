# from unittest import TestCase
# from flask_sqlalchemy import SQLAlchemy
# from app import app, create_test_app
# from models.models import User, Campaign, Player, Demo, Vitals, Combat, Spells, Level, Ability, Proficiency, Items, db, connect_db

# class UserTests(TestCase):
#     """Tests for user views."""

#     def create_test_app(self):
#         return create_test_app()

#     def setUp(self):

#         db.create_all()

#         username = 'Test User'
#         email = 'test@email.com'
#         password = 'password'
#         user = User.register(username, email, password)

#         db.session.add(user)
#         db.session.commit()

#         db.session.refresh(user)

#         self.user = user

#     def tearDown(self):

#         session.pop('username')
#         session.pop('user_id')

#         db.session.rollback()
#         db.drop_all()

#     def test_user_detail(self):
#         session['username'] = 'Test User'
#         session['user_id'] = f'{self.user_id}'
#         response = client.get("/", follow_redirects=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('Test User', str(response.data))