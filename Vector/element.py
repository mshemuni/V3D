# -*- coding: utf-8 -*-
"""
@author: Mohammad Shameoni Niaei
inspired by: https://github.com/allelos/vectors
Thanks to:

"""
from logging import getLogger

import math


class Point:
    def __init__(self, x=0, y=0, z=0, logger=None):
        # From https://stackoverflow.com/questions/13521981/implementing-an-optional-logger-in-code
        self.logger = logger or getLogger('dummy')
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "{}(x={}, y={}, z={})".format(self.__class__.__name__, self.x, self.y,
                                             self.z)  # From https://github.com/allelos/vectors/blob/master/vectors/vectors.py

    # From https://docs.python.org/3/library/operator.html
    def __sub__(self, other):
        return self.subtract(other)

    def __add__(self, other):
        return self.add(other)

    def __neg__(self):
        return Point(x=-self.x, y=-self.y, z=-self.z, logger=self.logger)

    def __mul__(self, scalar):
        return self.scale(scalar)

    def __rmul__(self, scalar):
        return self.scale(scalar)

    def __truediv__(self, scalar):
        return self.divide(scalar)

    def __eq__(self, other):
        return self.is_same(other)

    def copy(self):
        return Point(x=self.x, y=self.y, z=self.z, logger=self.logger)

    def divide(self, scalar):
        self.logger.info("Calling Point.scale")
        if scalar == 0:
            raise ValueError("Cannot divide by zero")

        return self.scale(1 / scalar)

    def to_polar(self):
        self.logger.info("Converting from cartesian to polar")
        r = math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2) + math.pow(self.z, 2))
        if r == 0:
            return 0, 0, 0

        phi = math.atan2(self.y, self.x)
        theta = math.acos(self.z / r)
        return r, math.degrees(theta), math.degrees(phi)

    def scale(self, scalar):
        self.logger.info("Scaling the {}".format(self))

        if isinstance(scalar, (int, float)):
            return Point(x=self.x * scalar,
                         y=self.y * scalar,
                         z=self.z * scalar, logger=self.logger)
        else:
            self.logger.error("Scalar must be float or int type")
            raise ValueError("Scalar must be float or int type")

    def subtract(self, other):
        self.logger.info("Calling Point.add")
        return self.add(-other)

    def add(self, other):
        self.logger.info("Calculating {} + {}".format(self, other))

        if isinstance(other, Point):

            return Point(x=self.x + other.x,
                         y=self.y + other.y,
                         z=self.z + other.z, logger=self.logger)

        else:
            self.logger.error("Data must be a Point type")
            raise ValueError("Data must be a Point type")

    def dist(self, other=None):
        self.logger.info("Calculating distance between {} and {}".format(self, other))
        if other is None:
            other = Point(logger=self.logger)

        if isinstance(other, Point):
            return math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2) +
                             math.pow(self.z - other.z, 2))
        else:
            self.logger.error("Data must be Point type")
            raise ValueError("Data must be Point type")

    def is_same(self, other):
        self.logger.info("Checking if {} and {} are same points".format(self, other))
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y and self.z == other.z
        else:
            self.logger.error("Data must be Point type")
            raise ValueError("Data must be Point type")

    def from_polar(self, r, theta, phi, override=True):
        self.logger.info("Calculating polar to cartesian")
        if isinstance(r, (int, float)) and isinstance(theta, (int, float)) and isinstance(phi, (int, float)):
            theta = math.radians(theta)
            phi = math.radians(phi)
            x = r * math.sin(theta) * math.cos(phi)
            y = r * math.sin(theta) * math.sin(phi)
            z = r * math.cos(theta)
            if override:
                self.x = x
                self.y = y
                self.z = z
            else:
                return Point(x=x, y=y, z=z, logger=self.logger)
        else:
            self.logger.error("Data must be numeric type")
            raise ValueError("Data must be numeric type")


