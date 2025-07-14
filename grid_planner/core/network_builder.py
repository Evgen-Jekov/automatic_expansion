"""
network_builder.py

Contains the create_initial_network() function, which returns the basic pandapower network.

The network is created programmatically (without .json) to conveniently run simulations, change the structure and test algorithms.
"""
import pandapower as pp
import random

def generate_network(n_buses=10, n_loads=4, n_gens=2, n_ext_grids=1, seed=None):
    if seed is not None:
        random.seed(seed)

    net = pp.create_empty_network()

    buses = [pp.create_bus(net, vn_kv=20.0, name=f"Bus {i}") for i in range(n_buses)]

    connected = set([buses[0]])
    remaining = set(buses[1:])
    while remaining:
        from_bus = random.choice(list(connected))
        to_bus = random.choice(list(remaining))
        pp.create_line_from_parameters(net, from_bus, to_bus, length_km=2.0,
                                       r_ohm_per_km=0.4, x_ohm_per_km=0.12,
                                       c_nf_per_km=210, max_i_ka=0.25)
        connected.add(to_bus)
        remaining.remove(to_bus)

    for _ in range(max(0, n_buses // 2 - 1)):
        from_bus, to_bus = random.sample(buses, 2)
        if not any((net.line.from_bus[i] == from_bus and net.line.to_bus[i] == to_bus) or
                   (net.line.from_bus[i] == to_bus and net.line.to_bus[i] == from_bus)
                   for i in net.line.index):
            pp.create_line_from_parameters(net, from_bus, to_bus, length_km=1.5,
                                           r_ohm_per_km=0.4, x_ohm_per_km=0.12,
                                           c_nf_per_km=210, max_i_ka=0.25)

    ext_buses = random.sample(buses, min(n_ext_grids, len(buses)))
    for bus in ext_buses:
        pp.create_ext_grid(net, bus, vm_pu=1.02)

    gen_candidates = [b for b in buses if b not in ext_buses]
    random.shuffle(gen_candidates)
    for i in range(min(n_gens, len(gen_candidates))):
        p_mw = round(random.uniform(0.3, 1.5), 2)  # Типичные значения для распределённой генерации
        min_p = round(p_mw * 0.2, 2)
        max_p = round(p_mw * 1.2, 2)
        cost = round(random.uniform(30, 80), 2)  # €/MWh — реальный диапазон в Германии
        gen_idx = pp.create_gen(net, gen_candidates[i], p_mw=p_mw, vm_pu=1.01,
                                min_p_mw=min_p, max_p_mw=max_p)
        pp.create_poly_cost(net, gen_idx, 'gen', cp1_eur_per_mw=cost)

    load_buses = random.sample(buses, min(n_loads, len(buses)))
    for bus in load_buses:
        pp.create_load(net, bus,
                       p_mw=round(random.uniform(0.1, 1.5), 2),
                       q_mvar=round(random.uniform(0.02, 0.3), 2))

    try:
        pp.runpp(net, max_iteration=20, tolerance_mva=1e-6)
    except pp.LoadflowNotConverged:
        return None

    try:
        pp.runopp(net)
    except:
        return None

    return net


