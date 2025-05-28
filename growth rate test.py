import numpy as np
import matplotlib.pyplot as plt

# === Base Parameters ===
Tf_base = 8  # Fast mover enters at month 8
fast_init_investment = 10000
slow_init_investment = 15000
M = 1000  # Market size
dt = 0.05
timesteps = int(36 / dt)  # Simulate for 3 years
epsilon = 1e-3
x0 = 0.2  # Initial proportion of fast mover

# === Experiment Parameters ===
entry_advantages = list(range(0, 19, 3))  # [0, 3, ..., 18]
growth_rates = [0.2, 0.8]  # Different values of a

# === Define replicator dynamic function ===
def replicator_dx(x, t_month, Tf, Ts, fast_I, slow_I, a):
    Rf = fast_I * np.exp(a * x * (t_month - Tf))
    Rs = slow_I * np.exp(a * (1 - x) * (t_month - Ts))
    Pf = Rf / (Rf + Rs)
    Ff = Pf * M
    Fs = (1 - Pf) * M
    delta_f = Ff - Fs
    return x * (1 - x) * delta_f

# === Run simulations ===
plt.figure(figsize=(10, 6))

for a in growth_rates:
    final_props = []

    for advantage in entry_advantages:
        Tf = Tf_base
        Ts = Tf_base + advantage
        x = x0

        for t in range(timesteps):
            t_month = t * dt
            dx = replicator_dx(x, t_month, Tf, Ts, fast_init_investment, slow_init_investment, a)
            x += dx * dt
            x = np.clip(x, epsilon, 1 - epsilon)

        final_props.append(x)

    # Plot result for this growth rate
    plt.plot(entry_advantages, final_props, marker='o', label=f"Growth Rate a = {a}")

# === Final plot formatting ===
plt.axhline(0.5, color='gray', linestyle='--', label='Neutral Share')
plt.xlabel("Entry Advantage (months): Slow − Fast")
plt.ylabel("Final Proportion of Fast Mover")
plt.title("Effect of Growth Rate on Final Market Share")
plt.legend(title="Growth Rate a")
plt.grid(True)
plt.xticks(entry_advantages)
plt.tight_layout()
plt.show()
