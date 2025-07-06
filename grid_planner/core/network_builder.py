"""
network_builder.py

Contains the create_initial_network() function, which returns the basic pandapower network.

The network is created programmatically (without .json) to conveniently run simulations, change the structure and test algorithms.
"""

import pandapower as pp
import random

def create_network(n_buses=200, n_lines=None, seed=None):
    if seed is not None:
        random.seed(seed)

    net = pp.create_empty_network()
    buses = []

    for i in range(n_buses):
        vn_kv = random.choice([20, 35, 110, 220])
        bus = pp.create_bus(net, vn_kv=vn_kv, name=f"Bus {i}")
        buses.append(bus)

    for _ in range(random.randint(1, 3)):
        pp.create_ext_grid(
            net,
            bus=random.choice(buses),
            vm_pu=random.uniform(0.98, 1.03),
            name="Ext Grid"
        )

    for _ in range(int(n_buses * random.uniform(0.1, 0.2))):
        pp.create_sgen(
            net,
            bus=random.choice(buses),
            p_mw=random.uniform(5, 50),
            q_mvar=random.uniform(-5, 5)
        )

    for _ in range(int(n_buses * random.uniform(0.2, 0.4))):
        pp.create_load(
            net,
            bus=random.choice(buses),
            p_mw=random.uniform(5, 100),
            q_mvar=random.uniform(0, 30)
        )

    if n_lines is None:
        n_lines = int(n_buses * 1.5)

    possible_pairs = [(i, j) for i in range(n_buses) for j in range(i+1, n_buses)]
    random.shuffle(possible_pairs)

    for i in range(min(n_lines, len(possible_pairs))):
        from_bus, to_bus = possible_pairs[i]
        pp.create_line_from_parameters(
            net,
            from_bus=buses[from_bus],
            to_bus=buses[to_bus],
            length_km=random.uniform(1, 15),
            r_ohm_per_km=random.uniform(0.01, 0.1),
            x_ohm_per_km=random.uniform(0.01, 0.08),
            c_nf_per_km=random.uniform(5, 20),
            max_i_ka=random.uniform(0.5, 2),
            name=f"Line {from_bus}-{to_bus}",
            type="ol"
        )

    return net