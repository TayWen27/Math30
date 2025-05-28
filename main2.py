import numpy as np
import matplotlib.pyplot as plt

# === Simulation Parameters ===
Tf_base = 8  # Fast mover entry time (months)
fast_init_investment = 10000
slow_init_investment = 10000
a = 0.8  # Reputation growth rate
M = 1000  # Total market size
dt = 0.05  # Time step in months
timesteps = int(36 / dt)  # Simulate 36 months
epsilon = 1e-3  # Boundary constraint for replicator dynamics

# Varying entry delay of the slow mover relative to the fast mover
entry_advantages = list(range(0, 19, 3))  # [0, 3, 6, ..., 18] months
entry_diff_results = []

# === Define replicator dynamic function ===
def replicator_dx(x, t_month, Tf, Ts):
    Rf = fast_init_investment * np.exp(a * x* (t_month - Tf))
    Rs = slow_init_investment * np.exp(a * (1-x)*(t_month - Ts))
    Pf = Rf / (Rf + Rs)
    Ff = Pf * M
    Fs = (1 - Pf) * M
    delta_f = Ff - Fs
    return x * (1 - x) * delta_f

# === Run simulation for each entry gap ===
for advantage in entry_advantages:
    Tf = Tf_base
    Ts = Tf_base + advantage  # Slow mover enters later
    x = 0.2  # Initial proportion of fast mover
    x_vals = []

    for t in range(timesteps):
        t_month = t * dt
        dx = replicator_dx(x, t_month, Tf, Ts)
        x_vals.append(x)
        x += dx * dt
        x = np.clip(x, epsilon, 1 - epsilon)

    entry_diff_results.append((advantage, x_vals[-1]))

# === Process and Plot Results ===
deltas, final_props = zip(*entry_diff_results)

plt.figure(figsize=(10, 6))
plt.plot(deltas, final_props, marker='o', label='Simulated Final Proportion (Fast Mover)')
plt.axhline(0.5, color='gray', linestyle='--', label='Neutral Share')

plt.xlabel("Entry Advantage (months): Slow − Fast")
plt.ylabel("Final Proportion of Fast Mover")
plt.title("Impact of Entry Advantage on Market Share (3-Year Simulation)")
plt.legend()
plt.grid(True)
plt.xticks(entry_advantages)
plt.tight_layout()
plt.show()
