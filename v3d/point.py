from __future__ import annotations

from logging import getLogger
from logging import Logger

import math


class Point:
    logger = getLogger('dummy')

    def __init__(self, x: float = 0, y: float = 0, z: float = 0, logger: Logger = None) -> None:
        """
        Constructor method
        >>> Point()
        Point(x=0, y=0, z=0)

        >>> Point(1, 1, 1)
        Point(x=1, y=1, z=1)


        :param x: X value of a 3D Point. 0 by default
        :param y: Y value of a 3D Point. 0 by default
        :param z: Z value of a 3D Point. 0 by default
        :param logger: Logger to log
        """
        if logger is not None:
            self.logger = logger

        # Set given x, y and z values for global usage
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        # From https://github.com/allelos/vectors/blob/master/vectors/vectors.py
        return f"{self.__class__.__name__}(x={self.x}, y={self.y}, z={self.z})"

    # From https://docs.python.org/3/library/operator.html
    def __sub__(self, other) -> Point:
        # Call self.subtract on a - b
        return self.subtract(other)

    def __add__(self, other) -> Point:
        # Call self.add on a + b
        return self.add(other)

    def __neg__(self) -> Point:
        # Change x, y and z's sign on -a
        return Point(x=-self.x, y=-self.y, z=-self.z, logger=self.logger)

    def __mul__(self, scalar: float) -> Point:
        # Call self.scale on a * b
        return self.scale(scalar)

    def __rmul__(self, scalar: float) -> Point:
        # Call self.scale on b * a
        return self.scale(scalar)

    def __truediv__(self, scalar: float) -> Point:
        # Call self.divide on a / b
        return self.divide(scalar)

    def __eq__(self, other: Point) -> bool:
        # Call self.is_same on a == b
        return self.is_same(other)

    def copy(self) -> Point:
        """
        Makes a copy of the given point

        >>> p = Point(1, 1, 1)
        >>> p2 = p.copy()
        >>> p2
        Point(x=1, y=1, z=1)


        :return: The copied Point
        """
        return Point(x=self.x, y=self.y, z=self.z, logger=self.logger)

    def divide(self, scalar: float) -> Point:
        """
        Returns a down scaled point

        >>> p = Point(2, 2, 2)
        >>> p.divide(2)
        Point(x=1.0, y=1.0, z=1.0)


        :param scalar: Scalar to down scale
        :return: The new down scaled Point
        """
        # Raise an error if scalar is zero
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        # Call self.scale for 1/scalar
        self.logger.info("Calling Point.scale")
        return self.scale(1 / scalar)

    def to_polar(self) -> tuple:
        """
        Returns Polar coordinates of the point

        >>> p = Point(1, 1, 1)
        >>> p.to_polar()
        (1.7320508075688772, 54.735610317245346, 45.0)


        :return: tuple of r, theta and phi
        """
        self.logger.info("Converting from cartesian to polar")
        # Calculate distance from zero point. It will be the radius of the polar coordinate
        r = self.dist()
        # If r is zero no need to calculate angles.
        if r == 0:
            return 0, 0, 0

        # Normal cartesian to polar conversion
        phi = math.atan2(self.y, self.x)
        theta = math.acos(self.z / r)
        return r, math.degrees(theta), math.degrees(phi)

    def scale(self, scalar: float) -> Point:
        """
        Returns an up scaled point

        >>> p = Point(1, 1, 1)
        >>> p.scale(2)
        Point(x=2, y=2, z=2)


        :param scalar: Scalar to up scale
        :return: The new up scaled Point
        """
        self.logger.info("Scaling the {}".format(self))
        # If scalar is float or int (in short if it's numeric)
        if isinstance(scalar, (int, float)):
            # Multiply each x, y and z values by scalar.
            return Point(x=self.x * scalar,
                         y=self.y * scalar,
                         z=self.z * scalar, logger=self.logger)
        else:
            # Raise an error if scalar is not numeric
            self.logger.error("Scalar must be float or int type")
            raise ValueError("Scalar must be float or int type")

    def subtract(self, other: Point) -> Point:
        """
        Return subtraction of two points

        >>> p = Point(1, 2, 3)
        >>> p2 = Point(1, 1, 1)
        >>> p.subtract(p2)
        Point(x=0, y=1, z=2)


        :param other: The point to subtract from this point
        :return: The subtraction result as a Point
        """
        self.logger.info("Calling Point.add")
        # Call add with negative value of other point
        return self.add(-other)

    def add(self, other: Point) -> Point:
        """
        Return addition of two points

        >>> p = Point(1, 2, 3)
        >>> p2 = Point(1, 1, 1)
        >>> p.add(p2)
        Point(x=2, y=3, z=4)


        :param other: The point to add to this point
        :return: The addition result as a Point
        """
        self.logger.info(f"Calculating {self} + {other}")
        # Check if the other is a Point
        if isinstance(other, Point):
            # Add other's x, y and z values to Point's each x, y and z values.
            return Point(x=self.x + other.x,
                         y=self.y + other.y,
                         z=self.z + other.z, logger=self.logger)

        else:
            # Raise an error if other is not a Point
            self.logger.error("Data must be a Point type")
            raise ValueError("Data must be a Point type")

    def dist(self, other: Point = None) -> float:
        """
        Returns distance between two Points if the other is given.
        Returns distance from origin if the other is not given

        >>> p = Point(2, 2, 2)
        >>> p2 = Point(1, 1, 1)
        >>> p.dist()
        3.4641016151377544
        >>> p.dist(p2)
        1.7320508075688772


        :param other: Point to calculate distance between this point.
        :return: The distance
        """
        self.logger.info("Calculating distance between {} and {}".format(self, other))
        # Check if the other is None.
        # If it is create a zero point and assign it to other.
        # This way if other is not given, distance from origin will be calculated.
        # Can be used for magnitude calculation
        if other is None:
            other = Point(logger=self.logger)

        # Check if other is a Point
        if isinstance(other, Point):
            # Calculate r for 3D.
            # r^2 = (x1 - x2)^2 + (y1 - y2)^2 + (z1 - z2)^2
            return math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2) +
                             math.pow(self.z - other.z, 2))
        else:
            # Raise an error if other is not a Point
            self.logger.error("Data must be Point type")
            raise ValueError("Data must be Point type")

    def is_same(self, other: Point, tolerance: float = 0.0001) -> bool:
        """
        Checks if two points are the same.
        One cannot check if two points are exactly the same, since x, y and z values are floats.

        >>> p = Point(1, 1, 1)
        >>> p2 = Point(1, 1, 1)
        >>> p3 = Point(1, 1, 2)
        >>> p.is_same(p2)
        True
        >>> p.is_same(p3)
        False


        :param other: The other Point to compair with this.
        :param tolerance: Tolerance for equality
        :return: True if the two points are the same, False if otherwise.
        """
        self.logger.info(f"Checking if {self} and {other} are same points")
        # Check if other is a Point
        if isinstance(other, Point):
            # Check if each element of each Point is equal to each element of other
            return abs(self.x - other.x) < tolerance and abs(self.y - other.y) < tolerance and\
                   abs(self.z - other.z) < tolerance
        else:
            # Raise an error if other is not a Point
            self.logger.error("Data must be Point type")
            raise ValueError("Data must be Point type")

    @classmethod
    def from_polar(cls, r: float, theta: float, phi: float) -> Point:
        """
        Returns a point from given polar values.

        >>> Point.from_polar(1.7320508075688772, 54.735610317245346, 45.0)
        Point(x=1.0, y=0.9999999999999998, z=0.9999999999999999)


        :param r: Distance from origin
        :param theta: Theta angle
        :param phi: Phi angle
        :return: The created Point
        """
        cls.logger.info("Calculating polar to cartesian")
        # Check if r, theta and phi are float or it (in short if they're numeric)
        if isinstance(r, (int, float)) and isinstance(theta, (int, float)) and isinstance(phi, (int, float)):
            # Convert from degrees to radians
            theta = math.radians(theta)
            phi = math.radians(phi)

            # Jacobian x, y and z calculation
            x = r * math.sin(theta) * math.cos(phi)
            y = r * math.sin(theta) * math.sin(phi)
            z = r * math.cos(theta)

            return Point(x=x, y=y, z=z, logger=cls.logger)
        else:
            # Raise an error if r, theta or phi is not numeric
            cls.logger.error("Data must be numeric type")
            raise ValueError("Data must be numeric type")
