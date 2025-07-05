"""
constraint_checker.py

Checks if the network meets technical constraints:
- voltages are within the acceptable range (e.g. 0.95–1.05 pu),
- no transformer or line overload,
- topology is acceptable (e.g. network remains connected and radial).

Returns a boolean value or a list of violations.
"""