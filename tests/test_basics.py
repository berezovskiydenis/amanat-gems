# -*- coding: UTF-8 -*-

import unittest
from flask import current_app
from app import create_app, db


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        """Set up application."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        """Tear down application."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_app_exists(self):
        """Test application exists."""
        self.assertFalse(current_app is None)
    
    def test_app_is_testing(self):
        """Test configuration."""
        self.assertTrue(current_app.config['TESTING'])
    
    