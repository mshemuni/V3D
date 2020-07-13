import unittest
from unittest.mock import patch
from element import Point
from element import Vector

from random import randint


class TestEmployee(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setupClass')

    @classmethod
    def tearDownClass(cls):
        print('teardownClass')

    def setUp(self):
        print('setUp')
        self.p1 = Point(0.5, 0.5, 0.7071)
        self.v1 = Vector(self.p1)
        self.v1_polar = (1, 45, 45)

        self.p2 = Point(0, 1, 0)
        self.v2 = Vector(self.p2)
        self.v2_polar = (1, 90, 90)

        self.p3 = Point(0, 0, 0)
        self.v3 = Vector(self.p3)
        self.v3_polar = (0, 0, 0)

        self.p4 = Point(1, 2, 3)
        self.v4 = Vector(self.p4)

        self.p5 = Point(-1, 7, -3)
        self.v5 = Vector(self.p5)

    def tearDown(self):
        print('tearDown\n')

    def test_to_polar(self):
        print('test_email')
        r1, theta1, phi1 = self.p1.to_polar()
        self.assertAlmostEqual(r1, self.v1_polar[0], places=3)
        self.assertAlmostEqual(theta1, self.v1_polar[1], places=3)
        self.assertAlmostEqual(phi1, self.v1_polar[2], places=3)

        r2, theta2, phi2 = self.p2.to_polar()
        self.assertAlmostEqual(r2, self.v2_polar[0], places=3)
        self.assertAlmostEqual(theta2, self.v2_polar[1], places=3)
        self.assertAlmostEqual(phi2, self.v2_polar[2], places=3)

        r3, theta3, phi3 = self.p3.to_polar()
        self.assertAlmostEqual(r3, self.v3_polar[0], places=3)
        self.assertAlmostEqual(theta3, self.v3_polar[1], places=3)
        self.assertAlmostEqual(phi3, self.v3_polar[2], places=3)
    #     self.assertEqual(self.emp_2.email, 'Sue.Smith@email.com')
    #
    #     self.emp_1.first = 'John'
    #     self.emp_2.first = 'Jane'
    #
    #     self.assertEqual(self.emp_1.email, 'John.Schafer@email.com')
    #     self.assertEqual(self.emp_2.email, 'Jane.Smith@email.com')
    #
    # def test_fullname(self):
    #     print('test_fullname')
    #     self.assertEqual(self.emp_1.fullname, 'Corey Schafer')
    #     self.assertEqual(self.emp_2.fullname, 'Sue Smith')
    #
    #     self.emp_1.first = 'John'
    #     self.emp_2.first = 'Jane'
    #
    #     self.assertEqual(self.emp_1.fullname, 'John Schafer')
    #     self.assertEqual(self.emp_2.fullname, 'Jane Smith')
    #
    # def test_apply_raise(self):
    #     print('test_apply_raise')
    #     self.emp_1.apply_raise()
    #     self.emp_2.apply_raise()
    #
    #     self.assertEqual(self.emp_1.pay, 52500)
    #     self.assertEqual(self.emp_2.pay, 63000)
    #
    # def test_monthly_schedule(self):
    #     with patch('employee.requests.get') as mocked_get:
    #         mocked_get.return_value.ok = True
    #         mocked_get.return_value.text = 'Success'
    #
    #         schedule = self.emp_1.monthly_schedule('May')
    #         mocked_get.assert_called_with('http://company.com/Schafer/May')
    #         self.assertEqual(schedule, 'Success')
    #
    #         mocked_get.return_value.ok = False
    #
    #         schedule = self.emp_2.monthly_schedule('June')
    #         mocked_get.assert_called_with('http://company.com/Smith/June')
    #         self.assertEqual(schedule, 'Bad Response!')


if __name__ == '__main__':
    unittest.main()
