# -*- coding: utf-8 -*-
"""
@author: Mohammad Shameoni Niaei
inspired by: https://github.com/allelos/vectors
Thanks to: https://github.com/allelos/
"""
from logging import getLogger

import math


class Point:
    def __init__(self, x=0, y=0, z=0, logger=None):
        # From https://stackoverflow.com/questions/13521981/implementing-an-optional-logger-in-code
        self.logger = logger or getLogger('dummy')
        # Set given x, y and z values for global usage
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        # From https://github.com/allelos/vectors/blob/master/vectors/vectors.py
        return "{}(x={}, y={}, z={})".format(self.__class__.__name__, self.x, self.y, self.z)

    # From https://docs.python.org/3/library/operator.html
    def __sub__(self, other):
        # Call self.subtract on a - b
        return self.subtract(other)

    def __add__(self, other):
        # Call self.add on a + b
        return self.add(other)

    def __neg__(self):
        # Change x, y and z's sign on -a
        return Point(x=-self.x, y=-self.y, z=-self.z, logger=self.logger)

    def __mul__(self, scalar):
        # Call self.scale on a * b
        return self.scale(scalar)

    def __rmul__(self, scalar):
        # Call self.scale on b * a
        return self.scale(scalar)

    def __truediv__(self, scalar):
        # Call self.divide on a / b
        return self.divide(scalar)

    def __eq__(self, other):
        # Call self.is_same on a == b
        return self.is_same(other)

    def copy(self):
        # Make a copy of point and return it
        return Point(x=self.x, y=self.y, z=self.z, logger=self.logger)

    def divide(self, scalar):
        # Raise an error if scalar is zero
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        # Call self.scale for 1/scalar
        self.logger.info("Calling Point.scale")
        return self.scale(1 / scalar)

    def to_polar(self):
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

    def scale(self, scalar):
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

    def subtract(self, other):
        self.logger.info("Calling Point.add")
        # Call add with negative value of other point
        return self.add(-other)

    def add(self, other):
        self.logger.info("Calculating {} + {}".format(self, other))
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

    def dist(self, other=None):
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

    def is_same(self, other):
        self.logger.info("Checking if {} and {} are same points".format(self, other))
        # Check if other is a Point
        if isinstance(other, Point):
            # Check if each element of each Point is equal to each element of other
            return self.x == other.x and self.y == other.y and self.z == other.z
        else:
            # Raise an error if other is not a Point
            self.logger.error("Data must be Point type")
            raise ValueError("Data must be Point type")

    def from_polar(self, r, theta, phi, override=True):
        self.logger.info("Calculating polar to cartesian")
        # Check if r, theta and phi are float or it (in short if they're numeric)
        if isinstance(r, (int, float)) and isinstance(theta, (int, float)) and isinstance(phi, (int, float)):
            # Convert from degrees to radians
            theta = math.radians(theta)
            phi = math.radians(phi)

            # Jacobian x, y and z calculation
            x = r * math.sin(theta) * math.cos(phi)
            y = r * math.sin(theta) * math.sin(phi)
            z = r * math.cos(theta)

            if override:
                # Change Point's values with new ones if override is enabled
                self.x = x
                self.y = y
                self.z = z
            else:
                # Return a new Point with new values if override is not enabled
                return Point(x=x, y=y, z=z, logger=self.logger)
        else:
            # Raise an error if r, theta or phi is not numeric
            self.logger.error("Data must be numeric type")
            raise ValueError("Data must be numeric type")


