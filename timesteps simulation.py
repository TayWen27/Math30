import numpy as np
import matplotlib.pyplot as plt

# === Base Parameters ===
Tf_base = 8  # Fast mover entry time
fast_init_investment = 10000
slow_init_investment = 10000
M = 1000  # Market size
a = 0.5  # Reputation growth rate
epsilon = 1e-3
x0 = 0.5  # Initial proportion of fast mover
entry_advantages = list(range(0, 25, 3))  # Ts - Tf
simulation_months_list = [6, 12, 36]  # Durations to simulate

# === Replicator dynamic function ===
def replicator_dx(x, t_month, Tf, Ts, fast_I, slow_I, a):
    Rf = fast_I * np.exp(a * x * (t_month - Tf)) / (1 + 0.05 * (t_month - Tf))
    Rs = slow_I * np.exp(a * (1 - x) * (t_month - Ts)) / (1 + 0.05 * (t_month - Ts))
    Pf = Rf / (Rf + Rs)
    Ff = Pf * M
    Fs = (1 - Pf) * M
    delta_f = Ff - Fs
    return x * (1 - x) * delta_f

# === Plotting ===
plt.figure(figsize=(10, 6))
styles = ['-', '--', '-.']
markers = ['o', 's', 'D']

for i, sim_months in enumerate(simulation_months_list):
    dt = 0.05
    timesteps = int(sim_months / dt)
    final_props = []

    print(f"\nSimulation duration: {sim_months} months")

    for adv in entry_advantages:
        Tf = Tf_base
        Ts = Tf_base + adv
        x = x0
        x_vals = []  # Track x over time

        for t in range(timesteps):
            t_month = t * dt
            dx = replicator_dx(x, t_month, Tf, Ts, fast_init_investment, slow_init_investment, a)
            x += dx * dt
            x = np.clip(x, epsilon, 1 - epsilon)
            x_vals.append(x)

        final_props.append(x)
        print(f"  Entry advantage = {adv} months, Final x = {x:.4f}, Max x = {max(x_vals):.4f}, Min x = {min(x_vals):.4f}")

    plt.plot(entry_advantages, final_props,
             marker=markers[i], linestyle=styles[i], linewidth=2,
             label=f"{sim_months} months")

# === Final plot formatting ===
plt.axhline(0.5, color='gray', linestyle='--', label='Neutral Share')
plt.xlabel("Entry Advantage (Ts − Tf) in Months")
plt.ylabel("Final Proportion of Fast Mover")
plt.title("Final Market Share vs. Entry Advantage (a = 0.8)")
plt.legend(title="Simulation Duration")
plt.grid(True)
plt.xticks(entry_advantages)
plt.tight_layout()
plt.show()
