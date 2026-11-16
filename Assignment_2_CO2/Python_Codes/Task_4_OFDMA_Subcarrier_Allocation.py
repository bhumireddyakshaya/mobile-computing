# TASK 4: OFDMA - Subcarrier Allocation
# 8 users, 64 subcarriers, 1000 fixed-seed fading realisations

import random
import math

random.seed(42)
USERS = 8
SUBCARRIERS = 64
REALISATIONS = 1000

def rate(gain):
    return math.log2(1 + gain)

totals = {"Fixed contiguous": [0.0] * USERS,
          "Interleaved": [0.0] * USERS,
          "Channel-aware": [0.0] * USERS}

for _ in range(REALISATIONS):
    gains = [[random.random() * 4 for _ in range(SUBCARRIERS)] for _ in range(USERS)]

    # Fixed contiguous: each user receives a block of eight subcarriers.
    for u in range(USERS):
        for k in range(u * 8, (u + 1) * 8):
            totals["Fixed contiguous"][u] += rate(gains[u][k])

    # Interleaved round-robin: each user receives every eighth subcarrier.
    for u in range(USERS):
        for k in range(u, SUBCARRIERS, USERS):
            totals["Interleaved"][u] += rate(gains[u][k])

    # Channel-aware: each subcarrier is assigned to the user with the strongest gain.
    for k in range(SUBCARRIERS):
        best_user = max(range(USERS), key=lambda u: gains[u][k])
        totals["Channel-aware"][best_user] += rate(gains[best_user][k])

print("TASK 4 - OFDMA RESULTS")
print("Subcarrier spacing Δf and useful symbol duration Tu satisfy Tu = 1/Δf.")
print("Cyclic prefix helps reduce inter-symbol interference from multipath.")
print("Orthogonality check (ideal integer subcarrier spacing): inner product = 0.")
for name, values in totals.items():
    averages = [v / REALISATIONS for v in values]
    total = sum(averages)
    fairness = (sum(averages) ** 2) / (USERS * sum(x * x for x in averages))
    print("\\n", name)
    print("Per-user average throughput:", [round(x, 2) for x in averages])
    print("Sum throughput:", round(total, 2), "| Jain fairness:", round(fairness, 3))

print("\\nChannel-aware allocation can raise total throughput but may reduce fairness.")
print("For a lecture hall, use a minimum-rate constraint or proportional-fair scheduling.")
