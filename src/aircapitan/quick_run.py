def quick_run(sim, components, duration_s, dt=0.010):
    # sim = sim
    while sim.sim_time_s < duration_s:
        sim.propagate(dt)
        for c in components:
            c.poke(sim.sim_time_s)
