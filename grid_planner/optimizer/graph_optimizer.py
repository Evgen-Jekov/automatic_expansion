"""
graph_optimizer.py

Implementation of the discrete optimization problem via PySCIPOpt:
- creation of binary variables (each measure is 0/1),
- setting constraints (e.g. no more than 3 measures),
- call solve(),
- interaction with pandapower (via external functions).

This is the main file if you use SCIP as a solver.
"""
import pandapower as pp

def optimize_network(net, max_iter=100):
    pp.runpp(net)

    for _ in range(max_iter):
        lines_to_disable = []
        for idx, row in net.res_line.iterrows():
            if abs(row.i_from_ka) < 0.05 and abs(row.i_to_ka) < 0.05:
                lines_to_disable.append(idx)

        if not lines_to_disable:
            break

        net_temp = net.deepcopy()
        net_temp.line.drop(lines_to_disable, inplace=True)

        if len(pp.topology.connected_components(net_temp)) == 1:
            net.line.drop(lines_to_disable, inplace=True)
            pp.runpp(net)

    return net