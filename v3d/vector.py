# -*- coding: utf-8 -*-
"""
@author: Mohammad Shameoni Niaei
inspired by: https://github.com/allelos/vectors
Thanks to: https://github.com/allelos/
"""
from __future__ import annotations
from typing import Union

from logging import getLogger
from logging import Logger

import math

from .point import Point


class Vector:
    logger = getLogger('dummy')

    def __init__(self, point: Point = None, logger: Logger = None) -> None:
        """
        Constructor method

        >>> Vector(Point(1, 1, 1))
        Vector(Point(x=1, y=1, z=1))
        >>> Vector(Point(1, 1, 2))
        Vector(Point(x=1, y=1, z=2))


        :param point: Point value of a vector
        :param logger: Logger to log
        """
        # From https://stackoverflow.com/questions/13521981/implementing-an-optional-logger-in-code
        self.logger = logger or getLogger('dummy')

        if logger is not None:
            self.logger = logger

        # If the point is not given. Create a zero point and assign it to point
        if point is None:
            point = Point()

        self.point = point

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        # From https://github.com/allelos/vectors/blob/master/vectors/vectors.py
        return "{}({})".format(self.__class__.__name__, self.point)

    # From https://docs.python.org/3/library/operator.html
    def __neg__(self) -> Vector:
        # Change sign of point on -a
        return Vector(-self.point, logger=self.logger)

    def __add__(self, other: Vector) -> Vector:
        # Call self.add on a + b
        return self.add(other)

    def __sub__(self, other: Vector) -> Vector:
        # Call self.subtract on a - b
        return self.subtract(other)

    def __mul__(self, other: Union[Vector, float, int]) -> Vector:
        # Call self.scale on a * b
        return self.multiply(other)

    def __rmul__(self, other: Union[Vector, float, int]) -> Vector:
        # Call self.scale on b * a
        return self.multiply(other)

    def __truediv__(self, scalar: float) -> Vector:
        # Call self.divide on a / b
        return self.divide(scalar)

    def __eq__(self, other: Vector) -> bool:
        # Call self.is_same on a == b
        return self.is_same(other)

    def __abs__(self) -> float:
        # call self.mag of abs(a)
        return self.mag()

    def is_same(self, other: Vector) -> bool:
        """
        Checks if two vectors are the same.
        One cannot check if two vectors are exactly the same, since x, y and z values of a point are floats.

        >>> v = Vector(Point(1, 1, 1))
        >>> v2 = Vector(Point(1, 1, 1))
        >>> v3 = Vector(Point(1, 1, 2))
        >>> v.is_same(v2)
        True
        >>> v.is_same(v3)
        False


        :param other: The other Vector to compair with this.
        :return: True if the two vectors are the same, False if otherwise.
        """
        # Check if two Vector is same as other by checking
        # if points assigned to Vector and other are same.
        return self.point == other.point

    @classmethod
    def from_points(cls, point1: Point, point2: Point) -> Vector:
        """
        Creates a Vectror from given two points

        :param point1: First point. To be translated to the origin
        :param point2: Second Point

        >>> Vector.from_points(Point(1, 1, 1), Point(2, 2, 3))
        Vector(Point(x=-1, y=-1, z=-2))


        :return: A vectro from two points
        """
        cls.logger.info("Creating vector from two points")
        # Check if point1 and point2 are Point
        if isinstance(point1, Point) and isinstance(point2, Point):
            # Assign Vector's Point ot point1 - point2
            return Vector(point1 - point2)
        else:
            # Raise an error if point1 or point2 is not Point
            cls.logger.error("Data must be Point type")
            raise ValueError("Data must be Point type")

    def copy(self) -> Vector:
        """
        Returns a copy of the vector

        >>> v = Vector(Point(1, 1, 1))
        >>> v.copy()
        Vector(Point(x=1, y=1, z=1))


        :return: The copied Vector
        """
        # Make a copy of Vector by returning a new Vector
        # with a copy of this.point is assigned as Point
        return Vector(self.point.copy(), logger=self.logger)

    def dot(self, other: Vector) -> float:
        """
        Returns dot product of two vectors

        >>> v = Vector(Point(1, 1, 1))
        >>> v2 = Vector(Point(3, 1, 4))
        >>> v.dot(v2)
        8


        :param other: Second vector
        :return: Dot product of two vectors
        """
        self.logger.info("Calculating dot product of {} and {}".format(self, other))
        # Check if the other is a Vector
        if isinstance(other, Vector):
            # Calculate and return dot product of two vectors
            return self.point.x * other.point.x + self.point.y * other.point.y + self.point.z * other.point.z
        else:
            # Raise an error if the other is not a Vector
            self.logger.error("Data must be Vector type")
            raise ValueError("Data must be Vector type")

    def multiply(self, other: Union[Vector, float, int]) -> Vector:
        """
        Returns either vector by vector or scalar by vector multiplication depending on given other.

        >>> v = Vector(Point(1, 1, 1))
        >>> v2 = Vector(Point(3, 1, 4))
        >>> v.multiply(2)
        Vector(Point(x=2, y=2, z=2))
        >>> v.multiply(v2)
        Vector(Point(x=3, y=-1, z=-2))


        :param other: Either scalar or vector.
        :return: Result of multiplication
        """
        self.logger.info("Calculating {} * {}".format(self, other))
        # Check if other is float or int (in short if it's numeric)
        if isinstance(other, (int, float)):
            # Scale Vector's Point with the scalar
            return Vector(self.point.scale(other), logger=self.logger)
        elif isinstance(other, Vector):
            # If it's a Vector than calculate cross product of two vectors
            return Vector(Point(x=self.point.y * other.point.z - self.point.z * other.point.y,
                                y=self.point.z * other.point.x - self.point.x * other.point.z,
                                z=self.point.x * other.point.y - self.point.y * other.point.x,
                                logger=self.logger), logger=self.logger)
        else:
            # Raise an error if other is neither numeric nor a vector
            self.logger.error("Data must be Vector or scalar type")
            raise ValueError("Data must be Vector or scalar type")

    def mag(self) -> float:
        """
        Returns the length of the vector.

        >>> v = Vector(Point(1, 1, 1))
        >>> v.mag()
        1.7320508075688772


        :return: The length of the vector
        """
        self.logger.info("Calling Point.dist")
        # Calls self.point's dist method
        return self.point.dist()

    def divide(self, other: Union[float, int]) -> Vector:
        """
        Returns a down scaled vector

        >>> v = Vector(Point(2, 2, 2))
        >>> v.divide(2)
        Vector(Point(x=1.0, y=1.0, z=1.0))


        :param other: Scalar to down scale
        :return: The new down scaled Vector
        """
        self.logger.info("Calling Vector.multiply")
        # Check if other is float or int (in short if it's numeric)
        if isinstance(other, (int, float)):
            # Raise an error if other is zero
            if other == 0:
                raise ValueError("Cannot divide by zero")

            # Calls self.multiply for 1/other
            return self.multiply(1 / other)

        elif isinstance(other, Vector):
            # Raise an error if other is a Vector
            self.logger.error("Vector by Vector division is not possible")
            raise ValueError("Vector by Vector division is not possible")
        else:
            # Raise an error if other is not numeric
            self.logger.error("Data must be numeric type")
            raise ValueError("Data must be numeric type")

    def add(self, other: Vector) -> Vector:
        """
        Return addition of two vectors

        >>> v = Vector(Point(1, 1, 1))
        >>> v2 = Vector(Point(2, 2, 2))
        >>> v.add(v2)
        Vector(Point(x=3, y=3, z=3))


        :param other: The vector to add to this vector
        :return: The addition result as a Vector
        """
        self.logger.info("Calculating {} + {}".format(self, other))
        # Check if other is a Vector
        if isinstance(other, Vector):
            # Return a new Vector with point as sum of this and other's points
            return Vector(self.point + other.point, logger=self.logger)
        else:
            # Raise and error if other is not a Vector
            self.logger.error("Data must be Vector type")
            raise ValueError("Data must be Vector type")

    def subtract(self, other: Vector) -> Vector:
        """
        Return subtraction of two vectors

        >>> v = Vector(Point(1, 1, 1))
        >>> v2 = Vector(Point(2, 2, 2))
        >>> v.subtract(v2)
        Vector(Point(x=-1, y=-1, z=-1))


        :param other: The vector to subtract from this vector
        :return: The subtraction result as a Vector
        """
        self.logger.info("Calling Vector.add")
        # Call add with negative value of other vector
        return self.add(-other)

    def heading(self) -> tuple[float, float]:
        """
        Returns heading angle of the vector

        >>> v = Vector(Point(1, 1, 1))
        >>> v.heading()
        (54.735610317245346, 45.0)


        :return: Angles of the vector
        """
        self.logger.info("Calculating Heading")
        # Calculate Magnitude of Vector
        r = self.mag()
        # Use Jacobian to calculate theta and phi
        phi = math.atan2(self.point.y, self.point.x)

        theta = math.acos(self.point.z / r)
        return math.degrees(theta), math.degrees(phi)

    def unit(self) -> Vector:
        """
        Returns unit vector

        >>> v = Vector(Point(1, 1, 1))
        >>> v.unit()
        Vector(Point(x=0.5773502691896258, y=0.5773502691896258, z=0.5773502691896258))


        :return: The unit vector of this vector
        """
        self.logger.info("Calculating unit vector of {}".format(self))
        # Divide self with magnitude and return as a new vector
        m = self.mag()
        return Vector(self.point / m, logger=self.logger)

    def angle_between(self, other: Vector) -> float:
        """
        Returns angle between this and the given vector

        >>> v = Vector(Point(1, 1, 1))
        >>> v2 = Vector(Point(3, 1, 4))
        >>> v.angle_between(v2)
        25.065829224994683


        :param other: The vector to calculate angle between this
        :return: Angle between this and given vector
        """
        self.logger.info("calculating angle between {} and {}".format(self, other))
        # Check if the other is a Vector
        if isinstance(other, Vector):
            # Check if Vector is not equal to a zero Vector
            if not self == Vector(Point(logger=self.logger), logger=self.logger):
                # Check if Vector is not equal to the other
                if not other == Vector(Point(logger=self.logger), logger=self.logger):
                    # Calculate Unit Vector of Vector and the other vector
                    unit_other = other.unit()
                    unit_self = self.unit()
                    # Check if unit vectors are not same
                    if not unit_other.point == unit_self.point:
                        # Calculate and return angle between two Vectors
                        return math.degrees(math.acos(self.dot(other) / (self.mag() * other.mag())))
                    else:
                        # Return zero as angle because unit vectors are same
                        self.logger.warning("Unit Vectors are the same")
                        return 0
                else:
                    # Raise an error if other is not a valid Vector. Its zero Vector
                    self.logger.error("{} is not a valid Vector".format(other))
                    raise ValueError("{} is not a valid Vector".format(other))
            else:
                # Raise an error if vector is zero vector
                self.logger.error("{} is not a valid Vector".format(other))
                raise ValueError("{} is not a valid Vector".format(other))
        else:
            # Raise an error if other is not a Vector
            self.logger.error("Data must be Vector type")
            raise ValueError("Data must be Vector type")

    def as_plt(self) -> dict:
        """
        Returns values to plot on matplotlib

        >>> v = Vector(Point(1, 1, 1))
        >>> v.as_plt()
        {'x': [0, 1], 'y': [0, 1], 'z': [0, 1]}


        :return: a dict of x, y and z values
        """
        # Returns a dictionary for plotting with matplotlib
        return {"x": [0, self.point.x], "y": [0, self.point.y], "z": [0, self.point.z]}

    def normal(self, other: Vector) -> Vector:
        """
        Returns normal (unit) vector of two vectors

        >>> v = Vector(Point(1, 1, 1))
        >>> v2 = Vector(Point(3, 1, 4))
        >>> v.normal(v2)
        Vector(Point(x=0.8017837257372732, y=-0.2672612419124244, z=-0.5345224838248488))


        :param other: Other vector
        :return: A unit vector normal to a plane which this and other vector are on.
        """
        self.logger.info("calculating Normal Vector")
        # Check if other is a Vector
        if isinstance(other, Vector):
            # Return unit vector of cross product of Vector and other
            nrm = self * other
            return nrm.unit()
        else:
            # Raise an error if other is not a Vector
            self.logger.error("Data must be Vector type")
            raise ValueError("Data must be Vector type")

    def is_parallel(self, other: Vector) -> bool:
        """
        Checks if two vectors are parallel

        >>> v = Vector(Point(1, 1, 1))
        >>> v2 = Vector(Point(1, 1, 1))
        >>> v3 = Vector(Point(3, 1, 4))
        >>> v.is_parallel(v2)
        True
        >>> v.is_parallel(v3)
        False


        :param other: Other vector to check
        :return: True if this and other vector are parallel, False otherwise
        """
        self.logger.info("Checking if vectors are parallel")
        # Check if the other is Vector
        if isinstance(other, Vector):
            # Return True if vecotr and other's cross products's
            # magnitude is zero
            return (self * other).mag() == 0
        else:
            # Raise an error if the other is not a vector
            self.logger.error("Data must be Vector type")
            raise ValueError("Data must be Vector type")

    def is_perpendicular(self, other: Vector) -> bool:
        """
        Checks if two vectors are perpendicular

        >>> v = Vector(Point(1, 0, 0))
        >>> v2 = Vector(Point(0, 0, 1))
        >>> v3 = Vector(Point(0, 1, 0))
        >>> v4 = Vector(Point(1, 1, 1))
        >>> v.is_perpendicular(v2)
        True
        >>> v.is_perpendicular(v3)
        True
        >>> v.is_perpendicular(v4)
        False


        :param other: Other vector to check
        :return: True if this and other vector are perpendicular, False otherwise
        """
        self.logger.info("Checking if vectors are perpendicular")
        # Check if the other is Vector
        if isinstance(other, Vector):
            # Return True if dot product of vector and the other is zero
            return self.dot(other) == 0
        else:
            # Raise an error if the other is not a vector
            self.logger.error("Data must be Vector type")
            raise ValueError("Data must be Vector type")

    def is_non_parallel(self, other: Vector) -> bool:
        """
        Checks if two vectors are neither parallel nor perpendicular

        >>> v = Vector(Point(1, 0, 0))
        >>> v2 = Vector(Point(0, 1, 0))
        >>> v3 = Vector(Point(1, 1, 0))
        >>> v.is_non_parallel(v2)
        False
        >>> v.is_non_parallel(v3)
        True


        :param other: Other vector to check
        :return: True if this and other vector are not parallel, False otherwise
        """
        self.logger.info("Checking if vectors are non-parallel")
        # Check if the other is Vector
        if isinstance(other, Vector):
            # Return True if vector and other is not parallel
            return not (self.is_parallel(other) or self.is_perpendicular(other))
        else:
            # Raise an error if the other is not a vector
            self.logger.error("Data must be Vector type")
            raise ValueError("Data must be Vector type")

    def rotate_about(self, other: Vector, angle: float) -> Vector:
        """
        Rotates the vector around other one by given angle

        >>> v = Vector(Point(1, 0, 0))
        >>> v2 = Vector(Point(0, 1, 0))
        >>> v.rotate_about(v2, 90)
        Vector(Point(x=6.123233995736766e-17, y=0.0, z=-1.0))


        :param other: The vector to rotate this around
        :param angle: Rotation amount

        :return: The rotated vector
        """
        angle = math.radians(angle)
        return self * math.cos(angle) + (other * self) * math.sin(angle) + other * other.dot(self) * (
                    1 - math.cos(angle))

    def rotate(self, alpha: float = 0, beta: float = 0, gamma: float = 0) -> Vector:
        """
        Rotates the vector around x, y or z axis by given amount

        >>> v = Vector(Point(1, 1, 1))
        >>> v.rotate(alpha=180, beta=0, gamma=0)
        Vector(Point(x=1.0, y=-1.0000000000000002, z=-0.9999999999999999))


        :param alpha: Rotation quantity around x axis
        :param beta: Rotation quantity around y axis
        :param gamma: Rotation quantity around z axis

        :return: The rotated vector
        """
        self.logger.info("Rotating Vector")
        # From https://stackoverflow.com/a/14609567/2681662

        # Check if alpha, beta and gamma are float or int (in short if it's numeric)
        if isinstance(alpha, (int, float)) and isinstance(beta, (int, float)) and isinstance(gamma, (int, float)):
            # Convert angles from degrees to radians
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
            # Raise an error if alpha, beta or gamma is not numeric
            self.logger.error("Angle must be numeric type")
            raise ValueError("Angle must be numeric type")
