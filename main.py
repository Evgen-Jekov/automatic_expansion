"""
main.py

Main entry to the project.
1. Creates a basic network using network_builder
2. Runs optimization
3. Outputs/saves results

Run:
python main.py
"""

from grid_planner.core.network_builder import generate_network
from pandapower.plotting import simple_plot
import pandapower as pp

net = generate_network(n_buses=100, n_loads=10, n_gens=5, n_ext_grids=1)
pp.runopp(net=net)

simple_plot(net=net)

