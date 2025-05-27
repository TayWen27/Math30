import matplotlib.pyplot as plt
import numpy as np

# Time and Parameters
timesteps = 1000
dt = 0.01
simulation_time = np.arange(0, timesteps*dt, dt)

# Model parameters
Tf_base = 6  # baseline entry time for fast mover
Ts_base = 6  # baseline entry time for slow mover
fast_init_investment = 10000
slow_init_investment = 10000
a = 0.6  # growth rate
M = 100  # market value

# === 1. Entry Time Sensitivity Analysis ===
entry_diff_results = []

for delta in range(-6, 7):  # Vary Tf - Ts from -6 to 6
    Tf = Tf_base + delta
    Ts = Ts_base
    x = 0.5
    x_vals = []

    for t in range(timesteps):
        t_month = t * dt
        Rf = fast_init_investment * np.exp(a * x * (t_month - Tf)) - 1
        Rs = slow_init_investment * np.exp(a * (1 - x) * (t_month - Ts)) - 1
        Pf = Rf / (Rf + Rs)
        Ff = Pf * M
        Fs = (1 - Pf) * M
        delta_f = Ff - Fs
        dx = x * (1 - x) * delta_f
        x_vals.append(x)
        x += dx * dt
        x = np.clip(x, 0, 1)

    entry_diff_results.append((delta, x_vals[-1]))

deltas, final_props = zip(*entry_diff_results)
plt.figure(figsize=(8, 5))
plt.plot(deltas, final_props, marker='o')
plt.axhline(0.5, color='gray', linestyle='--')
plt.xlabel("Fast Mover Entry Time Advantage (Tf - Ts)")
plt.ylabel("Final Proportion of Fast Mover")
plt.title("Effect of Entry Timing on Fast Mover Advantage")
plt.grid(True)
plt.tight_layout()
#plt.show()

# === 2. Detecting Equilibrium Time ===
x = 0.5
fast_prop_eq = np.zeros(timesteps)
equilibrium_time = None

for t in range(timesteps):
    t_month = t * dt
    Rf = fast_init_investment * np.exp(a * x * (t_month - Tf_base)) - 1
    Rs = slow_init_investment * np.exp(a * (1 - x) * (t_month - Ts_base)) - 1
    Pf = Rf / (Rf + Rs)
    Ff = Pf * M
    Fs = (1 - Pf) * M
    delta_f = Ff - Fs
    dx = x * (1 - x) * delta_f
    fast_prop_eq[t] = x
    if t > 0 and equilibrium_time is None:
        if abs(fast_prop_eq[t] - fast_prop_eq[t-1]) < 1e-4:
            equilibrium_time = simulation_time[t]
    x += dx * dt
    x = np.clip(x, 0, 1)

plt.figure(figsize=(8, 5))
plt.plot(simulation_time, fast_prop_eq, label="Proportion of Fast Mover")
if equilibrium_time:
    plt.axvline(equilibrium_time, color="red", linestyle="--", label=f"Approx. Equilibrium at t = {equilibrium_time:.2f}")
plt.xlabel("Time (Months)")
plt.ylabel("Proportion of Fast Mover")
plt.title("Replicator Dynamics with Equilibrium Detection")
plt.legend()
plt.grid(True)
plt.tight_layout()
#plt.show()

# === 3. Initial Proportion Sensitivity ===
initials = np.linspace(0.05, 0.95, 10)
results = []

for init_x in initials:
    x = init_x
    for t in range(timesteps):
        t_month = t * dt
        Rf = fast_init_investment * np.exp(a * x * (t_month - Tf_base)) - 1
        Rs = slow_init_investment * np.exp(a * (1 - x) * (t_month - Ts_base)) - 1
        Pf = Rf / (Rf + Rs)
        Ff = Pf * M
        Fs = (1 - Pf) * M
        delta_f = Ff - Fs
        dx = x * (1 - x) * delta_f
        x += dx * dt
        x = np.clip(x, 0, 1)
    results.append((init_x, x))

initials, finals = zip(*results)
plt.figure(figsize=(8, 5))
plt.plot(initials, finals, marker='o')
plt.xlabel("Initial Proportion of Fast Mover")
plt.ylabel("Final Proportion of Fast Mover")
plt.title("Basins of Attraction for Fast Mover Strategy")
plt.grid(True)
plt.tight_layout()
plt.show()
