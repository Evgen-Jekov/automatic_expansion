"""
measures.py

Contains the implementation of possible "measures" (actions) that can be applied to the network:
- line replacement (increase in cross-section),
- opening/closing of the switch,
- adding a parallel line,
- installing a new TP, etc.

Each measure is implemented by a separate function: apply_measure_xxx(net)
"""