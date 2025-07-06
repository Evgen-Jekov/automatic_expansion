"""
network_builder.py

Contains the create_initial_network() function, which returns the basic pandapower network.

The network is created programmatically (without .json) to conveniently run simulations, change the structure and test algorithms.
"""

import pandapower as pp
import random
import numpy as np


def create_network(n_buses=200, n_lines=None, seed=None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    net = pp.create_empty_network()
    buses = []

    for i in range(n_buses):
        vn_kv = random.choice([20, 35, 110, 220])
        bus = pp.create_bus(net, vn_kv=vn_kv, name=f"Bus {i}")
        buses.append(bus)

    ext_bus = random.choice(buses)
    pp.create_ext_grid(net, bus=ext_bus, vm_pu=1.02, name="Grid")

    for _ in range(int(n_buses * 0.15)):
        pp.create_sgen(net, bus=random.choice(buses), p_mw=random.uniform(5, 50), q_mvar=random.uniform(-5, 5))

    for _ in range(int(n_buses * 0.3)):
        pp.create_load(net, bus=random.choice(buses), p_mw=random.uniform(5, 100), q_mvar=random.uniform(0, 30))

    def add_min_spanning_tree(net, buses):
        n = len(buses)
        parent = [i for i in range(n)]

        def find(u):
            while parent[u] != u:
                parent[u] = parent[parent[u]]
                u = parent[u]
            return u

        def union(u, v):
            u_root = find(u)
            v_root = find(v)
            if u_root == v_root:
                return False
            parent[v_root] = u_root
            return True

        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                weight = random.uniform(1, 10)
                edges.append((i, j, weight))

        edges.sort(key=lambda x: x[2])

        tree_edges = []
        for u, v, w in edges:
            if union(u, v):
                tree_edges.append((u, v))
                if len(tree_edges) == n - 1:
                    break

        for u, v in tree_edges:
            from_bus = buses[u]
            to_bus = buses[v]
            vn_kv = net.bus.loc[from_bus, "vn_kv"]
            r = random.uniform(0.01, 0.1)
            x = random.uniform(0.01, 0.08)
            c = random.uniform(5, 20)
            max_i = random.uniform(0.5, 2)
            pp.create_line_from_parameters(
                net, from_bus, to_bus, length_km=10,
                r_ohm_per_km=r, x_ohm_per_km=x, c_nf_per_km=c, max_i_ka=max_i,
                name=f"Line {u}-{v}"
            )

    add_min_spanning_tree(net, buses)

    if n_lines is None:
        n_lines = n_buses // 2

    possible_pairs = [(i, j) for i in range(n_buses) for j in range(i + 1, n_buses)]
    random.shuffle(possible_pairs)

    for i in range(min(n_lines, len(possible_pairs))):
        u, v = possible_pairs[i]
        from_bus = buses[u]
        to_bus = buses[v]
        if not net.line[(net.line.from_bus == from_bus) & (net.line.to_bus == to_bus)].empty:
            continue
        vn_kv = net.bus.loc[from_bus, "vn_kv"]
        pp.create_line_from_parameters(
            net, from_bus, to_bus, length_km=random.uniform(1, 15),
            r_ohm_per_km=random.uniform(0.01, 0.1), x_ohm_per_km=random.uniform(0.01, 0.08),
            c_nf_per_km=random.uniform(5, 20), max_i_ka=random.uniform(0.5, 2),
            name=f"Line {u}-{v}"
        )

    return net