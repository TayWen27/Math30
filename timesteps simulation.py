import numpy as np
import matplotlib.pyplot as plt

# === Simulation Parameters ===
Tf_base = 8  # Fast mover entry time (months)
fast_init_investment = 10000
slow_init_investment = 10000
a = 0.8  # Reputation growth rate
M = 1000  # Total market size
dt = 0.05  # Time step in months
epsilon = 1e-3  # Boundary constraint for replicator dynamics

# Simulate for different total durations
simulation_months_list = [1, 6, 18]
entry_advantages = list(range(0, 19, 3))  # [0, 3, ..., 18]

# === Define replicator dynamic function ===
def replicator_dx(x, t_month, Tf, Ts):
    Rf = fast_init_investment * np.exp(a * x * (t_month - Tf))
    Rs = slow_init_investment * np.exp(a * (1 - x) * (t_month - Ts))
    Pf = Rf / (Rf + Rs)
    Ff = Pf * M
    Fs = (1 - Pf) * M
    delta_f = Ff - Fs
    return x * (1 - x) * delta_f

# === Run simulations ===
plt.figure(figsize=(10, 6))
for duration in simulation_months_list:
    timesteps = int(duration / dt)
    final_props = []

    for advantage in entry_advantages:
        Tf = Tf_base
        Ts = Tf_base + advantage
        x = 0.2

        for t in range(timesteps):
            t_month = t * dt
            dx = replicator_dx(x, t_month, Tf, Ts)
            x += dx * dt
            x = np.clip(x, epsilon, 1 - epsilon)

        final_props.append(x)

    plt.plot(entry_advantages, final_props, marker='o', label=f'{duration}-Month Simulation')

# === Plot Formatting ===
plt.axhline(0.5, color='gray', linestyle='--', label='Neutral Share')
plt.xlabel("Entry Advantage (months): Slow − Fast")
plt.ylabel("Final Proportion of Fast Mover")
plt.title("Impact of Entry Advantage on Market Share (Varying Simulation Durations)")
plt.legend()
plt.grid(True)
plt.xticks(entry_advantages)
plt.tight_layout()
plt.show()