class Vector:
    def __init__(self, point=None, logger=None):
        # From https://stackoverflow.com/questions/13521981/implementing-an-optional-logger-in-code
        self.logger = logger or getLogger('dummy')

        # If the point is not given. Create a zero point and assign it to point
        if point is None:
            point = Point()

        # Check if point is a Point
        if isinstance(point, Point):
            # Set given point for global usage
            self.point = point
        else:
            # Set a new zero point for global usage
            self.point = Point(logger=self.logger)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        # From https://github.com/allelos/vectors/blob/master/vectors/vectors.py
        return "{}({})".format(self.__class__.__name__, self.point)

    # From https://docs.python.org/3/library/operator.html
    def __neg__(self):
        # Change sign of point on -a
        return Vector(-self.point, logger=self.logger)

    def __add__(self, other):
        # Call self.add on a + b
        return self.add(other)

    def __sub__(self, other):
        # Call self.subtract on a - b
        return self.subtract(other)

    def __mul__(self, other):
        # Call self.scale on a * b
        return self.multiply(other)

    def __rmul__(self, other):
        # Call self.scale on b * a
        return self.multiply(other)

    def __truediv__(self, scalar):
        # Call self.divide on a / b
        return self.divide(scalar)

    def __eq__(self, other):
        # Call self.is_same on a == b
        return self.is_same(other)

    def __abs__(self):
        # call self.mag of abs(a)
        return self.mag()

    def is_same(self, other):
        # Check if two Vector is same as other by checking
        # if points assigned to Vector and other are same.
        return self.point == other.point

    def from_points(self, point1, point2):
        self.logger.info("Creating vector from two points")
        # Check if point1 and point2 are Point
        if isinstance(point1, Point) and isinstance(point2, Point):
            # Assign Vector's Point ot point1 - point2
            self.point = point1 - point2
        else:
            # Raise an error if point1 or point2 is not Point
            self.logger.error("Data must be Point type")
            raise ValueError("Data must be Point type")

    def copy(self):
        # Make a copy of Vector by returning a new Vector
        # with a copy of this.point is assigned as Point
        return Vector(self.point.copy(), logger=self.logger)

    def dot(self, other):
        self.logger.info("Calculating dot product of {} and {}".format(self, other))
        # Check if the other is a Vector
        if isinstance(other, Vector):
            # Calculate and return dot product of two vectors
            return self.point.x * other.point.x + self.point.y * other.point.y + self.point.z * other.point.z
        else:
            # Raise an error if the other is not a Vector
            self.logger.error("Data must be Vector type")
            raise ValueError("Data must be Vector type")

    def multiply(self, other):
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

    def mag(self):
        self.logger.info("Calling Point.dist")
        # Calls self.point's dist method
        return self.point.dist()

    def divide(self, other):
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

    def add(self, other):
        self.logger.info("Calculating {} + {}".format(self, other))
        # Check if other is a Vector
        if isinstance(other, Vector):
            # Return a new Vector with point as sum of this and other's points
            return Vector(self.point + other.point, logger=self.logger)
        else:
            # Raise and error if other is not a Vector
            self.logger.error("Data must be Vector type")
            raise ValueError("Data must be Vector type")

    def subtract(self, other):
        self.logger.info("Calling Vector.add")
        # Call add with negative value of other vector
        return self.add(-other)

    def heading(self):
        self.logger.info("Calculating Heading")
        # Calculate Magnitude of Vector
        r = self.mag()
        # Use Jacobian to calculate theta and phi
        phi = math.atan2(self.point.y, self.point.x)

        theta = math.acos(self.point.z / r)
        return math.degrees(theta), math.degrees(phi)

    def unit(self):
        self.logger.info("Calculating unit vector of {}".format(self))
        # Divide self with magnitude and return as a new vector
        m = self.mag()
        return Vector(self.point / m, logger=self.logger)

    def angle_between(self, other):
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

    def as_plt(self):
        # Returns a dictionary for plotting with matplotlib
        return {"x": [0, self.point.x], "y": [0, self.point.y], "z": [0, self.point.z]}

    def normal(self, other):
        self.logger.info("calculating Normal Vector")
        # Check if other is a Vector
        if isinstance(other, Vector):
            # Return unit vector of cross product of Vector and other
            nrm = self * Vector
            return nrm.unit()
        else:
            # Raise an error if other is not a Vector
            self.logger.error("Data must be Vector type")
            raise ValueError("Data must be Vector type")

    def is_parallel(self, other):
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

    def is_perpendicular(self, other):
        self.logger.info("Checking if vectors are perpendicular")
        # Check if the other is Vector
        if isinstance(other, Vector):
            # Return True if dot product of vector and the other is zero
            return self.dot(other) == 0
        else:
            # Raise an error if the other is not a vector
            self.logger.error("Data must be Vector type")
            raise ValueError("Data must be Vector type")

    def is_non_parallel(self, other):
        self.logger.info("Checking if vectors are non-parallel")
        # Check if the other is Vector
        if isinstance(other, Vector):
            # Return True if vector and other is not parallel
            return not (self.is_parallel(other) or self.is_perpendicular(other))
        else:
            # Raise an error if the other is not a vector
            self.logger.error("Data must be Vector type")
            raise ValueError("Data must be Vector type")

    def rotate_about(self, other, angle):
        angle = math.radians(angle)
        return self * math.cos(angle) + (other * self) * math.sin(angle) + other * other.dot(self) * (1 - math.cos(angle))

    def rotate(self, alpha=0, beta=0, gamma=0):
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
