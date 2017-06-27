# -*- coding: UTF-8 -*-

import unittest
from datetime import datetime
from time import sleep
from app.models import Gem

class GemModelTestCase(unittest.TestCase):
    def test_gem_creation(self):
        """Gem model - gem creation test."""
        _gem = Gem(
            created=datetime.utcnow(),
            author=111,
            name='Random name',
            cause='Random cause',
            description='Random description',
            number=123456,
            plan='Random plan'
        )
        
        self.assertTrue(isinstance(_gem.created, datetime))
        self.assertEqual(_gem.name, 'Random name')
        self.assertEqual(_gem.cause, 'Random cause')
        self.assertNotEqual(_gem.cause, 'Random name')
        self.assertEqual(_gem.description, 'Random description')
        self.assertEqual(_gem.number, 123456)
        self.assertTrue(_gem.number <= 999999)
        self.assertTrue(len(_gem.name) <= 299)
        self.assertIsNotNone(_gem.author)
        self.assertTrue(_gem.author, 111)

        sleep(1)
        _gem.closed_at = datetime.utcnow()

        self.assertLess(_gem.created, _gem.closed_at)
