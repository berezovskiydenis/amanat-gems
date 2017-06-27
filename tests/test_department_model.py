# -*- coding: UTF-8 -*-

import unittest
from datetime import datetime
from app.models import Department


class DepartmentModelTestCase(unittest.TestCase):

    def test_department_creation(self):
        """Department model - department creation test."""
        d = Department(
            depname="New Department Name"
        )
        self.assertEqual(d.depname, "New Department Name")
