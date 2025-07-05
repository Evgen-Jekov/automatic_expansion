"""
graph_optimizer.py

Implementation of the discrete optimization problem via PySCIPOpt:
- creation of binary variables (each measure is 0/1),
- setting constraints (e.g. no more than 3 measures),
- call solve(),
- interaction with pandapower (via external functions).

This is the main file if you use SCIP as a solver.
"""