# -*- coding: UTF-8 -*-

import unittest
from datetime import datetime
from app.models import Proposal

class ProposalModelTestCase(unittest.TestCase):
    def test_proposal_creation(self):
        """Proposal model - proposal creation test."""
        _proposal = Proposal(
            created=datetime.utcnow(),
            author=11,
            name='Random name',
            cause='Random cause',
            description='Random description',
            number=999999,
            plan='Random plan'
        )

        self.assertTrue(isinstance(_proposal.created, datetime))
        self.assertEqual(_proposal.name, 'Random name')
        self.assertEqual(_proposal.cause, 'Random cause')
        self.assertNotEqual(_proposal.cause, 'Random name')
        self.assertEqual(_proposal.description, 'Random description')
        self.assertEqual(_proposal.number, 999999)
        self.assertTrue(len(_proposal.name) <= 299)
        self.assertIsNotNone(_proposal.author)
