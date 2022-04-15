import os
from unittest import TestCase
from sqlalchemy import exc
from app import app
from models import db, User, Message, Follows, Likes

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"
db.create_all()

class UserModelTestCase(TestCase):
    def setup(self):
        db.drop_all()
        db.create_all()
        self.uid = 10000
        u = User.signup("test", "testing1@testing.com", "passcode")
        u.id = self.uid
        db.session.commit()
        self.u = User.query.get(self.uid)
        self.client = app.test_client()
    
    def tearDown(self) -> None:
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_message_model(self):
        m = Message(text = "Test Message", user_id = self.uid)
        db.session.add(m)
        db.session.commit()
        self.assertEqual(len(self.u.messages), 1)
        self.assertEqual(self.u.messages[0].text, "Test Message")

    def test_message_likes(self):
        m1 = Message(text = "Message 1", user_id = self.uid)
        m2 = Message(text = "Message 2", user_id = self.uid)
        u = User.signup("second_test", "test2@test2.com", "password", None)
        uid = 888
        u.id = uid
        db.session.add_all([m1, m2, u])
        db.session.commit()
        u.likes.append(m1)
        db.session.commit()
        l = Likes.query.filter(Likes.user_id == uid).all()
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0].message_id, m1.id)