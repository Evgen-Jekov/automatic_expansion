"""
main.py

Main entry to the project.
1. Creates a basic network using network_builder
2. Runs optimization (SCIPO or heuristics)
3. Outputs/saves results

Run:
python main.py
"""

from grid_planner.core.network_builder import create_network
from grid_planner.optimizer.graph_optimizer import optimize_network
from pandapower.plotting import simple_plot

net = create_network()
simple_plot(net=net)
o_net = optimize_network(net=net)
simple_plot(net=net)
