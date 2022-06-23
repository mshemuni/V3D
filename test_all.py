import unittest
from v3d import Point, Vector


class TestPoint(unittest.TestCase):
    def test_init(self):
        p = Point()
        self.assertEqual(p.x, 0)
        self.assertEqual(p.y, 0)
        self.assertEqual(p.z, 0)

        p = Point(1, 1, 1)
        self.assertEqual(p.x, 1)
        self.assertEqual(p.y, 1)
        self.assertEqual(p.z, 1)

        p = Point(z=1, x=2, y=3)
        self.assertEqual(p.x, 2)
        self.assertEqual(p.y, 3)
        self.assertEqual(p.z, 1)

        pc = p.copy()
        self.assertEqual(pc.x, p.x)
        self.assertEqual(pc.y, p.y)
        self.assertEqual(pc.z, p.z)
        self.assertEqual(pc, p)

        p = Point(2, 2, 2)
        p_r = Point(1, 1, 1)
        new_p = p.divide(2)
        self.assertEqual(new_p, p_r)

        p = Point(1, 1, 1)
        polar = p.to_polar()
        self.assertAlmostEqual(polar[0], 1.7320508)
        self.assertAlmostEqual(polar[1], 54.7356103)
        self.assertEqual(polar[2], 45)

        p = Point(1, 1, 1)
        self.assertEqual(p.scale(2), Point(2, 2, 2))

        p = Point(1, 2, 3)
        p2 = Point(1, 1, 1)
        self.assertEqual(p.subtract(p2), Point(0, 1, 2))

        p = Point(1, 2, 3)
        p2 = Point(1, 1, 1)
        self.assertEqual(p.add(p2), Point(2, 3, 4))

        p = Point(2, 2, 2)
        p2 = Point(1, 1, 1)
        self.assertAlmostEqual(p.dist(), 3.4641016)
        self.assertAlmostEqual(p.dist(p2), 1.7320508)

        p = Point(1, 1, 1)
        p2 = Point(1, 1, 1)
        p3 = Point(1, 1, 2)
        self.assertTrue(p.is_same(p2))
        self.assertFalse(p.is_same(p3))

        new_p = Point.from_polar(1.7320508075688772, 54.735610317245346, 45.0)
        self.assertEqual(new_p, Point(1, 1, 1))


class TestVector(unittest.TestCase):
    def test_init(self):
        v = Vector(Point(1, 1, 1))
        self.assertEqual(v.point.x, 1)
        self.assertEqual(v.point.y, 1)
        self.assertEqual(v.point.z, 1)

        v2 = Vector(Point(1, 1, 2))
        self.assertEqual(v2.point.x, 1)
        self.assertEqual(v2.point.y, 1)
        self.assertEqual(v2.point.z, 2)

        v = Vector(Point(1, 1, 1))
        v2 = Vector(Point(1, 1, 1))
        v3 = Vector(Point(1, 1, 2))
        self.assertTrue(v.is_same(v2))
        self.assertFalse(v.is_same(v3))

        self.assertEqual(
            Vector.from_points(
                Point(1, 1, 1), Point(2, 2, 3)
            ),
            Vector(Point(-1, -1, -2))
        )

        v = Vector(Point(1, 1, 1))
        self.assertEqual(v, v.copy())

        v = Vector(Point(1, 1, 1))
        v2 = Vector(Point(3, 1, 4))
        self.assertEqual(v.dot(v2), 8)

        v = Vector(Point(1, 1, 1))
        v2 = Vector(Point(3, 1, 4))
        self.assertEqual(v.multiply(2), Vector(Point(2, 2, 2)))
        self.assertEqual(v.multiply(v2), Vector(Point(3, -1, -2)))

        v = Vector(Point(1, 1, 1))
        self.assertAlmostEqual(v.mag(), 1.7320508)

        v = Vector(Point(2, 2, 2))
        self.assertEqual(v.divide(2), Vector(Point(1, 1, 1)))

        v = Vector(Point(1, 1, 1))
        v2 = Vector(Point(2, 2, 2))
        self.assertEqual(v.add(v2), Vector(Point(3, 3, 3)))

        v = Vector(Point(1, 1, 1))
        v2 = Vector(Point(2, 2, 2))
        self.assertEqual(v.subtract(v2), Vector(Point(-1, -1, -1)))

        v = Vector(Point(1, 1, 1))
        theta, phi = v.heading()
        self.assertAlmostEqual(theta, 54.7356103)
        self.assertEqual(phi, 45)

        v = Vector(Point(1, 1, 1))
        self.assertEqual(v.unit(), Vector(Point(0.5773, 0.5773, 0.5773)))

        v = Vector(Point(1, 1, 1))
        v2 = Vector(Point(3, 1, 4))
        self.assertAlmostEqual(v.angle_between(v2), 25.0658292)

        v = Vector(Point(1, 1, 1))
        self.assertEqual(v.as_plt(), {'x': [0, 1], 'y': [0, 1], 'z': [0, 1]})

        v = Vector(Point(1, 1, 1))
        v2 = Vector(Point(3, 1, 4))
        self.assertEqual(v.normal(v2), Vector(Point(0.8017, -0.2672, -0.5345)))

        v = Vector(Point(1, 1, 1))
        v2 = Vector(Point(1, 1, 1))
        v3 = Vector(Point(3, 1, 4))
        self.assertTrue(v.is_parallel(v2))
        self.assertFalse(v.is_parallel(v3))

        v = Vector(Point(1, 0, 0))
        v2 = Vector(Point(0, 0, 1))
        v3 = Vector(Point(0, 1, 0))
        v4 = Vector(Point(1, 1, 1))
        self.assertTrue(v.is_perpendicular(v2))
        self.assertTrue(v.is_perpendicular(v3))
        self.assertFalse(v.is_perpendicular(v4))

        v = Vector(Point(1, 0, 0))
        v2 = Vector(Point(0, 1, 0))
        v3 = Vector(Point(1, 1, 0))
        self.assertFalse(v.is_non_parallel(v2))
        self.assertTrue(v.is_non_parallel(v3))

        v = Vector(Point(1, 0, 0))
        v2 = Vector(Point(0, 1, 0))
        self.assertEqual(v.rotate_about(v2, 90), Vector(Point(0, 0, -1)))

        v = Vector(Point(1, 1, 1))
        self.assertEqual(v.rotate(alpha=180, beta=0, gamma=0), Vector(Point(1, -1, -1)))


if __name__ == '__main__':
    unittest.main()
