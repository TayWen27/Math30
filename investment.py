import numpy as np
import matplotlib.pyplot as plt

# === Base Parameters ===
Tf_base = 8  # Fast mover enters at month 8
fast_init_investment = 10000
a = 0.8  # Growth rate of reputation
M = 1000  # Market size
dt = 0.05
timesteps = int(36 / dt)  # Simulate for 3 years
epsilon = 1e-3

# === Vary these ===
entry_advantages = list(range(0, 19, 3))  # [0, 3, 6, ..., 18]
slow_investments = [10000, 20000]  # Try multiple slow investment values

# === Define replicator dynamic function ===
def replicator_dx(x, t_month, Tf, Ts, fast_I, slow_I):
    Rf = fast_I * np.exp(a * (t_month - Tf)) #To make initial investment matter, reputation must scale with time since entry, not with current market share.
    Rs = slow_I * np.exp(a *  (t_month - Ts))
    Pf = Rf / (Rf + Rs)
    Ff = Pf * M
    Fs = (1 - Pf) * M
    delta_f = Ff - Fs
    return x * (1 - x) * delta_f

# === Run simulations ===
plt.figure(figsize=(10, 6))

all_final_props = {}

for slow_I in slow_investments:
    final_props = []

    for advantage in entry_advantages:
        Tf = Tf_base
        Ts = Tf_base + advantage
        x = 0.2  # Initial proportion of fast mover

        for t in range(timesteps):
            t_month = t * dt
            dx = replicator_dx(x, t_month, Tf, Ts, fast_init_investment, slow_I)
            x += dx * dt
            x = np.clip(x, epsilon, 1 - epsilon)

        final_props.append(x)

    all_final_props[slow_I] = final_props
    plt.plot(entry_advantages, final_props, marker='o', label=f"Slow Init Invest = {slow_I}")

# Debug print to confirm different values
for slow_I, props in all_final_props.items():
    print(f"Slow Investment = {slow_I}, Final Proportions = {props}")

# === Final plot formatting ===
plt.axhline(0.5, color='gray', linestyle='--', label='Neutral Share')
plt.xlabel("Entry Advantage (months): Slow − Fast")
plt.ylabel("Final Proportion of Fast Mover")
plt.title("Effect of Slow Mover Investment on Final Market Share")
plt.legend(title="Slow Investment")
plt.grid(True)
plt.xticks(entry_advantages)
plt.tight_layout()
plt.show()
