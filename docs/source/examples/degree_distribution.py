from ts2vg import NaturalVG
import numpy as np
import matplotlib.pyplot as plt

# 1. Generate random time series (Brownian motion)
rng = np.random.default_rng(0)
ts = rng.standard_normal(size=100_000)
ts = np.cumsum(ts)

# 2. Build visibility graph
g = NaturalVG().build(ts, only_degrees=True)

# 3. Get degree distribution
ks, ps = g.degree_distribution

# 4. Make plots
fig, [ax0, ax1, ax2] = plt.subplots(ncols=3, figsize=(12, 3.5))

ax0.plot(ts, c="#000", linewidth=1)
ax0.set_title("Time Series")
ax0.set_xlabel("t")

ax1.scatter(ks, ps, s=2, c="#000", alpha=1)
ax1.set_title("Degree Distribution")
ax1.set_xlabel("k")
ax1.set_ylabel("P(k)")

ax2.scatter(ks, ps, s=2, c="#000", alpha=1)
ax2.set_yscale("log")
ax2.set_xscale("log")
ax2.set_title("Degree Distribution (log-log)")
ax2.set_xlabel("k")
ax2.set_ylabel("P(k)")
