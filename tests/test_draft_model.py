# -*- coding: UTF-8 -*-

import unittest
from datetime import datetime
from app.models import Draft

class DraftModelTestCase(unittest.TestCase):
    def test_draft_creation(self):
        """Draft model - draft creation test."""
        _draft = Draft(
            created=datetime.utcnow(),
            author=11,
            name='Random name',
            cause='Randon cause',
            description='Random description',
            number=999999,
            plan='Random plan'
        )

        self.assertTrue(isinstance(_draft.created, datetime))
        self.assertEqual(_draft.name, 'Random name')
        self.assertEqual(_draft.number, 999999)
        self.assertTrue(len(_draft.name) <= 299)
        self.assertIsNotNone(_draft.author)
