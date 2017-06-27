# -*- coding: UTF-8 -*-

import unittest
from datetime import datetime
from flask import url_for
from app import create_app, db
from app.models import User, Department, Draft


class FlaskUserTestCase(unittest.TestCase):
    def setUp(self):
        """Set up user interation with application."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Department.generate_fake()
        User.generate_fake()
        self.client = self.app.test_client(use_cookies=True)
    
    
    def tearDown(self):
        """Tear down user interation with application."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    
    def test_home_page(self):
        """Home page access for not authenticated user."""
        response = self.client.get(url_for('main.index'))
        self.assertTrue(response.status_code == 302)


    def test_create_user_and_login(self):
        """New user creation and login to the application test."""
        # Register a new user
        _user = User(
            created=datetime.utcnow(),
            username='foo bar',
            email='foobar@mail.com',
            password='qwerty',
            active=1,
            dep_id=0,
            role=0
        )
        db.session.add(_user)
        db.session.commit()
        
        # Login with a new user
        response = self.client.post(
            url_for('auth.login'),
            data = {
                'email': 'foobar@mail.com',
                'password': 'qwerty'
            },
            follow_redirects=True
        )
        self.assertTrue(response.status_code==200)
        self.assertTrue('foo bar' in response.get_data(as_text=True))

        # Logout
        response = self.client.get(url_for('auth.logout'), follow_redirects=True)
        self.assertTrue(response.status_code==200)
        self.assertFalse('foo bar' in response.get_data(as_text=True))


    def test_wrong_login(self):
        """Login fail with wrong password test."""
        # Register a new user
        _user = User(
            created=datetime.utcnow(),
            # last_login=datetime.utcnow(),
            username='cat dog',
            email='catdog@mail.com',
            password='qwerty',
            active=1,
            dep_id=0,
            role=0
        )
        db.session.add(_user)
        db.session.commit()

        # Login with wrong password
        response = self.client.post(
            url_for('auth.login'),
            data = {
                'email': 'catdog@mail.com',
                'password': 'cat' # wrong
            },
            follow_redirects=True
        )
        self.assertFalse('cat dog' in response.get_data(as_text=True))


    def test_draft_creation(self):
        """New draft creation test."""
        # get random user
        _user = db.session.query(User).filter(User.role==0).first()
        self.assertIsNotNone(_user)
        # login
        response = self.client.post(
            url_for('auth.login'),
            data = {
                'email': _user.email,
                'password': _user.password
            },
            follow_redirects=True
        )
        # write draft
        response = self.client.post(
            url_for('draft.drafts_add'),
            data = {
                'name': "Random name",
                'cause': "Random cause",
                'description': "Random description"
            },
            follow_redirects=True
        )
        # complete test
        _draft = db.session.query(Draft).filter(Draft.name=='Random name').first()
        self.assertIsNotNone(_draft)
        self.assertEqual(_draft.name, "Random name")
        self.assertEqual(_draft.cause, "Random cause")
        self.assertEqual(_draft.description, "Random description")
        self.assertEqual(_draft.plan, '')
