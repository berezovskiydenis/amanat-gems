# -*- coding: UTF-8 -*-

import unittest
from datetime import datetime
from app.models import User


class UserModelTestCase(unittest.TestCase):

    def test_password_setter(self):
        """Test user password verifying."""
        u = User(
            created=datetime.utcnow(),
            last_login=datetime.utcnow(),
            username='cat',
            email='cat@mail.com',
            password='qwerty',
            active=1,
            dep_id=0,
            role=0
        )
        self.assertTrue(u.verify_password('qwerty'))
        self.assertFalse(u.verify_password('mouse'))
    
    def test_user_creation(self):
        """User model - user creation test."""
        u = User(
            created=datetime.utcnow(),
            last_login=datetime.utcnow(),
            username='cat',
            email='cat@mail.com',
            password='qwerty',
            active=1,
            dep_id=0,
            role=0
        )
        self.assertTrue(isinstance(u.created, datetime))
        self.assertNotEqual(u.active, 0)
        self.assertEqual(u.dep_id, 0)
        self.assertEqual(u.role, 0)