class Vector:
    def __init__(self, point=None, logger=None):
        # From https://stackoverflow.com/questions/13521981/implementing-an-optional-logger-in-code
        self.logger = logger or getLogger('dummy')

        if point is None:
            point = Point()

        if isinstance(point, Point):
            self.point = point
        else:
            self.point = Vector(Point(logger=self.logger), logger=self.logger)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        # From https://github.com/allelos/vectors/blob/master/vectors/vectors.py
        return "{}({})".format(self.__class__.__name__, self.point)

    # From https://docs.python.org/3/library/operator.html
    def __neg__(self):
        return Vector(-self.point, logger=self.logger)

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.subtract(other)

    def __mul__(self, other):
        return self.multiply(other)

    def __rmul__(self, other):
        return self.multiply(other)

    def __truediv__(self, scalar):
        return self.divide(scalar)

    def __eq__(self, other):
        return self.is_same(other)

    def __abs__(self):
        return self.mag()

    def is_same(self, other):
        return self.point == other.point

    def from_points(self, point1, point2):
        self.logger.info("Creating vector from two points")
        if isinstance(point1, Point) and isinstance(point2, Point):
            self.point = point1 - point2
        else:
            self.logger.error("Data must be Point type")
            raise ValueError("Data must be Point type")

    def copy(self):
        return Vector(self.point.copy(), logger=self.logger)

    def dot(self, other):
        self.logger.info("Calculating dot product of {} and {}".format(self, other))
        if isinstance(other, Vector):
            return self.point.x * other.point.x + self.point.y * other.point.y + self.point.z * other.point.z
        else:
            self.logger.error("Data must be Vector type")
            raise ValueError("Data must be Vector type")

    def multiply(self, other):
        self.logger.info("Calculating {} * {}".format(self, other))
        if isinstance(other, (int, float)):
            return Vector(self.point.scale(other), logger=self.logger)
        elif isinstance(other, Vector):
            return Vector(Point(
                x=self.point.y * other.point.z - self.point.z * other.point.y,
                y=self.point.z * other.point.x - self.point.x * other.point.z,
                z=self.point.x * other.point.y - self.point.y * other.point.x,
                logger=self.logger), logger=self.logger)
        else:
            self.logger.error("Data must be Point or scalar type")
            raise ValueError("Data must be Point or scalar type")

    def mag(self):
        self.logger.info("Calling Point.dist")
        return self.point.dist()

    def divide(self, other):
        self.logger.info("Calling Vector.multiply")
        if isinstance(other, (int, float)):
            if other == 0:
                raise ValueError("Cannot divide by zero")

            return self.multiply(1 / other)
        elif isinstance(other, Vector):
            self.logger.error("Vector by Vector division is not possible")
            raise ValueError("Vector by Vector division is not possible")
        else:
            self.logger.error("Data must be numeric type")
            raise ValueError("Data must be numeric type")

    def add(self, other):
        self.logger.info("Calculating {} + {}".format(self, other))
        if isinstance(other, Vector):
            return Vector(Point(x=self.point.x + other.point.x,
                                y=self.point.y + other.point.y,
                                z=self.point.z + other.point.z,
                                logger=self.logger), logger=self.logger)
        else:
            self.logger.error("Data must be Vector type")
            raise ValueError("Data must be Vector type")

    def subtract(self, other):
        self.logger.info("Calling Vector.add")
        return self.add(-other)

    def heading(self):
        self.logger.info("Calculating Heading")
        r = self.mag()
        phi = math.acos(self.point.z / r)
        theta = math.atan2(self.point.y, self.point.x)
        return math.degrees(theta), math.degrees(phi)

    def unit(self):
        self.logger.info("Calculating unit vector of {}".format(self))
        m = self.mag()
        return Vector(self.point / m, logger=self.logger)

    def angle_between(self, other):
        self.logger.info("calculating angle between {} and {}".format(self, other))
        if isinstance(other, Vector):
            if not self == Vector(Point(logger=self.logger), logger=self.logger):
                if not other == Vector(Point(logger=self.logger), logger=self.logger):
                    unit_other = other.unit()
                    unit_self = self.unit()
                    if not unit_other.point == unit_self.point:
                        return math.degrees(math.acos(self.dot(other) / (self.mag() * other.mag())))
                    else:
                        self.logger.warning("Unit Vectors are the same")
                        return 0
                else:
                    self.logger.error("{} is not a valid Vector".format(other))
                    raise ValueError("{} is not a valid Vector".format(other))
            else:
                self.logger.error("{} is not a valid Vector".format(other))
                raise ValueError("{} is not a valid Vector".format(other))

        else:
            self.logger.error("Data must be Vector type")
            raise ValueError("Data must be Vector type")

    def as_plt(self):
        return [0, self.point.x], [0, self.point.y], [0, self.point.z]

    def normal(self, other):
        self.logger.info("calculating Normal Vector")
        if isinstance(other, Vector):
            nrm = self * Vector
            return nrm.unit()
        else:
            self.logger.error("Data must be Vector type")
            raise ValueError("Data must be Vector type")

    def is_parallel(self, other):
        self.logger.info("Checking if vectors are parallel")
        if isinstance(other, Vector):
            return (self * other).mag() == 0
        else:
            self.logger.error("Data must be Vector type")
            raise ValueError("Data must be Vector type")

    def is_perpendicular(self, other):
        self.logger.info("Checking if vectors are perpendicular")
        if isinstance(other, Vector):
            return self.dot(other) == 0
        else:
            self.logger.error("Data must be Vector type")
            raise ValueError("Data must be Vector type")

    def is_non_parallel(self, other):
        self.logger.info("Checking if vectors are non-parallel")
        if isinstance(other, Vector):
            return not (self.is_parallel(other) or self.is_parallel(other))
        else:
            self.logger.error("Data must be Vector type")
            raise ValueError("Data must be Vector type")

    def rotate(self, alpha=0, beta=0, gamma=0):
        self.logger.info("Rotating Vector")
        # From https://stackoverflow.com/a/14609567/2681662
        if isinstance(alpha, (int, float)) and isinstance(beta, (int, float)) and isinstance(gamma, (int, float)):
            alpha = math.radians(alpha)
            beta = math.radians(beta)
            gamma = math.radians(gamma)

            # Make a copy of Vector
            vec = self.copy()

            # Rotate along X axis
            x = vec.point.x
            y = vec.point.y * math.cos(alpha) - vec.point.z * math.sin(alpha)
            z = vec.point.y * math.sin(alpha) + vec.point.z * math.cos(alpha)
            vec = Vector(Point(x=x, y=y, z=z, logger=self.logger), logger=self.logger)

            # Rotate along Y axis
            x = vec.point.x * math.cos(beta) + vec.point.z * math.sin(beta)
            y = vec.point.y
            z = -vec.point.x * math.sin(beta) + vec.point.z * math.cos(beta)
            vec = Vector(Point(x=x, y=y, z=z, logger=self.logger), logger=self.logger)

            # Rotate along Z axis
            x = vec.point.x * math.cos(gamma) - vec.point.y * math.sin(gamma)
            y = vec.point.x * math.sin(gamma) + vec.point.y * math.cos(gamma)
            z = vec.point.z
            vec = Vector(Point(x=x, y=y, z=z, logger=self.logger), logger=self.logger)

            return vec

        else:
            self.logger.error("Angle must be numeric type")
            raise ValueError("Angle must be numeric type")
