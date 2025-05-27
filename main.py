import matplotlib.pyplot as plt
import numpy as np

# Time (0 to 12 months)
time = np.arange(0, 13, 1)


# Parameters
Tf = 0 # time entry of fast mover
Ts= 12 # time entry of slow mover

# say that they invest the same amount of money
fast_init_investment = 1
slow_init_investment = 1000

a = 0.6 # growth rate
x = 0.2 # proportion of fast mover

Rf = fast_init_investment * np.exp(a*(time - Tf))  # fast reputation
Rs = slow_init_investment * np.exp(a*(time - Ts))  # slow reputaiton


Pf = (Rf)/(Rf + Rs) # probability of fast mover getting market share
Ps = 1 - Pf # probability of slow mover getting market share

M = 100 # market value

Ff = Pf * M
Fs = (1 - Pf) * M
delta_f = Ff - Fs

X = (1-x)*x*delta_f


# Cumulative Payoff Comparison
# Y axis: cumulative payoff
# X axis: time t
# Shows the cumulative payoff of fast and slow mover over time.

# cumulative_payoff_fast = np.cumsum(Ff)
# cumulative_payoff_slow = np.cumsum(Fs)

# plt.figure(figsize=(10, 5))
# plt.plot(time, cumulative_payoff_fast, label="Fast Mover Cumulative Payoff", color="blue", linewidth=2)
# plt.plot(time, cumulative_payoff_slow, label="Slow Mover Cumulative Payoff", color="green", linestyle='--', linewidth=2)
# plt.axvline(Tf, color="blue", linestyle=":", label="Fast Entry (Tf)")
# plt.axvline(Ts, color="green", linestyle=":", label="Slow Entry (Ts)")
# plt.xlabel("Time (Months)")
# plt.ylabel("Cumulative Payoff (Scaled)")
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# Visualizing Replicator Dynamics over time
# Y axis: proportion of fast mover x
# X axis: time t
# Tells whether fast strategy grows or shrinks in the population.

# under condition where same investment and same maket proportion over period of 12 month
timesteps = 100
dt = 0.01
simulation_time = np.arange(0, timesteps*dt, dt)
fast_prop = np.zeros(timesteps) # proportion of of market share
slow_prop = np.zeros(timesteps) # proportion of of market share
x = 0.5 # initial proportion of fast mover starting equal to slow mover

for t in range(timesteps):
    t_month  = t * dt
    Rf = fast_init_investment * np.exp(a* x*(t_month - Tf)) - 1
    Rs = slow_init_investment * np.exp(a* (1-x)*(t_month - Ts)) - 1

    Pf = (Rf)/(Rf + Rs)
    Ps = 1 - Pf

    Ff = Pf * M
    Fs = (1 - Pf) * M
    delta_f = Ff - Fs

    dx = x * (1 - x) * delta_f
    fast_prop[t] = x
    slow_prop[t] = 1 - x
    x+= dx * dt
    x = np.clip(x, 0, 1)

plt.figure(figsize=(10, 5))
plt.plot(simulation_time, fast_prop, label="Proportion of Fast Mover", color="blue", linewidth=2)
plt.plot(simulation_time, slow_prop, label="Proportion of Slow Mover", color="green", linestyle='--', linewidth=2)
plt.xlabel("Time (Months)")
plt.ylabel("Proportion of Fast Mover")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# The graph shows that initially the fast mover has a steep rise peaking around 20%
# However, after peak it starts to decline meaning payoff advantage of fast mover weakens over time.
# What are potential reason for this?