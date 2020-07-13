# v3d
v3d (Stands for Vector 3D) is a 3D vector library for basic Vector operations.
It was inspired by: https://github.com/allelos/vectors

## WHY?
The a library was created by https://github.com/allelos/. However there was some missing parts(such as from_mag_and_dir).

## Installation

```bash
pip install v3d
```
## Documentation
### Concept
This work inspired by https://github.com/allelos/vectors

V3D has no dependency other than standard math module.

It consists of two parts, Point and Vector.

A point is a class with multiple operations. It is also a data carrier for Vector.

Vector is a module with multiple operations.

### Point
Creating a Point:
```python3
from v3d import Vector, Point

p1 = Point()# This will create a zero point. (0, 0, 0)
p2 = Point(1, 3, 1)# This will create a point at (1, 3, 1)
```
Converting between Polar and Cartesian:
```python3
p2.to_polar()# r, theta, phi (angles are in degrees)
# (3.3166247903554, 72.4515993862077, 71.56505117707799)
p1.from_polar(1, 45, 0)# Overrides p1 with new x,y and z. Set override to False to get a return
```
Add/Subtract:
```python3
#Add
p1.add(p2)
# Point(x=1.7071067811865475, y=3.0, z=1.7071067811865475)
p2.add(p1)
# Point(x=1.7071067811865475, y=3.0, z=1.7071067811865475)
p1 + p2
# Point(x=1.7071067811865475, y=3.0, z=1.7071067811865475)
p2 + p1
# Point(x=1.7071067811865475, y=3.0, z=1.7071067811865475)

#Subtract
p1.subtract(p2)
# Point(x=-0.29289321881345254, y=-3.0, z=-0.2928932188134524)
p1 - p2
# Point(x=-0.29289321881345254, y=-3.0, z=-0.2928932188134524)

p2.subtract(p1)
# Point(x=0.29289321881345254, y=3.0, z=0.2928932188134524)
p2 - p1
# Point(x=0.29289321881345254, y=3.0, z=0.2928932188134524)
```
Multiply/Divide
```python3
p2.scale(2)
# Point(x=2, y=6, z=2)
p2 * 2
# Point(x=2, y=6, z=2)

p2.divide(2)
# Point(x=0.5, y=1.5, z=0.5)
p2 / 2
# Point(x=0.5, y=1.5, z=0.5)
```
Other Operations:

```python3
# Distance from origin:
p1.dist()
# 1.0

# Distance from other point:
p1.dist(p2)
# 3.028460479394408

#Check if two point are the same:
p1.is_same(p2)
# False
p1 == p2
# False

# Notice we made a copy of p2 as p3
p3 = p2.copy()

p2.is_same(p3)
# True
p2 == p3
# True
```
### Vector
Creating a Vector:
```python3
# Notice p1 is a point type. It was created before.
v1 = Vector(p1)
# Vector(Point(x=0.7071067811865475, y=0.0, z=0.7071067811865476))
```

Magnitude, heading and unit vector:
```python3
v1.mag()
# 1.0
abs(v1)
# 1.0

v1.heading()
# (0.0, 45.0)
v1.unit()
# Vector(Point(x=0.7071067811865475, y=0.0, z=0.7071067811865476))
```
Rotate:
```python3
v1.rotate(alpha=45, beta=0, gamma=0)# alpha in x, beta in y and gamma in y axis
# Vector(Point(x=0.7071067811865475, y=-0.5, z=0.5000000000000001))
```
Add/Subtract:
```python3
# Creating a new vector from p2
v2 = Vector(p2)

v1.add(v2)
# Vector(Point(x=1.7071067811865475, y=3.0, z=1.7071067811865475))
v1 + v2
# Vector(Point(x=1.7071067811865475, y=3.0, z=1.7071067811865475))

v1.subtract(v2)
# Vector(Point(x=-0.29289321881345254, y=-3.0, z=-0.2928932188134524))
v1 - v2
# Vector(Point(x=-0.29289321881345254, y=-3.0, z=-0.2928932188134524))
```
Multiply:
```python3
v1.multiply(2)
# Vector(Point(x=1.414213562373095, y=0.0, z=1.4142135623730951))
v1 * 2
# Vector(Point(x=1.414213562373095, y=0.0, z=1.4142135623730951))

# In case of two vector multiplication cross product will be calculated.
v1.multiply(v2)
# Vector(Point(x=-2.121320343559643, y=1.1102230246251565e-16, z=2.1213203435596424))
v1 * v2
# Vector(Point(x=-2.121320343559643, y=1.1102230246251565e-16, z=2.1213203435596424))

v1.divide(2)
# Vector(Point(x=0.35355339059327373, y=0.0, z=0.3535533905932738))
v1 / 2
# Vector(Point(x=0.35355339059327373, y=0.0, z=0.3535533905932738))

# These two lines will rise an error. Vector by Vector division is not possible
v1.divide(v2)
v1 / v2
```

Dot product:
```python3
v1.dot(v2)
# 1.414213562373095
```
Other operations:
```python3
# Angle between two vectors
v1.angle_between(v2)
# 64.7605981793211

# Check if two vector are same
# Noice Points p2 and p3 are the same so will the vectors be
v3 = Vector(p3)
# False
v1.is_same(v2)
# False
v1 == v2
# False

# Noice Points p2 and p3 are the same so will the vectors be
v3 = Vector(p3)
# True
v2.is_same(v3)
# True
v2 == v3
# True


# Check if two vectors are perpendicular
#We know cross product of two vectors will be a vector perpendicular to other two vectors

cross_product = v1 * v2
cross_product.is_perpendicular(v1) and cross_product.is_perpendicular(v2)
# True

# Check if two vectors are parallel
#We know cross product of two vectors will be a vector perpendicular to other two vectors

cross_product.is_parallel(v1) or cross_product.is_parallel(v2)
# False

# Check if two vectors are non_parallel
#We know cross product of two vectors will be a vector perpendicular to other two vectors

cross_product.is_non_parallel(v1) and cross_product.is_non_parallel(v2)
#True

```

## Example

Example: https://github.com/mshemuni/V3D/blob/master/example.ipynb
